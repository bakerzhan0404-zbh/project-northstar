"use strict";

const FilterModel = typeof window !== "undefined" ? window.NorthstarFilterModel : null;

const DEFAULT_VIEW = Object.freeze({
  liquidityDays: 14,
  paymentMeasure: "records",
  drawerTab: "overview",
});

const PAYMENT_MEASURES = Object.freeze({
  records: {
    valueKey: "records",
    shareKey: "record_share_pct",
    contributionKey: "record_contribution_pct",
    label: "records",
    displayLabel: "Records",
    headline: "of matching records in the priority union",
  },
  exceptions: {
    valueKey: "exceptions",
    shareKey: "exception_share_pct",
    contributionKey: "exception_contribution_pct",
    label: "exceptions",
    displayLabel: "Exceptions",
    headline: "of matching exceptions in the priority union",
  },
  repair_minutes: {
    valueKey: "repair_minutes",
    shareKey: "repair_share_pct",
    contributionKey: "repair_contribution_pct",
    label: "repair minutes",
    displayLabel: "Repair time",
    headline: "of matching repair effort in the priority union",
  },
});

const GUIDE_TOPICS = Object.freeze(["overview", "visibility", "liquidity", "payments", "regions", "gates"]);
const INLINE_TOPICS = Object.freeze(["decision", "visibility", "liquidity", "payments", "regions", "capacity", "closures"]);
const INLINE_GUIDE_TOPIC = Object.freeze({
  decision: "overview",
  visibility: "visibility",
  liquidity: "liquidity",
  payments: "payments",
  regions: "regions",
  capacity: "gates",
  closures: "gates",
});
const SEARCH_RESULT_LIMIT = 8;
const CLOSURE_CANDIDATE_RULE = "Dormant + legacy purpose + zero supplied payment records";
const VISUAL_COLORS = Object.freeze({
  purple: "#8474f5",
  teal: "#35b9ad",
  blue: "#6ca6e8",
  orange: "#ef8d61",
});
const COHORT_COLORS = Object.freeze([
  VISUAL_COLORS.purple,
  VISUAL_COLORS.teal,
  VISUAL_COLORS.blue,
  VISUAL_COLORS.orange,
]);
const METHOD_COLORS = Object.freeze([
  VISUAL_COLORS.blue,
  VISUAL_COLORS.teal,
  VISUAL_COLORS.purple,
  VISUAL_COLORS.orange,
]);
const REGION_PRESENTATION = Object.freeze({
  NA: Object.freeze({ left: 25, top: 41, color: "#3b6fb6" }),
  EMEA: Object.freeze({ left: 52, top: 43, color: "#267a6e" }),
  APAC: Object.freeze({ left: 78, top: 57, color: "#6655d9" }),
});

const state = { ...DEFAULT_VIEW };
let dashboardData = null;
let filterOptions = null;
let defaultFilters = null;
let draftFilters = null;
let appliedFilters = null;
let currentSummary = null;
let searchIndex = [];
let searchResults = [];
let activeSearchIndex = -1;
let lastDrawerOpener = null;
let lastFilterOpener = null;
let trendResizeObserver = null;
let trendAnimationFrame = null;

const get = (selector, root = document) => root.querySelector(selector);
const getAll = (selector, root = document) => Array.from(root.querySelectorAll(selector));

function setText(target, value) {
  const node = typeof target === "string" ? get(target) : target;
  if (node) node.textContent = String(value);
}

function make(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = String(text);
  return node;
}

function isFiniteNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function formatNumber(value, maximumFractionDigits = 0) {
  if (!isFiniteNumber(value)) return "—";
  return new Intl.NumberFormat("en-US", { maximumFractionDigits }).format(value);
}

function formatPercent(value) {
  return isFiniteNumber(value) ? `${formatNumber(value, 2)}%` : "—";
}

function safePercentage(numerator, denominator) {
  if (!isFiniteNumber(numerator) || !isFiniteNumber(denominator) || denominator === 0) return null;
  return Math.round((numerator / denominator) * 10000) / 100;
}

function clampedPercentage(value) {
  if (!isFiniteNumber(value)) return null;
  return Math.min(100, Math.max(0, value));
}

function formatUsdCompact(value) {
  if (!isFiniteNumber(value)) return "—";
  const sign = value < 0 ? "−" : "";
  const absolute = Math.abs(value);
  if (absolute >= 1_000_000) return `${sign}$${(absolute / 1_000_000).toFixed(2)}m`;
  if (absolute >= 1_000) return `${sign}$${formatNumber(absolute / 1_000, 1)}k`;
  if (absolute >= 1 || absolute === 0) return `${sign}$${formatNumber(absolute, 0)}`;
  return `${sign}$${new Intl.NumberFormat("en-US", { maximumSignificantDigits: 2 }).format(absolute)}`;
}

function plural(value, singular, pluralForm = `${singular}s`) {
  return `${formatNumber(value)} ${value === 1 ? singular : pluralForm}`;
}

function parseIsoDate(value) {
  const [year, month, day] = String(value).split("-").map(Number);
  return { year, month, day };
}

function formatIsoDate(value, { includeYear = true } = {}) {
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const { year, month, day } = parseIsoDate(value);
  if (!year || !months[month - 1] || !day) return String(value);
  return `${day} ${months[month - 1]}${includeYear ? ` ${year}` : ""}`;
}

function formatDateRange(dateFrom, dateTo) {
  const from = parseIsoDate(dateFrom);
  const to = parseIsoDate(dateTo);
  if (dateFrom === dateTo) return formatIsoDate(dateTo);
  if (from.year === to.year) {
    return `${formatIsoDate(dateFrom, { includeYear: false })}–${formatIsoDate(dateTo)}`;
  }
  return `${formatIsoDate(dateFrom)}–${formatIsoDate(dateTo)}`;
}

function announce(message) {
  setText("#dashboard-announcer", "");
  window.setTimeout(() => setText("#dashboard-announcer", message), 20);
}

function setDataControlsDisabled(disabled) {
  getAll("[data-requires-data]").forEach((node) => {
    node.disabled = disabled;
  });
  getAll("[data-inline-detail]").forEach((detail) => {
    if (disabled) detail.open = false;
    detail.hidden = disabled;
  });
}

function setKpiEmpty(selector, empty) {
  const node = get(selector);
  if (node) node.classList.toggle("kpi-empty", empty);
}

function assertDashboardData(data) {
  const required = [
    "meta",
    "decision",
    "visibility",
    "liquidity",
    "payments",
    "guardrails",
    "sources",
    "filtering",
    "definitions",
  ];
  for (const key of required) {
    if (!data || typeof data[key] !== "object") throw new Error(`Missing dashboard contract: ${key}`);
  }
  if (data.schema_version !== "2.0") throw new Error("Unsupported dashboard schema");
  if (!FilterModel || typeof FilterModel.summarize !== "function") {
    throw new Error("Filter model is unavailable");
  }
  if (data.liquidity.validated_mobility.value_usd !== null) {
    throw new Error("Validated mobility must remain not established");
  }
  if (data.liquidity.validated_mobility.status !== "not_established") {
    throw new Error("Validated mobility status is not fail-closed");
  }
  if (data.liquidity.funded_case.value_usd !== 0 || data.liquidity.funded_case.status !== "not_fundable") {
    throw new Error("Liquidity funded case is not fail-closed");
  }
  for (const topic of GUIDE_TOPICS) {
    if (!data.definitions[topic]) throw new Error(`Missing metric definition: ${topic}`);
  }
}

function showDataFailure() {
  dashboardData = null;
  currentSummary = null;
  document.body.classList.add("data-unavailable");
  get("#data-error").hidden = false;
  setDataControlsDisabled(true);
  clearVisualizationOutputs();
  closeSearch();
  closeFilterPanel({ restoreFocus: false });
  setText("#dashboard-scope", "Week 1–2 diagnostic snapshot · supplied data unavailable");
  setText("#data-status", "Unavailable — validation failed");
  ["#visibility-kpi", "#funded-case-value", "#payment-kpi", "#regional-kpi"].forEach((selector) => setText(selector, "Unavailable"));
  setText("#mobility-status", "No current result published.");
  setText("#liquidity-boundary", "Data unavailable — validation did not complete.");
  setText("#payment-boundary", "Data unavailable — validation did not complete.");
  setText("#closure-summary", "No current result published.");
  get("#dashboard-shell").setAttribute("aria-busy", "false");
}

function entityLabel(entityId) {
  if (!entityId || !filterOptions) return "All entities";
  const entity = filterOptions.entities.find((item) => item.value === entityId);
  return entity ? `${entity.value} — ${entity.label}` : entityId;
}

function filterContext(filters, { includeAll = true } = {}) {
  const parts = [formatDateRange(filters.dateFrom, filters.dateTo)];
  const entries = [
    [filters.currency, "All currencies"],
    [filters.region, "All regions"],
    [filters.entity ? entityLabel(filters.entity) : "", "All entities"],
    [filters.bank, "All banks"],
  ];
  entries.forEach(([value, fallback]) => {
    if (value || includeAll) parts.push(value || fallback);
  });
  return parts.join(" · ");
}

function dimensionFilterContext(filters, { includeAll = true } = {}) {
  const parts = [];
  const entries = [
    [filters.currency, "All currencies"],
    [filters.region, "All regions"],
    [filters.entity ? entityLabel(filters.entity) : "", "All entities"],
    [filters.bank, "All banks"],
  ];
  entries.forEach(([value, fallback]) => {
    if (value || includeAll) parts.push(value || fallback);
  });
  return parts.join(" · ");
}

