"use strict";

const FilterModel = window.NorthstarFilterModel;

const DEFAULT_VIEW = Object.freeze({
  liquidityDays: 14,
  paymentMeasure: "records",
  drawerTab: "overview",
});

const PAYMENT_MEASURES = Object.freeze({
  records: {
    valueKey: "records",
    shareKey: "record_share_pct",
    label: "records",
    headline: "of matching records in the priority union",
  },
  exceptions: {
    valueKey: "exceptions",
    shareKey: "exception_share_pct",
    label: "exceptions",
    headline: "of matching exceptions in the priority union",
  },
  repair_minutes: {
    valueKey: "repair_minutes",
    shareKey: "repair_share_pct",
    label: "repair minutes",
    headline: "of matching repair effort in the priority union",
  },
});

const GUIDE_TOPICS = Object.freeze(["overview", "visibility", "liquidity", "payments", "gates"]);
const SEARCH_RESULT_LIMIT = 8;

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

function formatUsdMillions(value) {
  if (!isFiniteNumber(value)) return "—";
  const absolute = Math.abs(value) / 1_000_000;
  const sign = value < 0 ? "−" : "";
  return `${sign}$${absolute.toFixed(2)}m`;
}

function formatUsdCompact(value) {
  if (!isFiniteNumber(value)) return "—";
  const sign = value < 0 ? "−" : "";
  const absolute = Math.abs(value);
  if (absolute >= 1_000_000) return `${sign}$${(absolute / 1_000_000).toFixed(2)}m`;
  if (absolute >= 1_000) return `${sign}$${formatNumber(absolute / 1_000, 1)}k`;
  return `${sign}$${formatNumber(absolute, 0)}`;
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
  closeSearch();
  closeFilterPanel({ restoreFocus: false });
  setText("#dashboard-scope", "Week 1–2 diagnostic snapshot · supplied data unavailable");
  setText("#data-status", "Unavailable — validation failed");
  ["#visibility-kpi", "#funded-case-value", "#payment-kpi"].forEach((selector) => setText(selector, "Unavailable"));
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
}

function renderFilterChrome() {
  const descriptors = activeFilterDescriptors(appliedFilters);
  const count = descriptors.length;
  const countNode = get("#filter-count");
  countNode.hidden = count === 0;
  countNode.textContent = String(count);
  countNode.setAttribute("aria-label", `${count} active ${count === 1 ? "filter" : "filters"}`);
  setText("#filter-scope-summary", currentScopeText());
  setText("#guide-scope-summary", currentScopeText());
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
    get("#same-day-segment").style.width = "0%";
    get("#delayed-segment").style.width = "0%";
    setText("#visibility-interpretation", "No account-day evidence matches the selected scope.");
  } else {
    const sameDayShare = (visibility.same_day_accounts / visibility.accounts_total) * 100;
    const delayedShare = 100 - sameDayShare;
    setText("#visibility-kpi", `${visibility.delayed_accounts} / ${visibility.accounts_total}`);
    setText("#same-day-label", `${visibility.same_day_accounts} same-day`);
    setText("#delayed-label", `${visibility.delayed_accounts} delayed`);
    get("#same-day-segment").style.width = `${sameDayShare}%`;
    get("#delayed-segment").style.width = `${delayedShare}%`;
    setText(
      "#visibility-interpretation",
      `${plural(visibility.delayed_accounts, "selected account")} show at least one calendar-date reporting delay.`,
    );
  }
  setText("#visibility-boundary", "Reporting-date proxy—not start-of-day or elapsed-24-hour performance.");
}

function liquidityScenario(days) {
  return currentSummary.liquidity.scenarios[String(days)];
}

function liquidityScenarioAvailable(days) {
  const scenario = liquidityScenario(days);
  return Boolean(currentSummary.scope.has_matches && scenario && isFiniteNumber(scenario.screen_usd));
}

