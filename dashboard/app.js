"use strict";

const DEFAULT_STATE = Object.freeze({
  liquidityDays: 14,
  paymentMeasure: "records",
  visibilitySource: "all",
  drawerTab: "overview",
});

const PAYMENT_MEASURES = Object.freeze({
  records: {
    valueKey: "records",
    shareKey: "record_contribution_pct",
    label: "records",
    headline: "of supplied records in the priority union",
  },
  exceptions: {
    valueKey: "exceptions",
    shareKey: "exception_contribution_pct",
    label: "exceptions",
    headline: "of exceptions in the priority union",
  },
  repair_minutes: {
    valueKey: "repair_minutes",
    shareKey: "repair_contribution_pct",
    label: "repair minutes",
    headline: "of repair effort in the priority union",
  },
});

const state = { ...DEFAULT_STATE };
let dashboardData = null;
let lastDrawerOpener = null;

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

function formatNumber(value, maximumFractionDigits = 0) {
  return new Intl.NumberFormat("en-US", { maximumFractionDigits }).format(value);
}

function formatPercent(value) {
  return `${formatNumber(value, 2)}%`;
}

function formatUsdMillions(value) {
  const absolute = Math.abs(value) / 1_000_000;
  const sign = value < 0 ? "−" : "";
  return `${sign}$${absolute.toFixed(2)}m`;
}

function formatUsdCompact(value) {
  if (Math.abs(value) >= 1_000_000) return formatUsdMillions(value);
  if (Math.abs(value) >= 1_000) return `$${formatNumber(value / 1_000, 1)}k`;
  return `$${formatNumber(value, 0)}`;
}

function sourceId(method) {
  return method.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "");
}