function regionalFacetContext(filters) {
  return [
    formatDateRange(filters.dateFrom, filters.dateTo),
    filters.currency || "All currencies",
    filters.entity ? entityLabel(filters.entity) : "All entities",
    filters.bank || "All banks",
  ].join(" · ");
}

function activeFilterDescriptors(filters) {
  if (!defaultFilters) return [];
  const descriptors = [];
  if (filters.dateFrom !== defaultFilters.dateFrom || filters.dateTo !== defaultFilters.dateTo) {
    descriptors.push({ key: "date", label: formatDateRange(filters.dateFrom, filters.dateTo) });
  }
  if (filters.currency) descriptors.push({ key: "currency", label: filters.currency });
  if (filters.region) descriptors.push({ key: "region", label: filters.region });
  if (filters.entity) descriptors.push({ key: "entity", label: entityLabel(filters.entity) });
  if (filters.bank) descriptors.push({ key: "bank", label: filters.bank });
  return descriptors;
}

function isDefaultFilterState(filters) {
  return Boolean(defaultFilters) && Object.keys(defaultFilters).every((key) => filters[key] === defaultFilters[key]);
}

function currentScopeText() {
  if (!appliedFilters || !currentSummary) return "Loading current scope…";
  const prefix = currentSummary.scope.has_matches ? filterContext(appliedFilters) : `No matching data · ${filterContext(appliedFilters)}`;
  return `${prefix} · ${plural(currentSummary.scope.account_count, "account")} · ${plural(currentSummary.payments.overall.records, "supplied payment record")}`;
}

function renderInlineDetail(topic, { scope, evidence, nextAction }) {
  setText(`[data-detail-scope="${topic}"]`, scope);
  if (evidence !== undefined) setText(`[data-detail-evidence="${topic}"]`, evidence);
  setText(`[data-detail-action="${topic}"]`, nextAction);
}

function closeAllInlineDetails({ except = null } = {}) {
  getAll("[data-inline-detail]").forEach((detail) => {
    if (detail !== except) detail.open = false;
  });
}

function openInlineDetail(topic, { focusSummary = true } = {}) {
  if (!dashboardData || !INLINE_TOPICS.includes(topic)) return false;
  const detail = get(`[data-inline-detail="${topic}"]`);
  if (!detail || detail.hidden) return false;
  closeAllInlineDetails({ except: detail });
  detail.open = true;
  const summary = get(`[data-detail-summary="${topic}"]`, detail);
  if (focusSummary && summary) summary.focus();
  if (summary) summary.scrollIntoView({ block: "nearest" });
  return true;
}

function setCompositionRing(ringSelector, valueSelector, share, valueLabel, ariaLabel) {
  const ring = get(ringSelector);
  const boundedShare = clampedPercentage(share);
  if (!ring) return;
  ring.classList.toggle("is-empty", boundedShare === null);
  ring.style.setProperty("--ring-share", `${boundedShare ?? 0}%`);
  ring.setAttribute("aria-label", ariaLabel);
  setText(valueSelector, boundedShare === null ? "—" : valueLabel);
}

function visualTrack(fillClass, width, colorProperty, color) {
  const track = make("span", fillClass.includes("capacity") ? "capacity-bar-track" : "source-bar-track");
  track.setAttribute("aria-hidden", "true");
  const fill = make("span", fillClass);
  fill.style.setProperty("--bar-width", `${clampedPercentage(width) ?? 0}%`);
  if (colorProperty && color) fill.style.setProperty(colorProperty, color);
  track.append(fill);
  return track;
}

function renderDecisionEvidence() {
  const visibility = dashboardData.visibility;
  const payments = dashboardData.payments;
  const paymentShare = safePercentage(payments.priority_union.records, payments.overall.records);
  setText("#decision-visibility-chip", `${formatNumber(visibility.delayed_accounts)} / ${formatNumber(visibility.accounts_total)} accounts delayed`);
  setText("#decision-liquidity-chip", `${dashboardData.liquidity.funded_case.display} funded case · mobility not established`);
  setText("#decision-payments-chip", `${formatPercent(paymentShare)} of supplied records in the priority union`);
  setText("#decision-composite-note", "Separate signals—not a composite score.");
}

function renderVisibilityAnalytics(visibility, hasData) {
  const delayedShare = hasData ? visibility.delayed_account_share_pct : null;
  setCompositionRing(
    "#visibility-ring",
    "#visibility-ring-value",
    delayedShare,
    formatPercent(delayedShare),
    hasData
      ? `${plural(visibility.delayed_accounts, "account")} delayed and ${plural(visibility.same_day_accounts, "account")} same-day in the selected scope.`
      : "No matching selected-account visibility composition.",
  );

  const list = get("#visibility-source-bars");
  const empty = get("#visibility-source-empty");
  list.replaceChildren();
  list.hidden = !hasData;
  empty.hidden = hasData;
  if (!hasData) return;

  visibility.by_method.forEach((method, index) => {
    const row = make("li", "source-bar-row");
    const copy = make("span", "source-bar-copy");
    const delayText = method.accounts_total === 0
      ? "No selected accounts"
      : `${plural(method.delayed_accounts, "delayed account")} · max ${formatNumber(method.maximum_delay_days)} calendar ${method.maximum_delay_days === 1 ? "day" : "days"}`;
    copy.append(make("strong", "", method.method), make("span", "", delayText));
    const track = visualTrack("source-bar-fill", method.account_share_pct, "--bar-color", METHOD_COLORS[index % METHOD_COLORS.length]);
    const value = make("span", "source-bar-value", `${formatNumber(method.accounts_total)} · ${formatPercent(method.account_share_pct)}`);
    row.append(copy, track, value);
    list.append(row);
  });
}

function visibilityActionText(visibility, hasData) {
  if (!hasData) return "No visibility action is derived for an empty scope.";
  const delayedMethods = visibility.by_method
    .filter((method) => method.delayed_accounts > 0)
    .map((method) => method.method);
  if (delayedMethods.length === 0) {
    return "No delayed reporting method is evidenced in the selected scope; validate timestamps before changing the pilot population.";
  }
  const methods = new Intl.ListFormat("en-US", { style: "long", type: "conjunction" }).format(delayedMethods);
  return `Prioritize ${methods} reporting exposure in the selected scope; validate timestamps, cutoffs, and ownership.`;
}

function renderHeader() {
  const scopeState = currentSummary.scope.has_matches
    ? plural(currentSummary.scope.account_count, "account")
    : "No matching accounts";
  setText(
    "#dashboard-scope",
    `Week 1–2 diagnostic snapshot · ${formatDateRange(appliedFilters.dateFrom, appliedFilters.dateTo)} · ${scopeState} · supplied data, not live operations`,
  );
  setText("#data-status", "Reconciled to supplied controls · source certification open");
  setText("#decision-title", dashboardData.decision.headline);
  setText("#decision-support", dashboardData.decision.next_step);
  renderDecisionEvidence();
  renderInlineDetail("decision", {
    scope: `Portfolio-wide decision; filters do not change it. Diagnostic scope: ${currentScopeText()}`,
    evidence: dashboardData.definitions.overview.meaning,
    nextAction: dashboardData.decision.next_step,
  });
}

function renderFilterChrome() {
  const descriptors = activeFilterDescriptors(appliedFilters);
  const count = descriptors.length;
  const countNode = get("#filter-count");
  countNode.hidden = count === 0;
  countNode.textContent = String(count);
  countNode.setAttribute("aria-label", `${count} active ${count === 1 ? "filter" : "filters"}`);
  setText("#filter-scope-summary", currentScopeText());
  get("#clear-active-filters").hidden = count === 0;

  const chips = get("#active-filter-chips");
  chips.replaceChildren();
  descriptors.forEach((descriptor) => {
    const item = make("span", "filter-chip-item");
    item.setAttribute("role", "listitem");
    const button = make("button", "filter-chip", `${descriptor.label} ×`);
    button.type = "button";
    button.dataset.removeFilter = descriptor.key;
    button.setAttribute("aria-label", `Remove filter: ${descriptor.label}`);
    button.addEventListener("click", () => removeAppliedFilter(descriptor.key));
    item.append(button);
    chips.append(item);
  });
  chips.hidden = count === 0;

  const emptyState = get("#filter-empty-state");
  emptyState.hidden = currentSummary.scope.has_matches;
  document.body.classList.toggle("scope-empty", !currentSummary.scope.has_matches);
  updateResetState();
}

function renderVisibility() {
  const visibility = currentSummary.visibility;
  const hasData = currentSummary.scope.has_matches && visibility.accounts_total > 0;
  setKpiEmpty("#visibility-kpi", !hasData);

  if (!hasData) {
    setText("#visibility-kpi", "No matching data");
    setText("#same-day-label", "—");
    setText("#delayed-label", "—");
    setText("#visibility-interpretation", "No account-day evidence matches the selected scope.");
  } else {
    setText("#visibility-kpi", `${visibility.delayed_accounts} / ${visibility.accounts_total}`);
    setText("#same-day-label", `${visibility.same_day_accounts} same-day`);
    setText("#delayed-label", `${visibility.delayed_accounts} delayed`);
    setText(
      "#visibility-interpretation",
      `${plural(visibility.delayed_accounts, "selected account")} show at least one calendar-date reporting delay.`,
    );
  }
  renderVisibilityAnalytics(visibility, hasData);
  const selectedAction = visibilityActionText(visibility, hasData);
  setText("#visibility-action-insight", selectedAction);
  setText("#visibility-summary-boundary", "Calendar-date proxy · not start-of-day or elapsed-24-hour visibility");
  setText("#visibility-boundary", "Reporting-date proxy—not start-of-day or elapsed-24-hour performance.");
  renderInlineDetail("visibility", {
    scope: currentScopeText(),
    nextAction: selectedAction,
  });
}

