(function attachNorthstarFilterModel(root, factory) {
  "use strict";

  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  if (root) {
    root.NorthstarFilterModel = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function createFilterModel() {
  "use strict";

  const REQUIRED_ACCOUNT_FIELDS = Object.freeze([
    "account_id",
    "entity_id",
    "entity_name",
    "region",
    "currency",
    "bank_name",
    "visibility_method",
    "closure_validation_candidate",
    "annual_fee_usd",
  ]);

  const ACCOUNT_DAY_FIELDS = Object.freeze([
    "date",
    "account_id",
    "reporting_delay_days",
    "positive_available_usd",
    "restricted_positive_available_usd",
    "negative_available_usd",
    "unflagged_payment_buffer_7d_usd",
    "net_screen_contribution_7d_usd",
    "unflagged_payment_buffer_14d_usd",
    "net_screen_contribution_14d_usd",
  ]);

  const PAYMENT_FIELDS = Object.freeze([
    "date",
    "account_id",
    "priority_cohort",
    "exception_flag",
    "repair_minutes",
  ]);

  const PRIORITY_COHORTS = Object.freeze([
    "Manual touch only",
    "Manual touch + cross-border wire",
    "Cross-border wire only",
    "Neither priority cohort",
  ]);

  const OUTSIDE_PRIORITY_UNION = "Neither priority cohort";

  const DEFAULT_METRIC_DEFINITIONS = Object.freeze([
    Object.freeze({
      id: "reporting-visibility",
      label: "Reporting visibility",
      description: "Calendar-date reporting proxy across supplied account-day observations.",
      keywords: "same day delayed portal spreadsheet API host-to-host reporting source",
    }),
    Object.freeze({
      id: "liquidity-screen",
      label: "Liquidity screening sensitivity",
      description: "Modeled 7-day and 14-day screens as of the selected end date.",
      keywords: "buffer restrictions negative positions cash screen scenario",
    }),
    Object.freeze({
      id: "payment-friction",
      label: "Payment friction",
      description: "Records, exceptions, and repair time in the deduplicated priority union.",
      keywords: "manual touch cross-border wire priority cohort overlap repair minutes",
    }),
    Object.freeze({
      id: "closure-candidates",
      label: "Closure-validation candidates",
      description: "Account candidates and estimated annual fees requiring local validation.",
      keywords: "account closure annual fee candidate not approved",
    }),
  ]);

  class FilterModelError extends Error {
    constructor(message, code = "invalid_filter_model") {
      super(message);
      this.name = "FilterModelError";
      this.code = code;
    }
  }

  function invariant(condition, message, code) {
    if (!condition) throw new FilterModelError(message, code);
  }

  function isPlainObject(value) {
    return Boolean(value) && typeof value === "object" && !Array.isArray(value);
  }

  function normalizeText(value) {
    return String(value ?? "")
      .normalize("NFKC")
      .toLocaleLowerCase("en-US")
      .trim();
  }

  function tokenizeLiteralQuery(value) {
    const normalized = normalizeText(value);
    return normalized ? normalized.split(/\s+/u).filter(Boolean) : [];
  }

  function isIsoDate(value) {
    if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/u.test(value)) return false;
    const [year, month, day] = value.split("-").map(Number);
    const date = new Date(Date.UTC(year, month - 1, day));
    return (
      date.getUTCFullYear() === year &&
      date.getUTCMonth() === month - 1 &&
      date.getUTCDate() === day
    );
  }

  function requireIsoDate(value, label) {
    invariant(isIsoDate(value), `${label} must be a valid ISO date`, "invalid_date");
    return value;
  }

  function requireString(value, label, { allowEmpty = false } = {}) {
    invariant(typeof value === "string", `${label} must be a string`, "invalid_contract");
    const result = value.trim();
    invariant(allowEmpty || result.length > 0, `${label} cannot be empty`, "invalid_contract");
    return result;
  }

  function requireFinite(value, label, { nullable = false, minimum = null } = {}) {
    if (nullable && value === null) return null;
    invariant(
      typeof value === "number" && Number.isFinite(value),
      `${label} must be a finite number${nullable ? " or null" : ""}`,
      "invalid_contract",
    );
    if (minimum !== null) {
      invariant(value >= minimum, `${label} must be at least ${minimum}`, "invalid_contract");
    }
    return value;
  }

  function requireBoolean(value, label) {
    invariant(typeof value === "boolean", `${label} must be boolean`, "invalid_contract");
    return value;
  }

  function periodFromPayload(payload) {
    invariant(isPlainObject(payload), "Dashboard payload must be an object", "invalid_contract");
    invariant(isPlainObject(payload.meta), "Dashboard payload is missing meta", "invalid_contract");
    const start = requireIsoDate(payload.meta.period_start, "meta.period_start");
    const end = requireIsoDate(payload.meta.period_end, "meta.period_end");
    invariant(start <= end, "Dashboard period is invalid", "invalid_contract");
    return { start, end };
  }

  function accountsFromPayload(payload) {
    invariant(
      isPlainObject(payload.filtering) && isPlainObject(payload.filtering.dimensions),
      "Dashboard payload is missing filtering dimensions",
      "invalid_contract",
    );
    const accounts = payload.filtering.dimensions.accounts;
    invariant(Array.isArray(accounts), "filtering.dimensions.accounts must be an array", "invalid_contract");

    const identifiers = new Set();
    return accounts.map((account, index) => {
      invariant(isPlainObject(account), `Account ${index} must be an object`, "invalid_contract");
      for (const field of REQUIRED_ACCOUNT_FIELDS) {
        invariant(Object.prototype.hasOwnProperty.call(account, field), `Account ${index} is missing ${field}`, "invalid_contract");
      }
      const normalized = {
        account_id: requireString(account.account_id, `Account ${index} account_id`),
        entity_id: requireString(account.entity_id, `Account ${index} entity_id`),
        entity_name: requireString(account.entity_name, `Account ${index} entity_name`),
        region: requireString(account.region, `Account ${index} region`),
        currency: requireString(account.currency, `Account ${index} currency`),
        bank_name: requireString(account.bank_name, `Account ${index} bank_name`),
        visibility_method: requireString(account.visibility_method, `Account ${index} visibility_method`),
        closure_validation_candidate: requireBoolean(
          account.closure_validation_candidate,
          `Account ${index} closure_validation_candidate`,
        ),
        annual_fee_usd: requireFinite(account.annual_fee_usd, `Account ${index} annual_fee_usd`, { minimum: 0 }),
      };
      invariant(!identifiers.has(normalized.account_id), `Duplicate account_id: ${normalized.account_id}`, "invalid_contract");
      identifiers.add(normalized.account_id);
      return normalized;
    });
  }

  function decodeCompactTable(table, requiredColumns, label) {
    invariant(isPlainObject(table), `${label} must be an object`, "invalid_contract");
    invariant(Array.isArray(table.columns), `${label}.columns must be an array`, "invalid_contract");
    invariant(Array.isArray(table.rows), `${label}.rows must be an array`, "invalid_contract");
    const columns = table.columns.map((column, index) => requireString(column, `${label}.columns[${index}]`));
    invariant(new Set(columns).size === columns.length, `${label}.columns must be unique`, "invalid_contract");
    for (const required of requiredColumns) {
      invariant(columns.includes(required), `${label} is missing column ${required}`, "invalid_contract");
    }

    return table.rows.map((row, rowIndex) => {
      if (Array.isArray(row)) {
        invariant(row.length === columns.length, `${label}.rows[${rowIndex}] has the wrong length`, "invalid_contract");
        return Object.fromEntries(columns.map((column, columnIndex) => [column, row[columnIndex]]));
      }
      invariant(isPlainObject(row), `${label}.rows[${rowIndex}] must be an array or object`, "invalid_contract");
      for (const column of requiredColumns) {
        invariant(Object.prototype.hasOwnProperty.call(row, column), `${label}.rows[${rowIndex}] is missing ${column}`, "invalid_contract");
      }
      return { ...row };
    });
  }

  function factsFromPayload(payload, accounts) {
    invariant(
      isPlainObject(payload.filtering) && isPlainObject(payload.filtering.facts),
      "Dashboard payload is missing filtering facts",
      "invalid_contract",
    );
    const knownAccounts = new Set(accounts.map((account) => account.account_id));
    const period = periodFromPayload(payload);
    const accountDays = decodeCompactTable(
      payload.filtering.facts.account_days,
      ACCOUNT_DAY_FIELDS,
      "filtering.facts.account_days",
    );
    const seenAccountDays = new Set();
    accountDays.forEach((row, index) => {
      row.date = requireIsoDate(row.date, `account_days row ${index} date`);
      row.account_id = requireString(row.account_id, `account_days row ${index} account_id`);
      invariant(knownAccounts.has(row.account_id), `Unknown account-day account: ${row.account_id}`, "invalid_contract");
      invariant(row.date >= period.start && row.date <= period.end, `Account-day date is outside the dashboard period: ${row.date}`, "invalid_contract");
      const key = `${row.date}\u0000${row.account_id}`;
      invariant(!seenAccountDays.has(key), `Duplicate account-day fact: ${row.date} ${row.account_id}`, "invalid_contract");
      seenAccountDays.add(key);
      row.reporting_delay_days = requireFinite(row.reporting_delay_days, `account_days row ${index} reporting_delay_days`, { minimum: 0 });
      for (const field of ACCOUNT_DAY_FIELDS.slice(3)) {
        row[field] = requireFinite(row[field], `account_days row ${index} ${field}`, { nullable: true });
      }
    });

    const payments = decodeCompactTable(
      payload.filtering.facts.payments,
      PAYMENT_FIELDS,
      "filtering.facts.payments",
    );
    const validCohorts = new Set(PRIORITY_COHORTS);
    payments.forEach((row, index) => {
      row.date = requireIsoDate(row.date, `payments row ${index} date`);
      row.account_id = requireString(row.account_id, `payments row ${index} account_id`);
      invariant(knownAccounts.has(row.account_id), `Unknown payment account: ${row.account_id}`, "invalid_contract");
      invariant(row.date >= period.start && row.date <= period.end, `Payment date is outside the dashboard period: ${row.date}`, "invalid_contract");
      row.priority_cohort = requireString(row.priority_cohort, `payments row ${index} priority_cohort`);
      invariant(validCohorts.has(row.priority_cohort), `Unknown priority cohort: ${row.priority_cohort}`, "invalid_contract");
      row.exception_flag = requireBoolean(row.exception_flag, `payments row ${index} exception_flag`);
      row.repair_minutes = requireFinite(row.repair_minutes, `payments row ${index} repair_minutes`, { minimum: 0 });
    });
    return { accountDays, payments };
  }

  function uniqueSorted(values) {
    return Array.from(new Set(values)).sort((left, right) => left.localeCompare(right, "en-US"));
  }

  function getFilterOptions(payload) {
    const accounts = accountsFromPayload(payload);
    const entityById = new Map();
    for (const account of accounts) {
      const existing = entityById.get(account.entity_id);
      invariant(
        !existing || existing === account.entity_name,
        `Entity ${account.entity_id} has conflicting names`,
        "invalid_contract",
      );
      entityById.set(account.entity_id, account.entity_name);
    }
    return {
      currencies: uniqueSorted(accounts.map((account) => account.currency)),
      regions: uniqueSorted(accounts.map((account) => account.region)),
      entities: Array.from(entityById, ([value, label]) => ({ value, label }))
        .sort((left, right) => left.label.localeCompare(right.label, "en-US") || left.value.localeCompare(right.value, "en-US")),
      banks: uniqueSorted(accounts.map((account) => account.bank_name)),
    };
  }

  function createDefaultState(payload) {
    const period = periodFromPayload(payload);
    return {
      dateFrom: period.start,
      dateTo: period.end,
      currency: "",
      region: "",
      entity: "",
      bank: "",
    };
  }

  function validateState(payload, candidate = {}) {
    invariant(isPlainObject(candidate), "Filter state must be an object", "invalid_state");
    const defaults = createDefaultState(payload);
    const state = { ...defaults, ...candidate };
    const period = periodFromPayload(payload);
    const options = getFilterOptions(payload);

    state.dateFrom = requireIsoDate(state.dateFrom, "dateFrom");
    state.dateTo = requireIsoDate(state.dateTo, "dateTo");
    invariant(
      state.dateFrom >= period.start && state.dateTo <= period.end,
      `Date range must stay within ${period.start} and ${period.end}`,
      "date_out_of_range",
    );
    invariant(state.dateFrom <= state.dateTo, "dateFrom must be on or before dateTo", "invalid_date_range");

    for (const field of ["currency", "region", "entity", "bank"]) {
      invariant(typeof state[field] === "string", `${field} must be a single string value`, "invalid_state");
      state[field] = state[field].trim();
    }
    const allowed = {
      currency: new Set(options.currencies),
      region: new Set(options.regions),
      entity: new Set(options.entities.map((entity) => entity.value)),
      bank: new Set(options.banks),
    };
    for (const field of Object.keys(allowed)) {
      invariant(!state[field] || allowed[field].has(state[field]), `Unknown ${field} filter: ${state[field]}`, "unknown_filter_value");
    }
    return state;
  }

  function selectedAccountsForState(accounts, state) {
    return accounts.filter((account) => (
      (!state.currency || account.currency === state.currency) &&
      (!state.region || account.region === state.region) &&
      (!state.entity || account.entity_id === state.entity) &&
      (!state.bank || account.bank_name === state.bank)
    ));
  }

  function percentage(numerator, denominator) {
    if (!Number.isFinite(numerator) || !Number.isFinite(denominator) || denominator === 0) return null;
    return Math.round((numerator / denominator) * 10000) / 100;
  }

  function summarizeVisibility(rows) {
    const maximumDelayByAccount = new Map();
    let sameDayObservations = 0;
    let withinOneDayObservations = 0;
    for (const row of rows) {
      const delay = row.reporting_delay_days;
      if (delay === 0) sameDayObservations += 1;
      if (delay <= 1) withinOneDayObservations += 1;
      maximumDelayByAccount.set(
        row.account_id,
        Math.max(maximumDelayByAccount.get(row.account_id) ?? 0, delay),
      );
    }
    const delays = Array.from(maximumDelayByAccount.values());
    const sameDayAccounts = delays.filter((delay) => delay === 0).length;
    const delayedAccounts = delays.filter((delay) => delay > 0).length;
    return {
      accounts_total: maximumDelayByAccount.size,
      observations: rows.length,
      same_day_accounts: sameDayAccounts,
      delayed_accounts: delayedAccounts,
      same_day_observations: sameDayObservations,
      delayed_observations: rows.length - sameDayObservations,
      within_one_day_observations: withinOneDayObservations,
      same_day_rate_pct: percentage(sameDayObservations, rows.length),
      within_one_day_rate_pct: percentage(withinOneDayObservations, rows.length),
    };
  }

  function completeSum(rows, field) {
    let total = 0;
    for (const row of rows) {
      if (typeof row[field] !== "number" || !Number.isFinite(row[field])) return null;
      total += row[field];
    }
    return Math.round(total * 1000000) / 1000000;
  }

  function summarizeLiquidity(accountRows, selectedAccountCount, dateTo) {
    const completeAccountSet = new Set(accountRows.map((row) => row.account_id));
    const panelComplete = (
      selectedAccountCount > 0 &&
      accountRows.length === selectedAccountCount &&
      completeAccountSet.size === selectedAccountCount
    );
    const baseFields = [
      "positive_available_usd",
      "restricted_positive_available_usd",
      "negative_available_usd",
    ];
    const scenarioFields = {
      "7": [
        "unflagged_payment_buffer_7d_usd",
        "net_screen_contribution_7d_usd",
      ],
      "14": [
        "unflagged_payment_buffer_14d_usd",
        "net_screen_contribution_14d_usd",
      ],
    };
    const allFields = baseFields.concat(scenarioFields["7"], scenarioFields["14"]);
    const sums = Object.fromEntries(allFields.map((field) => [field, completeSum(accountRows, field)]));
    const baseComplete = panelComplete && baseFields.every((field) => sums[field] !== null);
    const scenarioComplete = Object.fromEntries(
      Object.entries(scenarioFields).map(([days, fields]) => [
        days,
        panelComplete && fields.every((field) => sums[field] !== null),
      ]),
    );
    if (!baseComplete) {
      for (const field of baseFields) sums[field] = null;
    }
    for (const [days, fields] of Object.entries(scenarioFields)) {
      if (!scenarioComplete[days]) {
        for (const field of fields) sums[field] = null;
      }
    }
    return {
      as_of_date: dateTo,
      account_count: completeAccountSet.size,
      panel_complete: panelComplete,
      base_complete: baseComplete,
      complete: baseComplete && scenarioComplete["7"] && scenarioComplete["14"],
      positive_available_usd: sums.positive_available_usd,
      restricted_positive_available_usd: sums.restricted_positive_available_usd,
      negative_available_usd: sums.negative_available_usd,
      scenarios: {
        "7": {
          complete: scenarioComplete["7"],
          buffer_usd: sums.unflagged_payment_buffer_7d_usd,
          screen_usd: sums.net_screen_contribution_7d_usd,
        },
        "14": {
          complete: scenarioComplete["14"],
          buffer_usd: sums.unflagged_payment_buffer_14d_usd,
          screen_usd: sums.net_screen_contribution_14d_usd,
        },
      },
    };
  }

  function emptyMeasure() {
    return { records: 0, exceptions: 0, repair_minutes: 0 };
  }

  function addPayment(measure, row) {
    measure.records += 1;
    if (row.exception_flag) measure.exceptions += 1;
    measure.repair_minutes += row.repair_minutes;
  }

  function summarizePayments(rows) {
    const overall = emptyMeasure();
    const priorityUnion = emptyMeasure();
    const cohorts = Object.fromEntries(PRIORITY_COHORTS.map((cohort) => [cohort, emptyMeasure()]));
    for (const row of rows) {
      addPayment(overall, row);
      addPayment(cohorts[row.priority_cohort], row);
      if (row.priority_cohort !== OUTSIDE_PRIORITY_UNION) addPayment(priorityUnion, row);
    }
    priorityUnion.record_share_pct = percentage(priorityUnion.records, overall.records);
    priorityUnion.exception_share_pct = percentage(priorityUnion.exceptions, overall.exceptions);
    priorityUnion.repair_share_pct = percentage(priorityUnion.repair_minutes, overall.repair_minutes);
    return { overall, priority_union: priorityUnion, cohorts };
  }

  function summarizeClosures(accounts) {
    const candidates = accounts.filter((account) => account.closure_validation_candidate);
    return {
      validation_candidates: candidates.length,
      estimated_annual_fees_usd: Math.round(candidates.reduce((total, account) => total + account.annual_fee_usd, 0) * 100) / 100,
      candidate_account_ids: candidates.map((account) => account.account_id).sort((left, right) => left.localeCompare(right, "en-US")),
    };
  }

  function summarize(payload, candidateState = {}) {
    const accounts = accountsFromPayload(payload);
    const facts = factsFromPayload(payload, accounts);
    const state = validateState(payload, candidateState);
    const selectedAccounts = selectedAccountsForState(accounts, state);
    const selectedAccountIds = new Set(selectedAccounts.map((account) => account.account_id));
    const accountDays = facts.accountDays.filter((row) => (
      selectedAccountIds.has(row.account_id) && row.date >= state.dateFrom && row.date <= state.dateTo
    ));
    const asOfAccountDays = accountDays.filter((row) => row.date === state.dateTo);
    const payments = facts.payments.filter((row) => (
      selectedAccountIds.has(row.account_id) && row.date >= state.dateFrom && row.date <= state.dateTo
    ));

    return {
      state,
      scope: {
        account_count: selectedAccounts.length,
        account_ids: selectedAccounts.map((account) => account.account_id).sort((left, right) => left.localeCompare(right, "en-US")),
        has_matches: selectedAccounts.length > 0,
      },
      visibility: summarizeVisibility(accountDays),
      liquidity: summarizeLiquidity(asOfAccountDays, selectedAccounts.length, state.dateTo),
      payments: summarizePayments(payments),
      closures: summarizeClosures(selectedAccounts),
    };
  }

  function searchEntry(kind, id, label, description, values = {}) {
    const searchText = normalizeText([label, description, ...Object.values(values)].join(" "));
    return Object.freeze({ kind, id, label, description, values: Object.freeze({ ...values }), searchText });
  }

  function buildSearchIndex(payload, metricDefinitions = DEFAULT_METRIC_DEFINITIONS) {
    const accounts = accountsFromPayload(payload);
    invariant(Array.isArray(metricDefinitions), "Metric definitions must be an array", "invalid_search_index");
    const entries = [];
    const seen = new Set();
    function append(entry) {
      const key = `${entry.kind}\u0000${entry.id}`;
      invariant(!seen.has(key), `Duplicate search entry: ${entry.kind} ${entry.id}`, "invalid_search_index");
      seen.add(key);
      entries.push(entry);
    }

    metricDefinitions.forEach((definition, index) => {
      invariant(isPlainObject(definition), `Metric definition ${index} must be an object`, "invalid_search_index");
      const id = requireString(definition.id, `Metric definition ${index} id`);
      const label = requireString(definition.label, `Metric definition ${index} label`);
      const description = requireString(definition.description, `Metric definition ${index} description`);
      append(searchEntry("metric", id, label, description, { keywords: String(definition.keywords ?? "") }));
    });

    const dimensions = [
      ["currency", "Currency", uniqueSorted(accounts.map((account) => account.currency))],
      ["region", "Region", uniqueSorted(accounts.map((account) => account.region))],
      ["bank", "Bank", uniqueSorted(accounts.map((account) => account.bank_name))],
    ];
    dimensions.forEach(([dimension, noun, values]) => {
      values.forEach((value) => append(searchEntry(
        "dimension",
        `${dimension}:${value}`,
        value,
        `${noun} filter`,
        { dimension, value },
      )));
    });

    const entities = new Map();
    accounts.forEach((account) => entities.set(account.entity_id, account.entity_name));
    Array.from(entities, ([entityId, entityName]) => ({ entityId, entityName }))
      .sort((left, right) => left.entityName.localeCompare(right.entityName, "en-US"))
      .forEach(({ entityId, entityName }) => append(searchEntry(
        "dimension",
        `entity:${entityId}`,
        `${entityId} — ${entityName}`,
        "Entity filter",
        { dimension: "entity", value: entityId, entity_name: entityName },
      )));

    accounts
      .slice()
      .sort((left, right) => left.account_id.localeCompare(right.account_id, "en-US"))
      .forEach((account) => append(searchEntry(
        "account",
        account.account_id,
        `${account.account_id} — ${account.entity_name}`,
        `${account.bank_name} · ${account.currency} · ${account.region}`,
        account,
      )));
    return Object.freeze(entries);
  }

  function querySearchIndex(index, query, { limit = 12 } = {}) {
    invariant(Array.isArray(index), "Search index must be an array", "invalid_search_index");
    invariant(Number.isInteger(limit) && limit >= 0, "Search limit must be a nonnegative integer", "invalid_search_query");
    const tokens = tokenizeLiteralQuery(query);
    if (tokens.length === 0 || limit === 0) return [];
    return index
      .filter((entry) => tokens.every((token) => entry.searchText.includes(token)))
      .sort((left, right) => {
        const leftExact = normalizeText(left.label) === normalizeText(query) ? 0 : 1;
        const rightExact = normalizeText(right.label) === normalizeText(query) ? 0 : 1;
        if (leftExact !== rightExact) return leftExact - rightExact;
        const rank = { metric: 0, dimension: 1, account: 2 };
        return rank[left.kind] - rank[right.kind] || left.label.localeCompare(right.label, "en-US");
      })
      .slice(0, limit)
      .map(({ searchText, ...entry }) => entry);
  }

  return Object.freeze({
    FilterModelError,
    PRIORITY_COHORTS,
    DEFAULT_METRIC_DEFINITIONS,
    createDefaultState,
    resetState: createDefaultState,
    validateState,
    getFilterOptions,
    summarize,
    buildSearchIndex,
    querySearchIndex,
    tokenizeLiteralQuery,
  });
});