function renderLiquidity({ shouldAnnounce = false } = {}) {
  const liquidity = currentSummary.liquidity;
  const selected = liquidityScenario(state.liquidityDays);
  const selectedAvailable = liquidityScenarioAvailable(state.liquidityDays);

  setText("#funded-case-value", dashboardData.liquidity.funded_case.display);
  setText("#mobility-status", "Validated mobility: not established by supplied data.");
  setText("#screen-7-value", liquidityScenarioAvailable(7) ? formatUsdMillions(liquidityScenario(7).screen_usd) : "—");
  setText("#screen-14-value", liquidityScenarioAvailable(14) ? formatUsdMillions(liquidityScenario(14).screen_usd) : "—");

  if (selectedAvailable) {
    setText(
      "#liquidity-interpretation",
      `${formatUsdMillions(selected.screen_usd)} is the selected ${state.liquidityDays}-day modeled screen as of ${formatIsoDate(liquidity.as_of_date)}.`,
    );
    setText(
      "#liquidity-boundary",
      `${formatUsdMillions(selected.screen_usd)} is a ${state.liquidityDays}-day screening sensitivity—not surplus cash or transfer authorization.`,
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
  if (get("#evidence-dialog").open && state.drawerTab === "liquidity") renderDrawerPanel("liquidity");
  updateResetState();

  if (shouldAnnounce) {
    const result = selectedAvailable
      ? `Screening result ${formatUsdMillions(selected.screen_usd)}.`
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

function renderPayments({ shouldAnnounce = false } = {}) {
  const { config, unionValue, totalValue, share } = paymentMeasureData();
  const overlap = currentSummary.payments.cohorts["Manual touch + cross-border wire"];
  const hasComparableMeasure = totalValue > 0 && isFiniteNumber(share);
  setKpiEmpty("#payment-kpi", !hasComparableMeasure);

  if (hasComparableMeasure) {
    setText("#payment-kpi", formatPercent(share));
    setText("#payment-kpi-label", config.headline);
    get("#payment-union-bar").style.width = `${share}%`;
    setText(
      "#payment-union-label",
      `${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label} · ${formatPercent(share)}`,
    );
  } else {
    setText("#payment-kpi", "—");
    setText("#payment-kpi-label", "No matching data for the selected measure");
    get("#payment-union-bar").style.width = "0%";
    setText("#payment-union-label", `No matching ${config.label}; no percentage is calculated.`);
  }

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
  if (get("#evidence-dialog").open && state.drawerTab === "payments") renderDrawerPanel("payments");
  updateResetState();

  if (shouldAnnounce) {
    const message = hasComparableMeasure
      ? `Priority union contains ${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label}, ${formatPercent(share)}.`
      : `No matching ${config.label}; no percentage is calculated.`;
    announce(`${config.label} selected. ${message}`);
  }
}

function renderGuardrails() {
  const capacity = dashboardData.guardrails.capacity;
  const closures = currentSummary.closures;
  const variance = (capacity.process_to_payment_ratio - 1) * 100;
  setText("#capacity-filter-note", "Global baseline · filters do not apply");
  setText(
    "#capacity-summary",
    `${capacity.process_file_exception_repair_hours_monthly.toFixed(2)} h process estimate is ${variance.toFixed(0)}% above the ${capacity.payment_file_repair_hours_monthly.toFixed(2)} h payment-file estimate.`,
  );
  if (!currentSummary.scope.has_matches) {
    setText("#closure-summary", "No matching data for closure-validation candidates.");
  } else {
    setText(
      "#closure-summary",
      `${plural(closures.validation_candidates, "validation candidate")} · ${formatUsdCompact(closures.estimated_annual_fees_usd)} estimated annual fees · no approved closures.`,
    );
  }
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

function metricList(rows) {
  const list = make("ul", "metric-list");
  rows.forEach(([label, value]) => {
    const item = make("li", "metric-row");
    item.append(make("span", "", label), make("strong", "", value));
    list.append(item);
  });
  return list;
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

function topicValues(topic) {
  if (topic === "overview") {
    const hasMatches = currentSummary.scope.has_matches;
    return [
      ["Current scope", filterContext(appliedFilters)],
      ["Accounts", hasMatches ? formatNumber(currentSummary.scope.account_count) : "—"],
      ["Supplied payment records", hasMatches ? formatNumber(currentSummary.payments.overall.records) : "—"],
      ["Decision", "Portfolio-wide; unchanged by filters"],
    ];
  }
  if (topic === "visibility") {
    const visibility = currentSummary.visibility;
    const hasVisibility = visibility.accounts_total > 0;
    return [
      ["Selected accounts", hasVisibility ? formatNumber(visibility.accounts_total) : "—"],
      ["Delayed accounts", hasVisibility ? formatNumber(visibility.delayed_accounts) : "—"],
      ["Account-days", hasVisibility ? formatNumber(visibility.observations) : "—"],
      ["Same-day account-day rate", formatPercent(visibility.same_day_rate_pct)],
    ];
  }
  if (topic === "liquidity") {
    const liquidity = currentSummary.liquidity;
    const scenario = liquidityScenario(state.liquidityDays);
    return [
      ["As-of date", formatIsoDate(liquidity.as_of_date)],
      ["Selected accounts", currentSummary.scope.has_matches ? formatNumber(currentSummary.scope.account_count) : "—"],
      ["Gross positive estimated availability", formatUsdMillions(liquidity.positive_available_usd)],
      ["Preliminary restrictions", formatUsdMillions(liquidity.restricted_positive_available_usd)],
      ["Negative positions", formatUsdMillions(liquidity.negative_available_usd)],
      [`${state.liquidityDays}-day illustrative buffer`, formatUsdMillions(scenario.buffer_usd)],
      [`${state.liquidityDays}-day screening result`, formatUsdMillions(scenario.screen_usd)],
      ["Validated mobility", "Not established"],
      ["Funded case", dashboardData.liquidity.funded_case.display],
    ];
  }
  if (topic === "payments") {
    const { config, unionValue, totalValue, share } = paymentMeasureData();
    const hasComparableMeasure = totalValue > 0 && isFiniteNumber(share);
    return [
      ["Selected measure", config.label],
      ["Priority union", hasComparableMeasure ? formatNumber(unionValue) : "—"],
      ["Matching total", hasComparableMeasure ? formatNumber(totalValue) : "—"],
      ["Priority share", formatPercent(share)],
      ["Matching supplied records", currentSummary.payments.overall.records > 0 ? formatNumber(currentSummary.payments.overall.records) : "—"],
    ];
  }
  const capacity = dashboardData.guardrails.capacity;
  const closures = currentSummary.closures;
  return [
    ["Capacity scope", "Global baseline · filters do not apply"],
    ["Estimated manual process capacity", `${capacity.total_estimated_manual_hours_monthly.toFixed(2)} h/month`],
    ["Closure-validation candidates", currentSummary.scope.has_matches ? formatNumber(closures.validation_candidates) : "—"],
    ["Estimated candidate fees", currentSummary.scope.has_matches ? `${formatUsdCompact(closures.estimated_annual_fees_usd)} annually` : "—"],
    ["Approved closures", "0"],
  ];
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
    make("p", "metric-context", `Current scope: ${currentScopeText()}`),
    metricList(topicValues(topic)),
  ];
  panel.append(
    evidenceSection("Definition", definitionContent),
    evidenceSection("Calculation", calculationContent(topic, definition)),
    evidenceSection("Data source", sourceList(definition.sources)),
    evidenceSection("Interpretation limit", definition.boundary, "boundary-section"),
    evidenceSection("Next action", definition.next_action, "action-section"),
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
  return GUIDE_TOPICS.map((topic) => {
    const definition = dashboardData.definitions[topic];
    return {
      id: topic,
      label: definition.title,
      description: definition.meaning,
      keywords: definition.search_aliases.join(" "),
    };
  });
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
  if (kind === "metric") return "Metrics";
  if (kind === "account") return "Accounts";
  return "Filter values";
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

  searchResults = FilterModel.querySearchIndex(searchIndex, trimmed, { limit: SEARCH_RESULT_LIMIT });
  resultBox.hidden = false;
  get("#dashboard-search").setAttribute("aria-expanded", "true");
  if (searchResults.length === 0) {
    const empty = make("p", "search-empty", "No dashboard items found. Try a metric, entity, bank, region, or currency.");
    resultBox.append(empty);
    return;
  }

  const kinds = ["metric", "dimension", "account"];
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
    openDrawer(GUIDE_TOPICS.includes(entry.id) ? entry.id : "overview", searchInput);
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
  applyFilterCandidate(candidate, { message: `${entry.label} applied.` });
}

function updateResetState() {
  const viewIsDefault =
    state.liquidityDays === DEFAULT_VIEW.liquidityDays &&
    state.paymentMeasure === DEFAULT_VIEW.paymentMeasure &&
    (!appliedFilters || isDefaultFilterState(appliedFilters)) &&
    !(get("#dashboard-search") && get("#dashboard-search").value.trim());
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

initializeDashboard();