function liquidityScenario(days) {
  return currentSummary.liquidity.scenarios[String(days)];
}

function liquidityScenarioAvailable(days) {
  const scenario = liquidityScenario(days);
  return Boolean(currentSummary.scope.has_matches && scenario && isFiniteNumber(scenario.screen_usd));
}

function waterfallBarGeometry(steps) {
  const bounds = [0];
  const spans = steps.map((step) => {
    if (!isFiniteNumber(step.total_usd)) return null;
    if (step.role === "deduction" && isFiniteNumber(step.delta_usd)) {
      const before = step.total_usd - step.delta_usd;
      const low = Math.min(before, step.total_usd);
      const high = Math.max(before, step.total_usd);
      bounds.push(low, high);
      return { low, high };
    }
    const low = Math.min(0, step.total_usd);
    const high = Math.max(0, step.total_usd);
    bounds.push(low, high);
    return { low, high };
  });
  const minimum = Math.min(...bounds);
  const maximum = Math.max(...bounds);
  const range = maximum - minimum || 1;
  return spans.map((span) => span && ({
    bottom: ((span.low - minimum) / range) * 100,
    height: ((span.high - span.low) / range) * 100,
  }));
}

function renderLiquidityWaterfall(liquidity) {
  const waterfall = liquidity.waterfalls[String(state.liquidityDays)];
  const list = get("#liquidity-waterfall");
  const empty = get("#liquidity-waterfall-empty");
  list.replaceChildren();
  setText("#liquidity-analytics-period", `${state.liquidityDays}-day screen · as of ${formatIsoDate(liquidity.as_of_date)}`);

  const available = Boolean(currentSummary.scope.has_matches && waterfall && waterfall.complete);
  list.hidden = !available;
  empty.hidden = available;
  if (!available) {
    setText("#liquidity-waterfall-note", `No complete ${state.liquidityDays}-day account panel is available; no waterfall is drawn.`);
    return;
  }

  const geometry = waterfallBarGeometry(waterfall.steps);
  waterfall.steps.forEach((step, index) => {
    const item = make("li", "waterfall-step");
    item.dataset.role = step.role;
    const plot = make("span", "waterfall-plot");
    plot.setAttribute("aria-hidden", "true");
    const bar = make("span", "waterfall-bar");
    bar.style.setProperty("--bar-bottom", `${geometry[index].bottom}%`);
    bar.style.setProperty("--bar-height", `${geometry[index].height}%`);
    plot.append(bar);
    const label = make("span", "waterfall-label", step.label);
    const shownValue = step.role === "deduction" ? step.delta_usd : step.total_usd;
    const value = make("strong", "waterfall-value", formatUsdCompact(shownValue));
    item.append(plot, label, value);
    list.append(item);
  });
  setText(
    "#liquidity-waterfall-note",
    `Raw ${state.liquidityDays}-day buffer ${formatUsdCompact(waterfall.raw_buffer_usd)} · effective deduction after account-level floors ${formatUsdCompact(waterfall.effective_buffer_deduction_usd)} · unapplied because of floors ${formatUsdCompact(waterfall.unapplied_buffer_due_to_floor_usd)}.`,
  );
}

function liquidityTrendValue(point, days) {
  const scenario = point && point.scenarios && point.scenarios[String(days)];
  return scenario && scenario.complete && isFiniteNumber(scenario.screen_usd) ? scenario.screen_usd : null;
}

function lastFiniteTrendValue(trend, days) {
  for (let index = trend.length - 1; index >= 0; index -= 1) {
    const value = liquidityTrendValue(trend[index], days);
    if (isFiniteNumber(value)) return value;
  }
  return null;
}

function renderLiquidityTrendTable(trend) {
  const body = get("#liquidity-trend-table-body");
  body.replaceChildren();
  trend.forEach((point) => {
    const row = make("tr");
    const date = make("th", "", formatIsoDate(point.date));
    date.scope = "row";
    const seven = make("td", "numeric", formatUsdCompact(liquidityTrendValue(point, 7)));
    const fourteen = make("td", "numeric", formatUsdCompact(liquidityTrendValue(point, 14)));
    row.append(date, seven, fourteen);
    body.append(row);
  });
}

function canvasThemeColor(name, fallback) {
  if (typeof window === "undefined") return fallback;
  const value = window.getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return value || fallback;
}

function drawLiquidityTrendCanvas() {
  trendAnimationFrame = null;
  const canvas = get("#liquidity-trend-canvas");
  const frame = get("#liquidity-trend-frame");
  if (!canvas || !frame || !currentSummary) return;
  const context = canvas.getContext("2d");
  if (!context) return;

  const trend = currentSummary.liquidity.trend;
  const cssWidth = Math.max(280, Math.floor(frame.getBoundingClientRect().width - 16) || 720);
  const cssHeight = Math.max(160, Math.floor(canvas.getBoundingClientRect().height) || 220);
  const ratio = Math.min(2, Math.max(1, window.devicePixelRatio || 1));
  canvas.width = Math.round(cssWidth * ratio);
  canvas.height = Math.round(cssHeight * ratio);
  context.setTransform(ratio, 0, 0, ratio, 0, 0);
  context.clearRect(0, 0, cssWidth, cssHeight);

  const series = [
    { days: 7, color: canvasThemeColor("--purple", VISUAL_COLORS.purple) },
    { days: 14, color: canvasThemeColor("--aqua", VISUAL_COLORS.teal) },
  ];
  const values = series.flatMap(({ days }) => trend.map((point) => liquidityTrendValue(point, days))).filter(isFiniteNumber);
  const foreground = "#f7fbff";
  const muted = canvasThemeColor("--analytics-muted", "#b8c8d8");
  const grid = canvasThemeColor("--analytics-border", "#2b435d");
  context.font = "11px Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif";

  if (trend.length === 0 || values.length === 0) {
    context.fillStyle = muted;
    context.textAlign = "center";
    context.fillText("No complete liquidity trend is available for this scope.", cssWidth / 2, cssHeight / 2);
    return;
  }

  const margin = { top: 16, right: 14, bottom: 28, left: 58 };
  const plotWidth = Math.max(1, cssWidth - margin.left - margin.right);
  const plotHeight = Math.max(1, cssHeight - margin.top - margin.bottom);
  let minimum = Math.min(...values);
  let maximum = Math.max(...values);
  const valueSpan = maximum - minimum;
  const padding = valueSpan === 0 ? Math.max(Math.abs(maximum) * 0.08, 1) : valueSpan * 0.08;
  minimum = minimum >= 0 ? Math.max(0, minimum - padding) : minimum - padding;
  maximum += padding;
  if (maximum === minimum) maximum = minimum + 1;
  const x = (index) => margin.left + (trend.length === 1 ? plotWidth / 2 : (index / (trend.length - 1)) * plotWidth);
  const y = (value) => margin.top + ((maximum - value) / (maximum - minimum)) * plotHeight;

  context.strokeStyle = grid;
  context.fillStyle = muted;
  context.lineWidth = 1;
  context.textAlign = "right";
  context.textBaseline = "middle";
  for (let tick = 0; tick <= 3; tick += 1) {
    const value = minimum + ((maximum - minimum) * tick) / 3;
    const position = y(value);
    context.beginPath();
    context.moveTo(margin.left, position);
    context.lineTo(cssWidth - margin.right, position);
    context.stroke();
    context.fillText(formatUsdCompact(value), margin.left - 8, position);
  }

  context.textBaseline = "alphabetic";
  context.textAlign = "left";
  context.fillText(formatIsoDate(trend[0].date, { includeYear: false }), margin.left, cssHeight - 7);
  context.textAlign = "right";
  context.fillText(formatIsoDate(trend[trend.length - 1].date), cssWidth - margin.right, cssHeight - 7);

  series.forEach(({ days, color }) => {
    context.beginPath();
    context.strokeStyle = color;
    context.lineWidth = 2.25;
    context.lineJoin = "round";
    context.lineCap = "round";
    context.setLineDash(days === 14 ? [6, 4] : []);
    let drawing = false;
    let lastPoint = null;
    trend.forEach((point, index) => {
      const value = liquidityTrendValue(point, days);
      if (!isFiniteNumber(value)) {
        drawing = false;
        return;
      }
      const pointX = x(index);
      const pointY = y(value);
      if (!drawing) context.moveTo(pointX, pointY);
      else context.lineTo(pointX, pointY);
      drawing = true;
      lastPoint = { x: pointX, y: pointY };
    });
    context.stroke();
    if (lastPoint) {
      context.beginPath();
      context.arc(lastPoint.x, lastPoint.y, 3.5, 0, Math.PI * 2);
      context.strokeStyle = color;
      context.lineWidth = 2;
      context.stroke();
    }
  });
  context.setLineDash([]);
  context.fillStyle = foreground;
}

function scheduleLiquidityTrendDraw() {
  if (typeof window === "undefined" || trendAnimationFrame !== null) return;
  trendAnimationFrame = window.requestAnimationFrame(drawLiquidityTrendCanvas);
}

function setupLiquidityTrendResizeHandling() {
  const frame = get("#liquidity-trend-frame");
  if (typeof window.ResizeObserver === "function" && frame) {
    trendResizeObserver = new window.ResizeObserver(() => scheduleLiquidityTrendDraw());
    trendResizeObserver.observe(frame);
  }
  window.addEventListener("resize", scheduleLiquidityTrendDraw);
}