function assertDashboardData(data) {
  const required = ["meta", "decision", "visibility", "liquidity", "payments", "guardrails", "sources"];
  for (const key of required) {
    if (!data || typeof data[key] !== "object") throw new Error(`Missing dashboard contract: ${key}`);
  }
  if (data.schema_version !== "1.0") throw new Error("Unsupported dashboard schema");
  if (data.liquidity.validated_mobility.value_usd !== null) {
    throw new Error("Validated mobility must remain not established");
  }
  if (data.liquidity.validated_mobility.status !== "not_established") {
    throw new Error("Validated mobility status is not fail-closed");
  }
  if (!data.liquidity.scenarios["7"] || !data.liquidity.scenarios["14"]) {
    throw new Error("Liquidity scenarios are incomplete");
  }
  if (Object.keys(data.payments.cohorts).length !== 4) {
    throw new Error("Payment cohort partition is incomplete");
  }
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

function showDataFailure() {
  dashboardData = null;
  document.body.classList.add("data-unavailable");
  get("#data-error").hidden = false;
  setDataControlsDisabled(true);
  setText("#dashboard-scope", "Week 1–2 diagnostic snapshot · supplied data unavailable");
  setText("#data-status", "Unavailable — validation failed");
  ["#visibility-kpi", "#funded-case-value", "#payment-kpi"].forEach((selector) => setText(selector, "Unavailable"));
  setText("#mobility-status", "No current result published.");
  setText("#liquidity-boundary", "Data unavailable — validation did not complete.");
  setText("#payment-boundary", "Data unavailable — validation did not complete.");
  get("#dashboard-shell").setAttribute("aria-busy", "false");
}

function renderHeader() {
  setText(
    "#dashboard-scope",
    "Week 1–2 diagnostic snapshot · 1 Jan–30 Jun 2026 · supplied data, not live operations",
  );
  setText("#data-status", "Reconciled to supplied controls · source certification open");
  setText("#decision-title", dashboardData.decision.headline);
  setText("#decision-support", dashboardData.decision.next_step);
}

function renderVisibility() {
  const visibility = dashboardData.visibility;
  const sameDayShare = (visibility.same_day_accounts / visibility.accounts_total) * 100;
  const delayedShare = 100 - sameDayShare;

  setText("#visibility-kpi", `${visibility.delayed_accounts} / ${visibility.accounts_total}`);
  setText("#same-day-label", `${visibility.same_day_accounts} same-day`);
  setText("#delayed-label", `${visibility.delayed_accounts} delayed`);
  get("#same-day-segment").style.width = `${sameDayShare}%`;
  get("#delayed-segment").style.width = `${delayedShare}%`;
  setText(
    "#visibility-interpretation",
    `All ${visibility.delayed_accounts} delayed accounts use portal or spreadsheet reporting.`,
  );
  setText(
    "#visibility-boundary",
    "Reporting-date proxy—not start-of-day or elapsed-24-hour performance.",
  );
}

function renderLiquidity({ shouldAnnounce = false } = {}) {
  const liquidity = dashboardData.liquidity;
  const scenario = liquidity.scenarios[String(state.liquidityDays)];

  setText("#funded-case-value", liquidity.funded_case.display);
  setText(
    "#mobility-status",
    "Validated mobility: not established by supplied data.",
  );
  setText("#screen-7-value", formatUsdMillions(liquidity.scenarios["7"].screen_usd));
  setText("#screen-14-value", formatUsdMillions(liquidity.scenarios["14"].screen_usd));
  setText(
    "#liquidity-interpretation",
    `${formatUsdMillions(scenario.screen_usd)} is the selected ${state.liquidityDays}-day modeled screen.`,
  );
  setText(
    "#liquidity-boundary",
    `${formatUsdMillions(scenario.screen_usd)} is a ${state.liquidityDays}-day screening sensitivity—not surplus cash or transfer authorization.`,
  );
  getAll('input[name="liquidity-days"]').forEach((input) => {
    input.checked = Number(input.value) === state.liquidityDays;
  });

  if (get("#evidence-dialog").open && state.drawerTab === "liquidity") {
    renderDrawerPanel("liquidity");
  }
  updateResetState();
  if (shouldAnnounce) {
    announce(
      `${state.liquidityDays}-day screen selected. Screening result ${formatUsdMillions(scenario.screen_usd)}. Validated mobility remains not established; funded case stays at ${liquidity.funded_case.display}.`,
    );
  }
}

function paymentMeasureData() {
  const config = PAYMENT_MEASURES[state.paymentMeasure];
  const union = dashboardData.payments.priority_union;
  const overall = dashboardData.payments.overall;
  return {
    config,
    unionValue: union[config.valueKey],
    totalValue: overall[config.valueKey],
    share: union[config.shareKey],
  };
}

function renderPayments({ shouldAnnounce = false } = {}) {
  const { config, unionValue, totalValue, share } = paymentMeasureData();
  const overlap = dashboardData.payments.cohorts.manual_touch_and_cross_border_wire;

  setText("#payment-kpi", formatPercent(share));
  setText("#payment-kpi-label", config.headline);
  get("#payment-union-bar").style.width = `${share}%`;
  setText(
    "#payment-union-label",
    `${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label} · ${formatPercent(share)}`,
  );
  setText("#payment-overlap", `${formatNumber(overlap.records)} overlap records are counted once.`);
  setText(
    "#payment-boundary",
    `Within ${formatNumber(dashboardData.payments.overall.records)} supplied records only; association, not causation.`,
  );
  getAll('input[name="payment-measure"]').forEach((input) => {
    input.checked = input.value === state.paymentMeasure;
  });

  if (get("#evidence-dialog").open && state.drawerTab === "payments") {
    renderDrawerPanel("payments");
  }
  updateResetState();
  if (shouldAnnounce) {
    announce(
      `${config.label} selected. Priority union contains ${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label}, ${formatPercent(share)}.`,
    );
  }
}

function renderGuardrails() {
  const capacity = dashboardData.guardrails.capacity;
  const closures = dashboardData.guardrails.closures;
  const variance = (capacity.process_to_payment_ratio - 1) * 100;
  setText(
    "#capacity-summary",
    `${capacity.process_file_exception_repair_hours_monthly.toFixed(2)} h process estimate is ${variance.toFixed(0)}% above the ${capacity.payment_file_repair_hours_monthly.toFixed(2)} h payment-file estimate.`,
  );
  setText(
    "#closure-summary",
    `${closures.validation_candidates} validation candidates · ${formatUsdCompact(closures.estimated_annual_fees_usd)} estimated annual fees · no approved closures.`,
  );
}

function updateResetState() {
  const isDefault =
    state.liquidityDays === DEFAULT_STATE.liquidityDays &&
    state.paymentMeasure === DEFAULT_STATE.paymentMeasure &&
    state.visibilitySource === DEFAULT_STATE.visibilitySource;
  getAll("[data-reset]").forEach((button) => {
    button.disabled = !dashboardData || isDefault;
  });
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

function sourceFilesFor(...roles) {
  return dashboardData.sources
    .filter((source) => roles.includes(source.role))
    .map((source) => source.file)
    .join(" · ");
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

function renderOverviewPanel(panel) {
  panel.append(
    evidenceSection("What this means", [
      make("p", "", dashboardData.decision.headline),
      make("p", "", dashboardData.decision.next_step),
    ]),
    evidenceSection("Evidence", metricList([
      ["Period", "1 Jan–30 Jun 2026"],
      ["Data status", "Reconciled to supplied controls"],
      ["Certification", "Source certification open"],
    ])),
    evidenceSection(
      "Decision boundary",
      "This is supplied diagnostic evidence, not live operations, funding authority, or execution approval.",
      "boundary-section",
    ),
    evidenceSection(
      "Next action",
      "Use the three signal tabs to inspect the evidence and validation required before advancing.",
      "action-section",
    ),
    evidenceSection(
      "Definition & source",
      make("p", "source-files", sourceFilesFor("w1_checks", "w2_reconciliation")),
    ),
  );
}

function renderVisibilityPanel(panel) {
  const visibility = dashboardData.visibility;
  const selector = make("div", "source-selector");
  const choices = [{ id: "all", method: "All sources" }].concat(
    visibility.sources.map((source) => ({ id: sourceId(source.method), method: source.method })),
  );
  choices.forEach((choice) => {
    const button = make("button", "source-chip", choice.method);
    button.type = "button";
    button.dataset.source = choice.id;
    button.setAttribute("aria-pressed", String(state.visibilitySource === choice.id));
    button.addEventListener("click", () => {
      state.visibilitySource = choice.id;
      renderDrawerPanel("visibility");
      updateResetState();
      announce(`${choice.method} visibility evidence selected.`);
    });
    selector.append(button);
  });

  const evidence = make("div");
  evidence.append(selector);
  if (state.visibilitySource === "all") {
    const list = make("ul", "source-list");
    visibility.sources.forEach((source) => {
      const delayed = source.same_day_rate_pct === 100 ? "same-day" : `up to ${source.maximum_delay_days} day${source.maximum_delay_days === 1 ? "" : "s"} late`;
      const row = make("li", "source-row");
      row.append(
        make("strong", "", `${source.method} · ${source.accounts} accounts`),
        make("span", "", `${formatNumber(source.observations)} account-days · ${delayed}`),
      );
      list.append(row);
    });
    evidence.append(list);
  } else {
    const source = visibility.sources.find((row) => sourceId(row.method) === state.visibilitySource);
    evidence.append(metricList([
      ["Reporting source", source.method],
      ["Accounts", formatNumber(source.accounts)],
      ["Account-days", formatNumber(source.observations)],
      ["Same-day rate", formatPercent(source.same_day_rate_pct)],
      ["Maximum reporting delay", `${source.maximum_delay_days} calendar day${source.maximum_delay_days === 1 ? "" : "s"}`],
    ]));
  }

  panel.append(
    evidenceSection(
      "What this means",
      `All ${visibility.delayed_accounts} delayed accounts use portal or spreadsheet reporting; the global denominator remains ${visibility.accounts_total} accounts.`,
    ),
    evidenceSection("Evidence", evidence),
    evidenceSection(
      "Decision boundary",
      "Reporting-date proxy—not start-of-day or elapsed-24-hour performance.",
      "boundary-section",
    ),
    evidenceSection(
      "Next action",
      "Validate timestamps, cutoff, reporting source, and ownership; pilot the highest-exposure portal and spreadsheet accounts.",
      "action-section",
    ),
    evidenceSection(
      "Definition & source",
      [
        make("p", "", visibility.evidence_label),
        make("p", "source-files", sourceFilesFor("visibility")),
      ],
    ),
  );
}

function renderLiquidityPanel(panel) {
  const liquidity = dashboardData.liquidity;
  const scenario = liquidity.scenarios[String(state.liquidityDays)];
  const ladder = metricList(
    liquidity.evidence_ladder.map((row) => [row.label, formatUsdMillions(row.value_usd)]),
  );
  const table = make("table", "threshold-table");
  const head = make("thead");
  const headRow = make("tr");
  ["Threshold", "Modeled level", "Windows met", "Rate"].forEach((label) => headRow.append(make("th", "", label)));
  head.append(headRow);
  const body = make("tbody");
  ["stress", "base", "upside"].forEach((key) => {
    const threshold = scenario.thresholds[key];
    const row = make("tr");
    row.append(
      make("td", "", key[0].toUpperCase() + key.slice(1)),
      make("td", "", formatUsdMillions(threshold.threshold_usd)),
      make("td", "", `${threshold.windows_met}/${threshold.complete_windows}`),
      make("td", "", formatPercent(threshold.met_rate_pct)),
    );
    body.append(row);
  });
  table.append(head, body);

  const evidence = make("div");
  evidence.append(
    ladder,
    metricList([
      [`${state.liquidityDays}-day illustrative payment-intent buffer`, formatUsdMillions(scenario.buffer_usd)],
      [`${state.liquidityDays}-day net screening result`, formatUsdMillions(scenario.screen_usd)],
      ["Validated mobility", "Not established"],
      ["Funded case", liquidity.funded_case.display],
    ]),
    table,
  );

  panel.append(
    evidenceSection(
      "What this means",
      `${formatUsdMillions(scenario.screen_usd)} passes a ${state.liquidityDays}-day screen; it does not establish movable cash.`,
    ),
    evidenceSection("Evidence", evidence),
    evidenceSection(
      "Decision boundary",
      `${formatUsdMillions(scenario.screen_usd)} is a screening sensitivity—not surplus cash, a forecast, an approved buffer, or transfer authorization.`,
      "boundary-section",
    ),
    evidenceSection(
      "Next action",
      "Certify restrictions, transferability, operating buffers, timing, and funding economics account by account.",
      "action-section",
    ),
    evidenceSection(
      "Definition & source",
      [
        make("p", "", liquidity.evidence_label),
        make("p", "source-files", sourceFilesFor("liquidity_scenarios", "liquidity_thresholds")),
      ],
    ),
  );
}

function renderPaymentsPanel(panel) {
  const payments = dashboardData.payments;
  const { config, unionValue, totalValue, share } = paymentMeasureData();
  const cohortList = make("ol", "cohort-list");

  Object.values(payments.cohorts).forEach((cohort) => {
    const value = cohort[config.valueKey];
    const contribution = cohort[config.shareKey];
    const row = make("li", "cohort-row");
    row.append(
      make("strong", "", cohort.label),
      make("span", "", `${formatNumber(value)} ${config.label} · ${formatPercent(contribution)} of supplied total`),
    );
    const track = make("div", "cohort-track");
    const fill = make("div", "cohort-fill");
    fill.style.width = `${contribution}%`;
    track.append(fill);
    row.append(track);
    cohortList.append(row);
  });

  panel.append(
    evidenceSection(
      "What this means",
      `The deduplicated priority union contains ${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label}, or ${formatPercent(share)}.`,
    ),
    evidenceSection("Evidence", [
      cohortList,
      make("p", "", `${formatNumber(payments.cohorts.manual_touch_and_cross_border_wire.records)} overlap records are counted once.`),
    ]),
    evidenceSection(
      "Decision boundary",
      `Within ${formatNumber(payments.overall.records)} supplied records only; association does not establish cause or ACG-wide performance.`,
      "boundary-section",
    ),
    evidenceSection(
      "Next action",
      "Reconcile the source population, obtain reason codes and timestamps, and compare all four mutually exclusive cohorts.",
      "action-section",
    ),
    evidenceSection(
      "Definition & source",
      [
        make("p", "", payments.evidence_label),
        make("p", "source-files", sourceFilesFor("payments")),
      ],
    ),
  );
}

function renderGatesPanel(panel) {
  const capacity = dashboardData.guardrails.capacity;
  const closures = dashboardData.guardrails.closures;
  panel.append(
    evidenceSection(
      "What this means",
      "Capacity and closure figures are validation items—not approved business-case benefits.",
    ),
    evidenceSection("Evidence", metricList([
      ["Estimated manual process capacity", `${capacity.total_estimated_manual_hours_monthly.toFixed(2)} h/month`],
      ["Process-file repair estimate", `${capacity.process_file_exception_repair_hours_monthly.toFixed(2)} h/month`],
      ["Payment-file repair estimate", `${capacity.payment_file_repair_hours_monthly.toFixed(2)} h/month`],
      ["Closure-validation candidates", formatNumber(closures.validation_candidates)],
      ["Estimated candidate fees", `${formatUsdCompact(closures.estimated_annual_fees_usd)} annually`],
      ["Approved closures", formatNumber(closures.approved_closures)],
    ])),
    evidenceSection(
      "Decision boundary",
      "Management-estimated capacity is not observed labor or cashable savings. A closure candidate is not an approved closure, and estimated fees are not realized P&L.",
      "boundary-section",
    ),
    evidenceSection(
      "Next action",
      "Observe process time and control requirements; validate local account dependencies and actual fee removal before booking value.",
      "action-section",
    ),
    evidenceSection(
      "Definition & source",
      [
        make("p", "", `${capacity.evidence_label} · ${closures.evidence_label}`),
        make("p", "source-files", sourceFilesFor("process_capacity", "repair_baseline", "accounts")),
      ],
    ),
  );
}

function renderDrawerPanel(topic) {
  const panel = get(`#panel-${topic}`);
  panel.replaceChildren();
  if (topic === "overview") renderOverviewPanel(panel);
  if (topic === "visibility") renderVisibilityPanel(panel);
  if (topic === "liquidity") renderLiquidityPanel(panel);
  if (topic === "payments") renderPaymentsPanel(panel);
  if (topic === "gates") renderGatesPanel(panel);
}

function selectDrawerTab(topic, { focusTab = false } = {}) {
  if (!dashboardData) return;
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

function resetView({ shouldAnnounce = true } = {}) {
  state.liquidityDays = DEFAULT_STATE.liquidityDays;
  state.paymentMeasure = DEFAULT_STATE.paymentMeasure;
  state.visibilitySource = DEFAULT_STATE.visibilitySource;
  renderLiquidity();
  renderPayments();
  if (get("#evidence-dialog").open) renderDrawerPanel(state.drawerTab);
  updateResetState();
  if (shouldAnnounce) announce("Dashboard view reset to 14-day liquidity, payment records, and all reporting sources.");
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

  get("#evidence-dialog").addEventListener("close", () => {
    if (lastDrawerOpener && document.contains(lastDrawerOpener)) lastDrawerOpener.focus();
    lastDrawerOpener = null;
  });
}

function renderAll() {
  renderHeader();
  renderVisibility();
  renderLiquidity();
  renderPayments();
  renderGuardrails();
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