function renderLiquidityTrend(liquidity) {
  const trend = Array.isArray(liquidity.trend) ? liquidity.trend : [];
  const sevenEndpoint = lastFiniteTrendValue(trend, 7);
  const fourteenEndpoint = lastFiniteTrendValue(trend, 14);
  setText("#trend-7-endpoint", formatUsdCompact(sevenEndpoint));
  setText("#trend-14-endpoint", formatUsdCompact(fourteenEndpoint));
  renderLiquidityTrendTable(trend);
  const canvas = get("#liquidity-trend-canvas");
  const start = trend.length ? formatIsoDate(trend[0].date) : "the selected start";
  const end = trend.length ? formatIsoDate(trend[trend.length - 1].date) : "the selected end";
  canvas.setAttribute(
    "aria-label",
    `Unfilled 7-day and 14-day modeled screen lines from ${start} to ${end}. Current endpoints: 7-day ${formatUsdCompact(sevenEndpoint)}; 14-day ${formatUsdCompact(fourteenEndpoint)}. Missing complete windows are shown as gaps.`,
  );
  scheduleLiquidityTrendDraw();
}

function renderLiquidity({ shouldAnnounce = false } = {}) {
  const liquidity = currentSummary.liquidity;
  const selected = liquidityScenario(state.liquidityDays);
  const selectedAvailable = liquidityScenarioAvailable(state.liquidityDays);

  setText("#funded-case-value", dashboardData.liquidity.funded_case.display);
  setText("#mobility-status", "Validated mobility: not established by supplied data.");
  setText("#screen-7-value", liquidityScenarioAvailable(7) ? formatUsdCompact(liquidityScenario(7).screen_usd) : "—");
  setText("#screen-14-value", liquidityScenarioAvailable(14) ? formatUsdCompact(liquidityScenario(14).screen_usd) : "—");
  setText(
    "#liquidity-summary-screen",
    selectedAvailable
      ? `${formatUsdCompact(selected.screen_usd)} · ${state.liquidityDays}-day screen · as of ${formatIsoDate(liquidity.as_of_date)}`
      : `${state.liquidityDays}-day screen unavailable · as of ${formatIsoDate(liquidity.as_of_date)}`,
  );

  if (selectedAvailable) {
    setText(
      "#liquidity-interpretation",
      `${formatUsdCompact(selected.screen_usd)} is the selected ${state.liquidityDays}-day modeled screen as of ${formatIsoDate(liquidity.as_of_date)}.`,
    );
    setText(
      "#liquidity-boundary",
      `${formatUsdCompact(selected.screen_usd)} is a ${state.liquidityDays}-day screening sensitivity—not surplus cash or transfer authorization.`,
    );
  } else {
    setText(
      "#liquidity-interpretation",
      `${state.liquidityDays}-day screening is unavailable as of ${formatIsoDate(liquidity.as_of_date)}.`,
    );
    setText(
      "#liquidity-boundary",
      `No matching data or complete ${state.liquidityDays}-day window is available; validated mobility remains not established.`,
    );
  }

  getAll('input[name="liquidity-days"]').forEach((input) => {
    input.checked = Number(input.value) === state.liquidityDays;
  });
  renderLiquidityWaterfall(liquidity);
  renderLiquidityTrend(liquidity);
  renderInlineDetail("liquidity", {
    scope: `As of ${formatIsoDate(liquidity.as_of_date)} · trailing ${state.liquidityDays} calendar days · From date does not constrain this screen · ${dimensionFilterContext(appliedFilters)} · ${plural(currentSummary.scope.account_count, "account")}`,
    nextAction: dashboardData.definitions.liquidity.next_action,
  });
  if (get("#evidence-dialog").open && state.drawerTab === "liquidity") renderDrawerPanel("liquidity");
  updateResetState();

  if (shouldAnnounce) {
    const result = selectedAvailable
      ? `Screening result ${formatUsdCompact(selected.screen_usd)}.`
      : "Screening result unavailable for this scope.";
    announce(
      `${state.liquidityDays}-day screen selected. ${result} Validated mobility remains not established; funded case stays at ${dashboardData.liquidity.funded_case.display}.`,
    );
  }
}

function paymentMeasureData() {
  const config = PAYMENT_MEASURES[state.paymentMeasure];
  const union = currentSummary.payments.priority_union;
  const overall = currentSummary.payments.overall;
  return {
    config,
    unionValue: union[config.valueKey],
    totalValue: overall[config.valueKey],
    share: union[config.shareKey],
  };
}

function paymentCohortVisualRows(payments, measureKey) {
  const config = PAYMENT_MEASURES[measureKey];
  if (!config || !payments || !Array.isArray(payments.cohort_order)) return [];
  const totalValue = payments.overall[config.valueKey];
  if (!isFiniteNumber(totalValue) || totalValue <= 0) return [];
  return payments.cohort_order.map((label, index) => {
    const cohort = payments.cohorts[label];
    const value = cohort[config.valueKey];
    const suppliedContribution = cohort[config.contributionKey];
    const contribution = isFiniteNumber(suppliedContribution)
      ? suppliedContribution
      : safePercentage(value, totalValue);
    return {
      label,
      value,
      contribution,
      color: COHORT_COLORS[index % COHORT_COLORS.length],
    };
  });
}

function renderPaymentAnalytics({ config, unionValue, totalValue, share }) {
  const hasComparableMeasure = totalValue > 0 && isFiniteNumber(share);
  setText("#payment-visual-measure", config.displayLabel);
  setText("#payment-stack-title", `Share of all matching ${config.label}`);
  setCompositionRing(
    "#payment-ring",
    "#payment-ring-value",
    hasComparableMeasure ? share : null,
    formatPercent(share),
    hasComparableMeasure
      ? `The priority union contains ${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label}, ${formatPercent(share)}.`
      : `No matching ${config.label}; no percentage is calculated.`,
  );

  const stack = get("#payment-cohort-stack");
  const legend = get("#payment-cohort-legend");
  const empty = get("#payment-cohort-empty");
  stack.replaceChildren();
  legend.replaceChildren();
  stack.hidden = !hasComparableMeasure;
  legend.hidden = !hasComparableMeasure;
  empty.hidden = hasComparableMeasure;
  if (!hasComparableMeasure) {
    stack.setAttribute("aria-label", `No matching ${config.label}; no cohort composition is drawn.`);
    return;
  }

  const descriptions = [];
  paymentCohortVisualRows(currentSummary.payments, state.paymentMeasure).forEach((row) => {
    const segment = make("span", "cohort-segment");
    segment.style.setProperty("--segment-width", `${clampedPercentage(row.contribution) ?? 0}%`);
    segment.style.setProperty("--segment-color", row.color);
    segment.setAttribute("aria-hidden", "true");
    stack.append(segment);

    const item = make("li");
    const swatch = make("i", "legend-swatch");
    swatch.style.backgroundColor = row.color;
    swatch.setAttribute("aria-hidden", "true");
    item.append(
      swatch,
      make("span", "", row.label),
      make("strong", "", `${formatNumber(row.value)} · ${formatPercent(row.contribution)}`),
    );
    legend.append(item);
    descriptions.push(`${row.label}: ${formatNumber(row.value)} ${config.label}, ${formatPercent(row.contribution)}`);
  });
  stack.setAttribute("aria-label", `${config.displayLabel} composition. ${descriptions.join("; ")}.`);
}

function renderPayments({ shouldAnnounce = false } = {}) {
  const { config, unionValue, totalValue, share } = paymentMeasureData();
  const overlap = currentSummary.payments.cohorts["Manual touch + cross-border wire"];
  const hasComparableMeasure = totalValue > 0 && isFiniteNumber(share);
  setKpiEmpty("#payment-kpi", !hasComparableMeasure);

  if (hasComparableMeasure) {
    setText("#payment-kpi", formatPercent(share));
    setText("#payment-kpi-label", `${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label}`);
    setText(
      "#payment-union-label",
      `${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label} · ${formatPercent(share)}`,
    );
  } else {
    setText("#payment-kpi", "—");
    setText("#payment-kpi-label", "No matching data for the selected measure");
    setText("#payment-union-label", `No matching ${config.label}; no percentage is calculated.`);
  }
  renderPaymentAnalytics({ config, unionValue, totalValue, share });

  if (currentSummary.payments.overall.records > 0) {
    setText("#payment-overlap", `${formatNumber(overlap.records)} overlap records are counted once.`);
    setText(
      "#payment-boundary",
      `Within ${formatNumber(currentSummary.payments.overall.records)} matching supplied records only; association, not causation.`,
    );
  } else {
    setText("#payment-overlap", "No matching payment records in the selected scope.");
    setText("#payment-boundary", "No matching supplied records; no payment percentage is calculated.");
  }

  getAll('input[name="payment-measure"]').forEach((input) => {
    input.checked = input.value === state.paymentMeasure;
  });
  renderInlineDetail("payments", {
    scope: currentScopeText(),
    nextAction: dashboardData.definitions.payments.next_action,
  });
  if (get("#evidence-dialog").open && state.drawerTab === "payments") renderDrawerPanel("payments");
  updateResetState();

  if (shouldAnnounce) {
    const message = hasComparableMeasure
      ? `Priority union contains ${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label}, ${formatPercent(share)}.`
      : `No matching ${config.label}; no percentage is calculated.`;
    announce(`${config.label} selected. ${message}`);
  }
}

function renderCapacityComparison(capacity) {
  const rows = [
    {
      label: "Process-file exception repair",
      note: "Management process estimate",
      value: capacity.process_file_exception_repair_hours_monthly,
    },
    {
      label: "Payment-file repair",
      note: "Supplied payment-file estimate",
      value: capacity.payment_file_repair_hours_monthly,
    },
  ];
  const maximum = Math.max(...rows.map((row) => row.value));
  const list = get("#capacity-comparison-bars");
  list.replaceChildren();
  rows.forEach((row) => {
    const item = make("li", "capacity-bar-row");
    const copy = make("span", "capacity-bar-copy");
    copy.append(make("strong", "", row.label), make("span", "", row.note));
    const track = visualTrack("capacity-bar-fill", safePercentage(row.value, maximum));
    const value = make("span", "capacity-bar-value", `${formatNumber(row.value, 1)} h/month`);
    item.append(copy, track, value);
    list.append(item);
  });
}

function appendTableCell(row, tag, text, className = "") {
  const cell = make(tag, className, text);
  row.append(cell);
  return cell;
}

function regionalMarkerSize(accountCount, maximumAccountCount) {
  if (!isFiniteNumber(accountCount) || accountCount <= 0 || maximumAccountCount <= 0) return 52;
  return 64 + Math.round(Math.sqrt(accountCount / maximumAccountCount) * 20);
}

function focusRegionalControl(region, source) {
  window.requestAnimationFrame(() => {
    const selector = region
      ? `[data-region-${source}-action="${region}"]`
      : "#regional-all-button";
    const control = get(selector);
    if (control) control.focus();
  });
}

function applyRegionalSelection(region, source = "marker") {
  if (!dashboardData || !appliedFilters) return false;
  if (appliedFilters.region === region) {
    const selectedRow = region && currentSummary
      ? currentSummary.regional.rows.find((item) => item.code === region)
      : null;
    announce(
      selectedRow && selectedRow.status !== "available"
        ? `${selectedRow.label} is applied, but no accounts match the other active filters.`
        : region
          ? `${region} is already selected.`
          : "All regions are already selected.",
    );
    return true;
  }
  const row = region && currentSummary
    ? currentSummary.regional.rows.find((item) => item.code === region)
    : null;
  if (row && row.status !== "available") {
    announce(`${row.label} is unavailable under the other active filters.`);
    return false;
  }
  const label = row ? row.label : "All regions";
  const applied = applyFilterCandidate(
    { ...appliedFilters, region },
    { closePanel: true, message: `${label} ${region ? "region" : "scope"} applied.` },
  );
  if (applied) focusRegionalControl(region, source);
  return applied;
}

function bindRegionalMarkerKeyboard(buttons) {
  buttons.forEach((button, index) => {
    button.addEventListener("keydown", (event) => {
      let nextIndex = null;
      if (["ArrowRight", "ArrowDown"].includes(event.key)) nextIndex = (index + 1) % buttons.length;
      if (["ArrowLeft", "ArrowUp"].includes(event.key)) nextIndex = (index - 1 + buttons.length) % buttons.length;
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = buttons.length - 1;
      if (nextIndex === null) return;
      event.preventDefault();
      buttons[nextIndex].focus();
    });
  });
}

function regionalDelayedText(row) {
  if (row.status !== "available") return "No matching data";
  if (!isFiniteNumber(row.visibility.delayed_account_share_pct)) return "No supplied account-day evidence";
  return `${formatNumber(row.visibility.delayed_accounts)} / ${formatNumber(row.account_count)} · ${formatPercent(row.visibility.delayed_account_share_pct)}`;
}

function regionalPaymentText(row) {
  if (row.status !== "available") return "—";
  const share = row.payments.priority_union_record_share_pct;
  if (row.payments.records === 0 || !isFiniteNumber(share)) return "0 supplied records · share unavailable";
  return `${formatNumber(row.payments.priority_union_records)} / ${formatNumber(row.payments.records)} · ${formatPercent(share)}`;
}

function makeRegionalAction(row, source) {
  const button = make("button", source === "marker" ? "regional-marker" : "regional-table-action");
  button.type = "button";
  button.dataset[`region${source[0].toUpperCase()}${source.slice(1)}Action`] = row.code;
  button.setAttribute("aria-pressed", String(row.selected));
  const available = row.status === "available";
  if (!available) button.setAttribute("aria-disabled", "true");
  const action = row.selected ? `${row.label} selected` : `Filter to ${row.label}`;
  button.setAttribute(
    "aria-label",
    available
      ? `${action}: ${plural(row.account_count, "matching account")}, ${plural(row.visibility.delayed_accounts, "delayed account")}.`
      : row.selected
        ? `${row.label} applied but no accounts match the other active filters.`
        : `${row.label} unavailable: no accounts match the other active filters.`,
  );
  if (available || source === "marker") {
    button.addEventListener("click", () => applyRegionalSelection(row.code, source));
  }
  return button;
}

function renderRegionalFootprint(regional) {
  const markerGroup = get("#regional-map-markers");
  const table = get("#regional-evidence-table");
  const tableWrap = get(".regional-table-wrap");
  const tableBody = get("#regional-evidence-table-body");
  const empty = get("#regional-map-empty");
  const allButton = get("#regional-all-button");
  markerGroup.replaceChildren();
  tableBody.replaceChildren();

  const availableRows = regional.rows.filter((row) => row.status === "available");
  const maximumAccountCount = Math.max(0, ...availableRows.map((row) => row.account_count));
  const hasAnyRegion = availableRows.length > 0;
  empty.hidden = hasAnyRegion;
  table.hidden = !hasAnyRegion;
  tableWrap.hidden = !hasAnyRegion;
  allButton.setAttribute("aria-pressed", String(!regional.selected_region));

  const markerButtons = [];
  regional.rows.forEach((row) => {
    const presentation = REGION_PRESENTATION[row.code];
    if (!presentation) throw new Error(`Missing regional map position: ${row.code}`);
    const marker = makeRegionalAction(row, "marker");
    marker.style.setProperty("--marker-left", `${presentation.left}%`);
    marker.style.setProperty("--marker-top", `${presentation.top}%`);
    marker.style.setProperty("--marker-color", presentation.color);
    marker.style.setProperty("--marker-size", `${regionalMarkerSize(row.account_count, maximumAccountCount)}px`);
    marker.append(
      make("strong", "", row.code),
      make(
        "span",
        "",
        row.status === "available"
          ? plural(row.account_count, "account")
          : row.selected
            ? "Applied · no matches"
            : "Unavailable",
      ),
      make(
        "small",
        "",
        row.status === "available"
          ? (row.selected ? "Selected" : "Select region")
          : "0 matching accounts",
      ),
    );
    markerGroup.append(marker);
    markerButtons.push(marker);

    const tableRow = make("tr");
    const heading = appendTableCell(tableRow, "th", `${row.code} · ${row.label}`);
    heading.scope = "row";
    appendTableCell(tableRow, "td", row.status === "available" ? formatNumber(row.account_count) : "—", "numeric");
    appendTableCell(tableRow, "td", regionalDelayedText(row));
    appendTableCell(tableRow, "td", regionalPaymentText(row));
    const closureText = row.status !== "available"
      ? "—"
      : row.closures.validation_candidates === 0
        ? "0 · No candidates"
        : formatNumber(row.closures.validation_candidates);
    appendTableCell(tableRow, "td", closureText, "numeric");
    const actionCell = appendTableCell(tableRow, "td", "");
    const actionButton = makeRegionalAction(row, "table");
    actionButton.textContent = row.status !== "available"
      ? (row.selected ? "Applied · no matches" : "Unavailable")
      : row.selected
        ? `${row.code} selected`
        : `Filter to ${row.code}`;
    actionButton.disabled = row.status !== "available";
    actionCell.append(actionButton);
    tableBody.append(tableRow);
  });
  bindRegionalMarkerKeyboard(markerButtons);
}

function renderRegions() {
  const regional = currentSummary.regional;
  const selectedScopeHasData = currentSummary.scope.has_matches;
  const facetHasData = regional.basis.account_count > 0;
  const activeRegionHasNoMatches = Boolean(regional.selected_region && !selectedScopeHasData);
  const representedRegionCount = regional.selected_region && selectedScopeHasData
    ? 1
    : regional.basis.regions_represented;
  setKpiEmpty("#regional-kpi", !facetHasData);
  setText("#regional-kpi", facetHasData ? formatNumber(representedRegionCount) : "—");
  setText(
    "#regional-kpi-label",
    facetHasData
      ? activeRegionHasNoMatches
        ? `${representedRegionCount === 1 ? "comparable region" : "comparable regions"}`
        : `${representedRegionCount === 1 ? "region" : "regions"} represented`
      : "No matching regional data",
  );
  setText(
    "#regional-summary-context",
    selectedScopeHasData
      ? `${plural(currentSummary.scope.account_count, "selected account")} · Week 1–2 scope`
      : facetHasData
        ? `${plural(regional.basis.account_count, "comparable account")} · other filters held constant`
        : "No matching data",
  );
  setText(
    "#regional-selection-status",
    regional.selected_region
      ? `${regional.selected_region} applied${selectedScopeHasData ? "" : " · no matches"}`
      : "All regions",
  );
  setText(
    "#regional-facet-basis",
    `Comparison basis: each row overrides region · ${regionalFacetContext(appliedFilters)}`,
  );
  setText(
    "#regional-interpretation",
    "Use the region selector to test whether reporting and payment signals persist in a narrower operating scope.",
  );
  setText(
    "#regional-boundary",
    "Schematic region positions—not bank, account, cash, legal-domicile, or transfer-path locations. Liquidity is intentionally not plotted here.",
  );
  renderInlineDetail("regions", {
    scope: `Regional facet holds date, currency, entity, and bank constant while each row overrides region · ${regionalFacetContext(appliedFilters)}`,
    evidence: "Supplied Week 1–2 diagnostic classifications only. The map is not live and does not locate cash, accounts, banks, owners, or transfer paths.",
    nextAction: "Select a region, then inspect Reporting visibility, Liquidity, and Payment friction with their own evidence limits.",
  });
  renderRegionalFootprint(regional);
}

function renderClosureCandidateTable(closures) {
  const table = get("#closure-candidate-table");
  const body = get("#closure-candidate-table-body");
  const empty = get("#closure-candidate-empty");
  const candidates = Array.isArray(closures.candidate_accounts) ? closures.candidate_accounts : [];
  body.replaceChildren();
  table.hidden = candidates.length === 0;
  empty.hidden = candidates.length > 0;
  if (candidates.length === 0) {
    setText(
      empty,
      currentSummary.scope.has_matches
        ? "No closure-validation candidates match the selected dimensions; no closure value is calculated."
        : "No matching accounts; no closure-validation candidate table is shown.",
    );
    return;
  }
  candidates.forEach((candidate) => {
    const row = make("tr");
    const account = appendTableCell(row, "th", candidate.account_id);
    account.scope = "row";
    appendTableCell(row, "td", `${candidate.entity_id} — ${candidate.entity_name}`);
    appendTableCell(row, "td", candidate.bank_name);
    appendTableCell(row, "td", candidate.currency);
    appendTableCell(row, "td", formatUsdCompact(candidate.annual_fee_usd), "numeric");
    appendTableCell(row, "td", CLOSURE_CANDIDATE_RULE);
    appendTableCell(row, "td", "Validation required · not approved", "closure-status");
    body.append(row);
  });
}

function clearVisualizationOutputs(message = "Data unavailable — validation did not complete.") {
  [
    "#visibility-source-bars",
    "#liquidity-waterfall",
    "#payment-cohort-stack",
    "#payment-cohort-legend",
    "#capacity-comparison-bars",
    "#liquidity-trend-table-body",
    "#closure-candidate-table-body",
    "#regional-map-markers",
    "#regional-evidence-table-body",
  ].forEach((selector) => {
    const node = get(selector);
    if (node) node.replaceChildren();
  });
  setCompositionRing("#visibility-ring", "#visibility-ring-value", null, "—", message);
  setCompositionRing("#payment-ring", "#payment-ring-value", null, "—", message);
  setText("#decision-visibility-chip", "Unavailable");
  setText("#decision-liquidity-chip", "Unavailable");
  setText("#decision-payments-chip", "Unavailable");
  setText("#regional-summary-context", "Unavailable");
  setText("#regional-selection-status", "No current result published.");
  setText("#trend-7-endpoint", "—");
  setText("#trend-14-endpoint", "—");
  const canvas = get("#liquidity-trend-canvas");
  if (canvas) {
    canvas.setAttribute("aria-label", message);
    const context = canvas.getContext("2d");
    if (context) context.clearRect(0, 0, canvas.width, canvas.height);
  }
  const closureTable = get("#closure-candidate-table");
  if (closureTable) closureTable.hidden = true;
  const regionalTable = get("#regional-evidence-table");
  if (regionalTable) regionalTable.hidden = true;
  getAll(".trend-data-disclosure").forEach((detail) => {
    detail.open = false;
  });
}

function renderGuardrails() {
  const capacity = dashboardData.guardrails.capacity;
  const closures = currentSummary.closures;
  const variance = (capacity.process_to_payment_ratio - 1) * 100;
  const capacityScope = "Enterprise-global management estimate · filters do not apply · not a combined capacity or P&L baseline";
  setText("#capacity-filter-note", capacityScope);
  setText(
    "#capacity-summary",
    `${capacity.process_file_exception_repair_hours_monthly.toFixed(1)} h/month vs ${capacity.payment_file_repair_hours_monthly.toFixed(1)} h/month · process estimate ${variance.toFixed(0)}% higher.`,
  );
  renderCapacityComparison(capacity);
  renderInlineDetail("capacity", {
    scope: capacityScope,
    evidence: "Management-estimated capacity is not observed labor, headcount, cashable savings, or a combined P&L baseline.",
    nextAction: "Reconcile observed labor scope and removability before booking capacity value.",
  });
  if (!currentSummary.scope.has_matches) {
    setText("#closure-summary", "No matching data for closure-validation candidates.");
  } else {
    setText(
      "#closure-summary",
      `${plural(closures.validation_candidates, "validation candidate")} · ${formatUsdCompact(closures.estimated_annual_fees_usd)} estimated annual fees · no approved closures.`,
    );
  }
  renderInlineDetail("closures", {
    scope: `30 Jun 2026 snapshot · date filter does not apply · currency/region/entity/bank filters apply · ${dimensionFilterContext(appliedFilters)} · ${plural(currentSummary.scope.account_count, "account")}`,
    evidence: currentSummary.scope.has_matches
      ? `${plural(closures.validation_candidates, "candidate")} in scope; local purpose, dependencies, signatories, continuity, closure cost, and fee removal remain unvalidated.`
      : "No matching accounts; no closure value is calculated.",
    nextAction: "Complete local account validation before approving a closure or booking fee removal.",
  });
  renderClosureCandidateTable(closures);
}

function evidenceSection(title, children, extraClass = "") {
  const section = make("section", `evidence-section ${extraClass}`.trim());
  section.append(make("h3", "", title));
  const nodes = Array.isArray(children) ? children : [children];
  nodes.filter(Boolean).forEach((child) => {
    section.append(child instanceof Node ? child : make("p", "", child));
  });
  return section;
}

function sourceList(files) {
  const list = make("ul", "source-list");
  files.forEach((file) => {
    const item = make("li", "source-row");
    item.append(make("strong", "", file));
    list.append(item);
  });
  return list;
}

function calculationContent(topic, definition) {
  const children = [make("p", "", definition.calculation)];
  if (topic === "gates") {
    children.push(
      make(
        "p",
        "formula",
        "Estimated monthly manual hours = frequency × minutes per instance × manual percentage ÷ 60.",
      ),
    );
  }
  children.push(make("p", "formula", definition.formula));
  return children;
}

function renderGuidePanel(topic, panel) {
  const definition = dashboardData.definitions[topic];
  const definitionContent = [
    make("p", "guide-topic-title", definition.title),
    make("p", "", definition.meaning),
  ];
  panel.append(
    evidenceSection("Definition", definitionContent),
    evidenceSection("Formula / calculation", calculationContent(topic, definition)),
    evidenceSection("Data source", sourceList(definition.sources)),
    evidenceSection("Method limit", definition.boundary, "boundary-section"),
  );
}

function renderDrawerPanel(topic) {
  const panel = get(`#panel-${topic}`);
  panel.replaceChildren();
  renderGuidePanel(topic, panel);
}

function selectDrawerTab(topic, { focusTab = false } = {}) {
  if (!dashboardData || !GUIDE_TOPICS.includes(topic)) return;
  state.drawerTab = topic;
  getAll('[role="tab"][data-tab]').forEach((tab) => {
    const selected = tab.dataset.tab === topic;
    tab.setAttribute("aria-selected", String(selected));
    tab.tabIndex = selected ? 0 : -1;
    if (selected && focusTab) tab.focus();
  });
  getAll('[role="tabpanel"]').forEach((panel) => {
    panel.hidden = panel.id !== `panel-${topic}`;
  });
  renderDrawerPanel(topic);
}

function openDrawer(topic, opener) {
  if (!dashboardData) return;
  closeSearch();
  closeFilterPanel({ restoreFocus: false });
  const dialog = get("#evidence-dialog");
  lastDrawerOpener = opener || document.activeElement;
  selectDrawerTab(topic);
  if (!dialog.open) dialog.showModal();
  get("#drawer-close").focus();
}

function closeDrawer() {
  const dialog = get("#evidence-dialog");
  if (dialog.open) dialog.close();
}

function appendOption(select, value, label) {
  const option = make("option", "", label);
  option.value = value;
  select.append(option);
}

function populateFilterControls() {
  const from = get("#filter-date-from");
  const to = get("#filter-date-to");
  for (const input of [from, to]) {
    input.min = dashboardData.meta.period_start;
    input.max = dashboardData.meta.period_end;
  }

  const currency = get("#filter-currency");
  currency.replaceChildren();
  appendOption(currency, "", "All currencies");
  filterOptions.currencies.forEach((value) => appendOption(currency, value, value));

  const region = get("#filter-region");
  region.replaceChildren();
  appendOption(region, "", "All regions");
  filterOptions.regions.forEach((value) => appendOption(region, value, value));

  const entity = get("#filter-entity");
  entity.replaceChildren();
  appendOption(entity, "", "All entities");
  filterOptions.entities.forEach((item) => appendOption(entity, item.value, `${item.value} — ${item.label}`));

  const bank = get("#filter-bank");
  bank.replaceChildren();
  appendOption(bank, "", "All banks");
  filterOptions.banks.forEach((value) => appendOption(bank, value, value));
}

function writeFilterForm(filters) {
  get("#filter-date-from").value = filters.dateFrom;
  get("#filter-date-to").value = filters.dateTo;
  get("#filter-currency").value = filters.currency;
  get("#filter-region").value = filters.region;
  get("#filter-entity").value = filters.entity;
  get("#filter-bank").value = filters.bank;
}

function readFilterForm() {
  return {
    dateFrom: get("#filter-date-from").value,
    dateTo: get("#filter-date-to").value,
    currency: get("#filter-currency").value,
    region: get("#filter-region").value,
    entity: get("#filter-entity").value,
    bank: get("#filter-bank").value,
  };
}

function clearFilterValidation() {
  get("#filter-validation").hidden = true;
  get("#filter-date-from").removeAttribute("aria-invalid");
  get("#filter-date-to").removeAttribute("aria-invalid");
}

function showFilterValidation(error) {
  const validation = get("#filter-validation");
  const isDateError = error && ["invalid_date", "invalid_date_range", "date_out_of_range"].includes(error.code);
  validation.textContent = isDateError
    ? "From date must be on or before To date and stay within 1 Jan–30 Jun 2026. The last valid view is unchanged."
    : "Filters could not be applied. The last valid view remains displayed.";
  validation.hidden = false;
  if (isDateError) {
    get("#filter-date-from").setAttribute("aria-invalid", "true");
    get("#filter-date-to").setAttribute("aria-invalid", "true");
  }
  announce(validation.textContent);
}

function openFilterPanel() {
  if (!dashboardData) return;
  closeSearch();
  const panel = get("#filter-panel");
  draftFilters = { ...appliedFilters };
  writeFilterForm(draftFilters);
  clearFilterValidation();
  get("#filter-empty-state").hidden = currentSummary.scope.has_matches;
  lastFilterOpener = get("#filter-trigger");
  panel.hidden = false;
  get("#filter-trigger").setAttribute("aria-expanded", "true");
  get("#filter-date-from").focus();
}

function closeFilterPanel({ restoreFocus = true } = {}) {
  const panel = get("#filter-panel");
  const wasOpen = panel && !panel.hidden;
  if (panel) panel.hidden = true;
  const trigger = get("#filter-trigger");
  if (trigger) trigger.setAttribute("aria-expanded", "false");
  if (appliedFilters) {
    draftFilters = { ...appliedFilters };
    if (dashboardData) writeFilterForm(draftFilters);
  }
  clearFilterValidation();
  if (wasOpen && restoreFocus && lastFilterOpener && document.contains(lastFilterOpener)) lastFilterOpener.focus();
  lastFilterOpener = null;
}

function applyFilterCandidate(candidate, { closePanel = true, message = "Filters applied." } = {}) {
  if (!dashboardData) return false;
  try {
    const validated = FilterModel.validateState(dashboardData, candidate);
    const summary = FilterModel.summarize(dashboardData, validated);
    appliedFilters = { ...validated };
    draftFilters = { ...validated };
    currentSummary = summary;
    clearFilterValidation();
    if (closePanel) closeFilterPanel();
    renderAll();
    const scopeMessage = summary.scope.has_matches
      ? `${plural(summary.scope.account_count, "account")} and ${plural(summary.payments.overall.records, "supplied payment record")} in scope.`
      : "No matching data. No percentage has been calculated.";
    announce(`${message} ${scopeMessage}`);
    return true;
  } catch (error) {
    showFilterValidation(error);
    return false;
  }
}

function removeAppliedFilter(key) {
  const candidate = { ...appliedFilters };
  if (key === "date") {
    candidate.dateFrom = defaultFilters.dateFrom;
    candidate.dateTo = defaultFilters.dateTo;
  } else if (Object.prototype.hasOwnProperty.call(candidate, key)) {
    candidate[key] = "";
  }
  applyFilterCandidate(candidate, { message: "Filter removed." });
}

function resetView({ shouldAnnounce = true } = {}) {
  if (!dashboardData) return;
  state.liquidityDays = DEFAULT_VIEW.liquidityDays;
  state.paymentMeasure = DEFAULT_VIEW.paymentMeasure;
  closeAllInlineDetails();
  getAll(".trend-data-disclosure").forEach((detail) => {
    detail.open = false;
  });
  clearSearch();
  closeFilterPanel({ restoreFocus: false });
  const validated = FilterModel.validateState(dashboardData, defaultFilters);
  appliedFilters = { ...validated };
  draftFilters = { ...validated };
  currentSummary = FilterModel.summarize(dashboardData, validated);
  writeFilterForm(draftFilters);
  renderAll();
  if (get("#evidence-dialog").open) renderDrawerPanel(state.drawerTab);
  if (shouldAnnounce) announce("Dashboard reset to all supplied data, 14-day liquidity, and payment records.");
}

function metricSearchDefinitions() {
  const inlineDefinitions = [
    ["decision", "Decision", "Expand the portfolio-wide decision and validation direction."],
    ["visibility", "Reporting visibility", "Expand the current filtered visibility result."],
    ["liquidity", "Liquidity screening", "Expand the current filtered 7- or 14-day screening result."],
    ["payments", "Payment friction", "Expand the current filtered payment-cohort result."],
    ["regions", "Regional footprint", "Expand the governed NA, EMEA, and APAC regional facet."],
    ["capacity", "Capacity evidence gate", "Expand the global capacity evidence gate."],
    ["closures", "Closure evidence gate", "Expand the current filtered closure candidates."],
  ].map(([topic, label, description]) => {
    const guideTopic = INLINE_GUIDE_TOPIC[topic];
    const definition = dashboardData.definitions[guideTopic];
    return {
      id: `inline:${topic}`,
      label,
      description,
      keywords: [definition.title, definition.meaning, ...definition.search_aliases].join(" "),
    };
  });
  const methodologyDefinitions = GUIDE_TOPICS.map((topic) => {
    const definition = dashboardData.definitions[topic];
    return {
      id: `guide:${topic}`,
      label: `${definition.title} — method and sources`,
      description: "Definition, formula/calculation, data source, and method limit.",
      keywords: [
        "definition formula calculation data source methodology method limit",
        definition.title,
        definition.calculation,
        definition.formula,
        definition.boundary,
        definition.sources.join(" "),
        definition.search_aliases.join(" "),
      ].join(" "),
    };
  });
  return inlineDefinitions.concat(methodologyDefinitions);
}

function closeSearch() {
  const results = get("#dashboard-search-results");
  const input = get("#dashboard-search");
  searchResults = [];
  activeSearchIndex = -1;
  if (results) {
    results.hidden = true;
    results.replaceChildren();
  }
  if (input) {
    input.setAttribute("aria-expanded", "false");
    input.removeAttribute("aria-activedescendant");
  }
}

function clearSearch() {
  const input = get("#dashboard-search");
  if (input) input.value = "";
  closeSearch();
  updateResetState();
}

function searchGroupLabel(kind) {
  if (kind === "metric") return "Metrics & methodology";
  if (kind === "account") return "Accounts";
  return "Filter values";
}

function normalizedSearchLabel(value) {
  return String(value ?? "")
    .normalize("NFKD")
    .toLocaleLowerCase("en-US")
    .trim()
    .replace(/\s+/gu, " ");
}

function orderSearchResultsForDisplay(results, query) {
  const normalizedQuery = normalizedSearchLabel(query);
  const exactDimensionMatch = results.some((entry) => (
    entry.kind === "dimension" && normalizedSearchLabel(entry.label) === normalizedQuery
  ));
  const kindOrder = exactDimensionMatch
    ? ["dimension", "metric", "account"]
    : ["metric", "dimension", "account"];
  return kindOrder.flatMap((kind) => results.filter((entry) => entry.kind === kind));
}

function setActiveSearchResult(index) {
  if (searchResults.length === 0) return;
  activeSearchIndex = (index + searchResults.length) % searchResults.length;
  const input = get("#dashboard-search");
  getAll(".search-result-option", get("#dashboard-search-results")).forEach((option) => {
    const selected = Number(option.dataset.searchIndex) === activeSearchIndex;
    option.setAttribute("aria-selected", String(selected));
    if (selected) {
      input.setAttribute("aria-activedescendant", option.id);
      option.scrollIntoView({ block: "nearest" });
    }
  });
}

function renderSearchResults(query) {
  const resultBox = get("#dashboard-search-results");
  resultBox.replaceChildren();
  activeSearchIndex = -1;
  const trimmed = query.trim();
  const exactCurrency = filterOptions.currencies.some((value) => value.toLocaleLowerCase("en-US") === trimmed.toLocaleLowerCase("en-US"));
  if (!trimmed || (trimmed.length < 2 && !exactCurrency)) {
    closeSearch();
    return;
  }

  searchResults = orderSearchResultsForDisplay(
    FilterModel.querySearchIndex(searchIndex, trimmed, { limit: SEARCH_RESULT_LIMIT }),
    trimmed,
  );
  resultBox.hidden = false;
  get("#dashboard-search").setAttribute("aria-expanded", "true");
  if (searchResults.length === 0) {
    const empty = make("p", "search-empty", "No dashboard items found. Try a metric, entity, bank, region, or currency.");
    resultBox.append(empty);
    return;
  }

  const kinds = [...new Set(searchResults.map((entry) => entry.kind))];
  kinds.forEach((kind) => {
    const entries = searchResults.filter((entry) => entry.kind === kind);
    if (entries.length === 0) return;
    const group = make("div", "search-result-group");
    group.setAttribute("role", "group");
    const heading = make("p", "search-result-heading", searchGroupLabel(kind));
    const headingId = `search-result-group-${kind}`;
    heading.id = headingId;
    group.setAttribute("aria-labelledby", headingId);
    group.append(heading);
    entries.forEach((entry) => {
      const index = searchResults.indexOf(entry);
      const option = make("button", "search-result-option");
      option.type = "button";
      option.id = `dashboard-search-option-${index}`;
      option.dataset.searchIndex = String(index);
      option.setAttribute("role", "option");
      option.setAttribute("aria-selected", "false");
      option.append(make("strong", "", entry.label), make("span", "", entry.description));
      option.addEventListener("click", () => chooseSearchResult(index));
      group.append(option);
    });
    resultBox.append(group);
  });
}

function chooseSearchResult(index) {
  const entry = searchResults[index];
  if (!entry) return;
  const searchInput = get("#dashboard-search");
  if (entry.kind === "metric") {
    clearSearch();
    if (entry.id.startsWith("inline:")) {
      openInlineDetail(entry.id.slice("inline:".length));
    } else if (entry.id.startsWith("guide:")) {
      const topic = entry.id.slice("guide:".length);
      openDrawer(GUIDE_TOPICS.includes(topic) ? topic : "overview", searchInput);
    }
    return;
  }

  const candidate = { ...appliedFilters };
  if (entry.kind === "dimension") {
    candidate[entry.values.dimension] = entry.values.value;
  } else if (entry.kind === "account") {
    candidate.currency = entry.values.currency;
    candidate.region = entry.values.region;
    candidate.entity = entry.values.entity_id;
    candidate.bank = entry.values.bank_name;
  }
  clearSearch();
  const applied = applyFilterCandidate(candidate, { message: `${entry.label} applied.` });
  if (applied) window.requestAnimationFrame(() => searchInput.focus());
}

function updateResetState() {
  const inlineDetailOpen = getAll("[data-inline-detail]").some((detail) => detail.open);
  const nestedDetailOpen = getAll(".trend-data-disclosure").some((detail) => detail.open);
  const viewIsDefault =
    state.liquidityDays === DEFAULT_VIEW.liquidityDays &&
    state.paymentMeasure === DEFAULT_VIEW.paymentMeasure &&
    (!appliedFilters || isDefaultFilterState(appliedFilters)) &&
    !(get("#dashboard-search") && get("#dashboard-search").value.trim()) &&
    !inlineDetailOpen &&
    !nestedDetailOpen;
  getAll("[data-reset]").forEach((button) => {
    button.disabled = !dashboardData || viewIsDefault;
  });
}

function bindEvents() {
  getAll("[data-open-drawer]").forEach((button) => {
    button.addEventListener("click", () => openDrawer(button.dataset.openDrawer, button));
  });
  getAll("[data-close-drawer]").forEach((button) => button.addEventListener("click", closeDrawer));
  getAll("[data-reset]").forEach((button) => button.addEventListener("click", () => resetView()));
  get("#regional-all-button").addEventListener("click", () => applyRegionalSelection("", "marker"));
  setupLiquidityTrendResizeHandling();

  const inlineDetails = getAll("[data-inline-detail]");
  const detailSummaries = getAll("[data-detail-summary]");
  inlineDetails.forEach((detail) => {
    detail.addEventListener("toggle", () => {
      if (detail.open) closeAllInlineDetails({ except: detail });
      if (detail.open && detail.dataset.inlineDetail === "liquidity") scheduleLiquidityTrendDraw();
      updateResetState();
    });
  });
  detailSummaries.forEach((summary, index) => {
    summary.addEventListener("keydown", (event) => {
      let nextIndex = null;
      if (event.key === "ArrowDown" || event.key === "ArrowRight") nextIndex = (index + 1) % detailSummaries.length;
      if (event.key === "ArrowUp" || event.key === "ArrowLeft") nextIndex = (index - 1 + detailSummaries.length) % detailSummaries.length;
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = detailSummaries.length - 1;
      if (nextIndex !== null) {
        event.preventDefault();
        detailSummaries[nextIndex].focus();
      }
      if (event.key === "Escape") {
        const detail = summary.closest("details");
        if (detail && detail.open) {
          event.preventDefault();
          event.stopPropagation();
          detail.open = false;
          summary.focus();
        }
      }
    });
  });
  getAll(".trend-data-disclosure").forEach((detail) => {
    const summary = detail.querySelector("summary");
    detail.addEventListener("toggle", updateResetState);
    if (!summary) return;
    summary.addEventListener("keydown", (event) => {
      if (event.key !== "Escape" || !detail.open) return;
      event.preventDefault();
      event.stopPropagation();
      detail.open = false;
      summary.focus();
    });
  });

  getAll('input[name="liquidity-days"]').forEach((input) => {
    input.addEventListener("change", () => {
      if (!dashboardData || !input.checked) return;
      state.liquidityDays = Number(input.value);
      renderLiquidity({ shouldAnnounce: true });
    });
  });
  getAll('input[name="payment-measure"]').forEach((input) => {
    input.addEventListener("change", () => {
      if (!dashboardData || !input.checked) return;
      state.paymentMeasure = input.value;
      renderPayments({ shouldAnnounce: true });
    });
  });

  getAll('[role="tab"][data-tab]').forEach((tab) => {
    tab.addEventListener("click", () => selectDrawerTab(tab.dataset.tab));
    tab.addEventListener("keydown", (event) => {
      const tabs = getAll('[role="tab"][data-tab]');
      const index = tabs.indexOf(tab);
      let next = null;
      if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
      if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      if (next !== null) {
        event.preventDefault();
        selectDrawerTab(tabs[next].dataset.tab, { focusTab: true });
      }
    });
  });

  const filterTrigger = get("#filter-trigger");
  filterTrigger.addEventListener("click", () => {
    if (get("#filter-panel").hidden) openFilterPanel();
    else closeFilterPanel();
  });
  getAll("[data-close-filters]").forEach((button) => {
    button.addEventListener("click", () => closeFilterPanel());
  });
  getAll("[data-clear-filters]").forEach((button) => {
    button.addEventListener("click", () => {
      if (!dashboardData) return;
      if (button.dataset.clearFilters === "draft") {
        draftFilters = { ...defaultFilters };
        writeFilterForm(draftFilters);
        clearFilterValidation();
        get("#filter-empty-state").hidden = true;
        announce("Filter draft cleared. Select Apply filters to update the dashboard.");
      } else {
        applyFilterCandidate(defaultFilters, { message: "All filters cleared." });
      }
    });
  });
  get("#filter-form").addEventListener("input", () => {
    draftFilters = readFilterForm();
    clearFilterValidation();
    get("#filter-empty-state").hidden = true;
  });
  get("#filter-form").addEventListener("submit", (event) => {
    event.preventDefault();
    draftFilters = readFilterForm();
    applyFilterCandidate(draftFilters, { message: "Filters applied." });
  });

  const searchInput = get("#dashboard-search");
  searchInput.addEventListener("input", () => {
    renderSearchResults(searchInput.value);
    updateResetState();
  });
  searchInput.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      if (get("#dashboard-search-results").hidden) renderSearchResults(searchInput.value);
      if (searchResults.length) setActiveSearchResult(activeSearchIndex + 1);
    }
    if (event.key === "ArrowUp") {
      event.preventDefault();
      if (searchResults.length) setActiveSearchResult(activeSearchIndex <= 0 ? searchResults.length - 1 : activeSearchIndex - 1);
    }
    if (event.key === "Enter" && activeSearchIndex >= 0) {
      event.preventDefault();
      chooseSearchResult(activeSearchIndex);
    }
    if (event.key === "Escape" && !get("#dashboard-search-results").hidden) {
      event.preventDefault();
      closeSearch();
    }
  });

  document.addEventListener("pointerdown", (event) => {
    const filterToolbar = get(".filter-toolbar");
    if (!get("#filter-panel").hidden && !filterToolbar.contains(event.target)) {
      closeFilterPanel({ restoreFocus: false });
    }
    const searchShell = get("#dashboard-search-shell");
    if (!get("#dashboard-search-results").hidden && !searchShell.contains(event.target)) closeSearch();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !get("#filter-panel").hidden) {
      event.preventDefault();
      closeFilterPanel();
    }
  });

  get("#evidence-dialog").addEventListener("close", () => {
    if (lastDrawerOpener && document.contains(lastDrawerOpener)) lastDrawerOpener.focus();
    lastDrawerOpener = null;
  });
}

function renderAll() {
  renderHeader();
  renderFilterChrome();
  renderVisibility();
  renderLiquidity();
  renderPayments();
  renderRegions();
  renderGuardrails();
  if (get("#evidence-dialog").open) renderDrawerPanel(state.drawerTab);
  updateResetState();
}

async function initializeDashboard() {
  bindEvents();
  setDataControlsDisabled(true);
  try {
    const response = await fetch("dashboard_data.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`Dashboard data request failed: ${response.status}`);
    const data = await response.json();
    assertDashboardData(data);
    dashboardData = data;
    defaultFilters = FilterModel.createDefaultState(data);
    appliedFilters = FilterModel.validateState(data, defaultFilters);
    draftFilters = { ...appliedFilters };
    filterOptions = FilterModel.getFilterOptions(data);
    currentSummary = FilterModel.summarize(data, appliedFilters);
    searchIndex = FilterModel.buildSearchIndex(data, metricSearchDefinitions());
    populateFilterControls();
    writeFilterForm(draftFilters);
    renderAll();
    setDataControlsDisabled(false);
    updateResetState();
    get("#dashboard-shell").setAttribute("aria-busy", "false");
  } catch (error) {
    console.error("Dashboard unavailable", error);
    showDataFailure();
  }
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = Object.freeze({
    formatUsdCompact,
    waterfallBarGeometry,
    liquidityTrendValue,
    lastFiniteTrendValue,
    paymentCohortVisualRows,
    visibilityActionText,
    regionalMarkerSize,
    regionalDelayedText,
    regionalPaymentText,
    orderSearchResultsForDisplay,
  });
}

if (typeof window !== "undefined" && typeof document !== "undefined") initializeDashboard();
