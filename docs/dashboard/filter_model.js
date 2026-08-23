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

  const VISIBILITY_METHODS = Object.freeze([
    "API",
    "Host-to-host",
    "Portal",
    "Spreadsheet",
  ]);

  const REGION_METADATA = Object.freeze([
    Object.freeze({ code: "NA", label: "North America" }),
    Object.freeze({ code: "EMEA", label: "Europe, Middle East and Africa" }),
    Object.freeze({ code: "APAC", label: "Asia Pacific" }),
  ]);

  const LIQUIDITY_HORIZONS = Object.freeze(["7", "14"]);
  const MONEY_TOLERANCE_USD = 0.01;

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
      id: "regional-footprint",
      label: "Regional footprint",
      description: "Governed account, reporting, and payment evidence across NA, EMEA, and APAC.",
      keywords: "map geography geographic region regional North America EMEA APAC footprint",
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

  function roundToSix(value) {
    return Math.round(value * 1000000) / 1000000;
  }

  function roundToCents(value) {
    return Math.round(value * 100) / 100;
  }

  function nearlyEqual(left, right, tolerance = MONEY_TOLERANCE_USD) {
    return Number.isFinite(left) && Number.isFinite(right) && Math.abs(left - right) <= tolerance;
  }

  function isoDateRange(start, end) {
    const dates = [];
    const cursor = new Date(`${start}T00:00:00Z`);
    const final = new Date(`${end}T00:00:00Z`);
    while (cursor <= final) {
      dates.push(cursor.toISOString().slice(0, 10));
      cursor.setUTCDate(cursor.getUTCDate() + 1);
    }
    return dates;
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
      invariant(
        REGION_METADATA.some(({ code }) => code === normalized.region),
        `Unknown account region: ${normalized.region}`,
        "invalid_contract",
      );
      invariant(
        VISIBILITY_METHODS.includes(normalized.visibility_method),
        `Unknown visibility method: ${normalized.visibility_method}`,
        "invalid_contract",
      );
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
      invariant(
        Number.isInteger(row.reporting_delay_days) && row.reporting_delay_days <= 3,
        `account_days row ${index} reporting_delay_days must be an integer from 0 to 3`,
        "invalid_contract",
      );
      row.positive_available_usd = requireFinite(
        row.positive_available_usd,
        `account_days row ${index} positive_available_usd`,
        { minimum: 0 },
      );
      row.restricted_positive_available_usd = requireFinite(
        row.restricted_positive_available_usd,
        `account_days row ${index} restricted_positive_available_usd`,
        { minimum: 0 },
      );
      row.negative_available_usd = requireFinite(
        row.negative_available_usd,
        `account_days row ${index} negative_available_usd`,
      );
      invariant(
        row.restricted_positive_available_usd <= row.positive_available_usd,
        `account_days row ${index} restrictions exceed positive availability`,
        "invalid_contract",
      );
      invariant(
        row.negative_available_usd <= 0,
        `account_days row ${index} negative availability must be nonpositive`,
        "invalid_contract",
      );

      for (const days of LIQUIDITY_HORIZONS) {
        const bufferField = `unflagged_payment_buffer_${days}d_usd`;
        const screenField = `net_screen_contribution_${days}d_usd`;
        row[bufferField] = requireFinite(row[bufferField], `account_days row ${index} ${bufferField}`, { nullable: true });
        row[screenField] = requireFinite(row[screenField], `account_days row ${index} ${screenField}`, { nullable: true });
        if (row[bufferField] !== null) {
          invariant(
            row[bufferField] >= 0,
            `account_days row ${index} ${bufferField} must be nonnegative`,
            "invalid_contract",
          );
        }
        if (row[bufferField] !== null && row[screenField] !== null) {
          const unflaggedPositive = row.positive_available_usd - row.restricted_positive_available_usd;
          const unflaggedScreen = row[screenField] - row.negative_available_usd;
          const effectiveBuffer = unflaggedPositive - unflaggedScreen;
          invariant(
            unflaggedScreen >= -MONEY_TOLERANCE_USD,
            `account_days row ${index} ${days}-day unflagged screen is negative`,
            "invalid_contract",
          );
          invariant(
            effectiveBuffer >= -MONEY_TOLERANCE_USD && effectiveBuffer <= row[bufferField] + MONEY_TOLERANCE_USD,
            `account_days row ${index} ${days}-day screen does not reconcile to the account-level floor`,
            "invalid_contract",
          );
        }
      }
    });
    const expectedDates = isoDateRange(period.start, period.end);
    invariant(
      accountDays.length === accounts.length * expectedDates.length,
      "filtering.facts.account_days must contain one row per account and calendar date",
      "invalid_contract",
    );
    for (const date of expectedDates) {
      for (const account of accounts) {
        invariant(
          seenAccountDays.has(`${date}\u0000${account.account_id}`),
          `Missing account-day fact: ${date} ${account.account_id}`,
          "invalid_contract",
        );
      }
    }

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
      invariant(
        Number.isInteger(row.repair_minutes),
        `payments row ${index} repair_minutes must be an integer`,
        "invalid_contract",
      );
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

  function summarizeVisibilityRows(rows) {
    const maximumDelayByAccount = new Map();
    let sameDayObservations = 0;
    let oneDayDelayedObservations = 0;
    let twoPlusDayDelayedObservations = 0;
    let withinOneDayObservations = 0;
    for (const row of rows) {
      const delay = row.reporting_delay_days;
      if (delay === 0) sameDayObservations += 1;
      if (delay === 1) oneDayDelayedObservations += 1;
      if (delay >= 2) twoPlusDayDelayedObservations += 1;
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
      same_day_account_share_pct: percentage(sameDayAccounts, maximumDelayByAccount.size),
      delayed_account_share_pct: percentage(delayedAccounts, maximumDelayByAccount.size),
      same_day_observations: sameDayObservations,
      delayed_observations: rows.length - sameDayObservations,
      one_day_delayed_observations: oneDayDelayedObservations,
      two_plus_day_delayed_observations: twoPlusDayDelayedObservations,
      within_one_day_observations: withinOneDayObservations,
      same_day_rate_pct: percentage(sameDayObservations, rows.length),
      within_one_day_rate_pct: percentage(withinOneDayObservations, rows.length),
      maximum_delay_days: delays.length > 0 ? Math.max(...delays) : null,
    };
  }

  function summarizeVisibility(rows, accounts) {
    const accountMethod = new Map(accounts.map((account) => [account.account_id, account.visibility_method]));
    const rowsByMethod = new Map(VISIBILITY_METHODS.map((method) => [method, []]));
    for (const row of rows) {
      const method = accountMethod.get(row.account_id);
      invariant(method && rowsByMethod.has(method), `Visibility row has no governed method: ${row.account_id}`, "invalid_contract");
      rowsByMethod.get(method).push(row);
    }

    const overall = summarizeVisibilityRows(rows);
    invariant(
      overall.accounts_total === accounts.length,
      "Visibility summary does not cover every selected account",
      "invalid_contract",
    );
    const byMethod = VISIBILITY_METHODS.map((method) => {
      const methodSummary = summarizeVisibilityRows(rowsByMethod.get(method));
      const expectedAccounts = accounts.filter((account) => account.visibility_method === method).length;
      invariant(
        methodSummary.accounts_total === expectedAccounts,
        `Visibility method ${method} does not cover every selected account`,
        "invalid_contract",
      );
      return {
        method,
        account_share_pct: percentage(methodSummary.accounts_total, overall.accounts_total),
        ...methodSummary,
      };
    });

    const reconciledFields = [
      "accounts_total",
      "same_day_accounts",
      "delayed_accounts",
      "observations",
      "same_day_observations",
      "delayed_observations",
      "one_day_delayed_observations",
      "two_plus_day_delayed_observations",
      "within_one_day_observations",
    ];
    for (const field of reconciledFields) {
      invariant(
        byMethod.reduce((total, row) => total + row[field], 0) === overall[field],
        `Visibility method ${field} does not reconcile to the selected total`,
        "invalid_contract",
      );
    }
    return { ...overall, by_method: byMethod };
  }

  function completeSum(rows, field) {
    let total = 0;
    for (const row of rows) {
      if (typeof row[field] !== "number" || !Number.isFinite(row[field])) return null;
      total += row[field];
    }
    return roundToSix(total);
  }

  function liquidityWaterfallSteps(values = {}) {
    return [
      {
        key: "gross_positive_estimated_availability",
        label: "Gross positive balance — screening only",
        role: "starting_total",
        delta_usd: values.gross ?? null,
        total_usd: values.gross ?? null,
      },
      {
        key: "preliminary_restrictions",
        label: "Preliminary restrictions",
        role: "deduction",
        delta_usd: values.restrictionDelta ?? null,
        total_usd: values.afterRestrictions ?? null,
      },
      {
        key: "negative_positions",
        label: "Negative positions",
        role: "deduction",
        delta_usd: values.negative ?? null,
        total_usd: values.apparentNetBeforeBuffer ?? null,
      },
      {
        key: "apparent_net_before_buffer",
        label: "Apparent net before illustrative buffer",
        role: "subtotal",
        delta_usd: null,
        total_usd: values.apparentNetBeforeBuffer ?? null,
      },
      {
        key: "effective_buffer_after_account_floors",
        label: "Effective buffer after account-level floors",
        role: "deduction",
        delta_usd: values.bufferDelta ?? null,
        total_usd: values.screen ?? null,
      },
      {
        key: "modeled_screen",
        label: "Modeled screening result",
        role: "resulting_total",
        delta_usd: null,
        total_usd: values.screen ?? null,
      },
    ];
  }

  function summarizeLiquidityWaterfall(sums, baseComplete, scenarioComplete, days) {
    if (!baseComplete || !scenarioComplete) {
      return {
        complete: false,
        raw_buffer_usd: null,
        effective_buffer_deduction_usd: null,
        unapplied_buffer_due_to_floor_usd: null,
        steps: liquidityWaterfallSteps(),
      };
    }

    const gross = sums.positive_available_usd;
    const restrictions = sums.restricted_positive_available_usd;
    const negative = sums.negative_available_usd;
    const rawBuffer = sums[`unflagged_payment_buffer_${days}d_usd`];
    const screen = sums[`net_screen_contribution_${days}d_usd`];
    const afterRestrictions = roundToSix(gross - restrictions);
    const apparentNetBeforeBuffer = roundToSix(afterRestrictions + negative);
    let effectiveBuffer = roundToSix(apparentNetBeforeBuffer - screen);
    if (Math.abs(effectiveBuffer) <= MONEY_TOLERANCE_USD) effectiveBuffer = 0;
    invariant(
      effectiveBuffer >= -MONEY_TOLERANCE_USD && effectiveBuffer <= rawBuffer + MONEY_TOLERANCE_USD,
      `${days}-day aggregate screen does not reconcile to the account-level floor`,
      "invalid_contract",
    );
    invariant(
      nearlyEqual(apparentNetBeforeBuffer - effectiveBuffer, screen),
      `${days}-day waterfall does not reconcile to the modeled screen`,
      "invalid_contract",
    );
    let unappliedBuffer = roundToSix(rawBuffer - effectiveBuffer);
    if (Math.abs(unappliedBuffer) <= MONEY_TOLERANCE_USD) unappliedBuffer = 0;
    invariant(
      unappliedBuffer >= -MONEY_TOLERANCE_USD,
      `${days}-day unapplied buffer cannot be negative`,
      "invalid_contract",
    );

    return {
      complete: true,
      raw_buffer_usd: rawBuffer,
      effective_buffer_deduction_usd: effectiveBuffer,
      unapplied_buffer_due_to_floor_usd: Math.max(0, unappliedBuffer),
      steps: liquidityWaterfallSteps({
        gross,
        restrictionDelta: roundToSix(-restrictions),
        afterRestrictions,
        negative,
        apparentNetBeforeBuffer,
        bufferDelta: roundToSix(-effectiveBuffer),
        screen,
      }),
    };
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
    const waterfalls = Object.fromEntries(
      LIQUIDITY_HORIZONS.map((days) => [
        days,
        summarizeLiquidityWaterfall(sums, baseComplete, scenarioComplete[days], days),
      ]),
    );
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
      waterfalls,
    };
  }

  function summarizeLiquidityTrend(rows, selectedAccountCount, dateFrom, dateTo) {
    const rowsByDate = new Map();
    for (const row of rows) {
      if (!rowsByDate.has(row.date)) rowsByDate.set(row.date, []);
      rowsByDate.get(row.date).push(row);
    }
    return isoDateRange(dateFrom, dateTo).map((date) => {
      const snapshot = summarizeLiquidity(rowsByDate.get(date) || [], selectedAccountCount, date);
      return {
        date,
        account_count: snapshot.account_count,
        panel_complete: snapshot.panel_complete,
        base_complete: snapshot.base_complete,
        complete: snapshot.complete,
        positive_available_usd: snapshot.positive_available_usd,
        restricted_positive_available_usd: snapshot.restricted_positive_available_usd,
        negative_available_usd: snapshot.negative_available_usd,
        scenarios: snapshot.scenarios,
      };
    });
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
    overall.exception_rate_pct = percentage(overall.exceptions, overall.records);
    priorityUnion.exception_rate_pct = percentage(priorityUnion.exceptions, priorityUnion.records);
    for (const cohort of PRIORITY_COHORTS) {
      const measure = cohorts[cohort];
      measure.record_contribution_pct = percentage(measure.records, overall.records);
      measure.exception_contribution_pct = percentage(measure.exceptions, overall.exceptions);
      measure.repair_contribution_pct = percentage(measure.repair_minutes, overall.repair_minutes);
      measure.exception_rate_pct = percentage(measure.exceptions, measure.records);
    }
    for (const field of ["records", "exceptions", "repair_minutes"]) {
      invariant(
        PRIORITY_COHORTS.reduce((total, cohort) => total + cohorts[cohort][field], 0) === overall[field],
        `Payment cohort ${field} does not reconcile to the selected total`,
        "invalid_contract",
      );
      invariant(
        PRIORITY_COHORTS
          .filter((cohort) => cohort !== OUTSIDE_PRIORITY_UNION)
          .reduce((total, cohort) => total + cohorts[cohort][field], 0) === priorityUnion[field],
        `Payment priority-union ${field} does not reconcile to the selected cohorts`,
        "invalid_contract",
      );
    }
    return {
      overall,
      priority_union: priorityUnion,
      cohort_order: [...PRIORITY_COHORTS],
      cohorts,
    };
  }

  function summarizeClosures(accounts) {
    const orderedAccounts = [...accounts].sort((left, right) => left.account_id.localeCompare(right.account_id, "en-US"));
    const candidates = orderedAccounts.filter((account) => account.closure_validation_candidate);
    const totalAnnualFees = roundToCents(orderedAccounts.reduce((total, account) => total + account.annual_fee_usd, 0));
    const candidateAnnualFees = roundToCents(candidates.reduce((total, account) => total + account.annual_fee_usd, 0));
    invariant(candidates.length <= orderedAccounts.length, "Closure candidates exceed selected accounts", "invalid_contract");
    invariant(
      candidateAnnualFees <= totalAnnualFees + MONEY_TOLERANCE_USD,
      "Closure candidate fees exceed selected account fees",
      "invalid_contract",
    );
    return {
      accounts_total: orderedAccounts.length,
      validation_candidates: candidates.length,
      non_candidates: orderedAccounts.length - candidates.length,
      candidate_share_pct: percentage(candidates.length, orderedAccounts.length),
      total_annual_fees_usd: totalAnnualFees,
      estimated_annual_fees_usd: candidateAnnualFees,
      candidate_fee_share_pct: percentage(candidateAnnualFees, totalAnnualFees),
      candidate_account_ids: candidates.map((account) => account.account_id),
      candidate_accounts: candidates.map((account) => ({
        account_id: account.account_id,
        entity_id: account.entity_id,
        entity_name: account.entity_name,
        region: account.region,
        currency: account.currency,
        bank_name: account.bank_name,
        visibility_method: account.visibility_method,
        annual_fee_usd: account.annual_fee_usd,
      })),
    };
  }

  function summarizeRegionalFootprint(accounts, facts, state) {
    const facetState = { ...state, region: "" };
    const facetAccounts = selectedAccountsForState(accounts, facetState);
    const facetAccountIds = new Set(facetAccounts.map((account) => account.account_id));
    const facetAccountDays = facts.accountDays.filter((row) => (
      facetAccountIds.has(row.account_id) && row.date >= state.dateFrom && row.date <= state.dateTo
    ));
    const facetPayments = facts.payments.filter((row) => (
      facetAccountIds.has(row.account_id) && row.date >= state.dateFrom && row.date <= state.dateTo
    ));
    const facetVisibility = summarizeVisibility(facetAccountDays, facetAccounts);
    const facetPaymentSummary = summarizePayments(facetPayments);
    const facetClosures = summarizeClosures(facetAccounts);
    const facetAsOfRows = facetAccountDays.filter((row) => row.date === state.dateTo);
    const facetLiquidity = summarizeLiquidity(facetAsOfRows, facetAccounts.length, state.dateTo);

    const rows = REGION_METADATA.map(({ code, label }) => {
      const regionAccounts = facetAccounts.filter((account) => account.region === code);
      const regionAccountIds = new Set(regionAccounts.map((account) => account.account_id));
      const accountDays = facetAccountDays.filter((row) => regionAccountIds.has(row.account_id));
      const asOfAccountDays = accountDays.filter((row) => row.date === state.dateTo);
      const payments = facetPayments.filter((row) => regionAccountIds.has(row.account_id));
      const visibility = summarizeVisibility(accountDays, regionAccounts);
      const paymentSummary = summarizePayments(payments);
      const liquidity = summarizeLiquidity(asOfAccountDays, regionAccounts.length, state.dateTo);
      const closures = summarizeClosures(regionAccounts);
      return {
        code,
        label,
        selected: state.region === code,
        status: regionAccounts.length > 0 ? "available" : "no_matching_accounts",
        account_count: regionAccounts.length,
        visibility: {
          delayed_accounts: visibility.delayed_accounts,
          delayed_account_share_pct: visibility.delayed_account_share_pct,
          account_days: visibility.observations,
          same_day_account_days: visibility.same_day_observations,
          same_day_rate_pct: visibility.same_day_rate_pct,
        },
        payments: {
          records: paymentSummary.overall.records,
          exceptions: paymentSummary.overall.exceptions,
          repair_minutes: paymentSummary.overall.repair_minutes,
          priority_union_records: paymentSummary.priority_union.records,
          priority_union_record_share_pct: paymentSummary.priority_union.record_share_pct,
        },
        liquidity: {
          as_of_date: liquidity.as_of_date,
          scenarios: Object.fromEntries(LIQUIDITY_HORIZONS.map((days) => [
            days,
            {
              complete: liquidity.scenarios[days].complete,
              screen_usd: liquidity.scenarios[days].screen_usd,
            },
          ])),
        },
        closures: {
          snapshot_date: "2026-06-30",
          validation_candidates: closures.validation_candidates,
          estimated_annual_fees_usd: closures.estimated_annual_fees_usd,
        },
      };
    });

    invariant(
      rows.reduce((total, row) => total + row.account_count, 0) === facetAccounts.length,
      "Regional account counts do not reconcile to the facet scope",
      "invalid_contract",
    );
    invariant(
      rows.reduce((total, row) => total + row.visibility.account_days, 0) === facetAccountDays.length,
      "Regional account-day counts do not reconcile to the facet scope",
      "invalid_contract",
    );
    invariant(
      rows.reduce((total, row) => total + row.payments.records, 0) === facetPayments.length,
      "Regional payment counts do not reconcile to the facet scope",
      "invalid_contract",
    );
    const integerReconciliations = [
      ["delayed accounts", rows.reduce((total, row) => total + row.visibility.delayed_accounts, 0), facetVisibility.delayed_accounts],
      ["same-day account-days", rows.reduce((total, row) => total + row.visibility.same_day_account_days, 0), facetVisibility.same_day_observations],
      ["payment exceptions", rows.reduce((total, row) => total + row.payments.exceptions, 0), facetPaymentSummary.overall.exceptions],
      ["payment repair minutes", rows.reduce((total, row) => total + row.payments.repair_minutes, 0), facetPaymentSummary.overall.repair_minutes],
      ["priority-union records", rows.reduce((total, row) => total + row.payments.priority_union_records, 0), facetPaymentSummary.priority_union.records],
      ["closure candidates", rows.reduce((total, row) => total + row.closures.validation_candidates, 0), facetClosures.validation_candidates],
    ];
    integerReconciliations.forEach(([label, regionalTotal, facetTotal]) => {
      invariant(
        regionalTotal === facetTotal,
        `Regional ${label} do not reconcile to the facet scope`,
        "invalid_contract",
      );
    });
    invariant(
      nearlyEqual(
        rows.reduce((total, row) => total + row.closures.estimated_annual_fees_usd, 0),
        facetClosures.estimated_annual_fees_usd,
      ),
      "Regional closure candidate fees do not reconcile to the facet scope",
      "invalid_contract",
    );

    for (const days of LIQUIDITY_HORIZONS) {
      const rowsWithAccounts = rows.filter((row) => row.account_count > 0);
      const allRegionsComplete = rowsWithAccounts.length > 0 && rowsWithAccounts.every(
        (row) => row.liquidity.scenarios[days].complete,
      );
      if (allRegionsComplete && facetLiquidity.scenarios[days].complete) {
        const regionalScreen = roundToSix(rowsWithAccounts.reduce(
          (total, row) => total + row.liquidity.scenarios[days].screen_usd,
          0,
        ));
        invariant(
          nearlyEqual(regionalScreen, facetLiquidity.scenarios[days].screen_usd),
          `${days}-day regional screens do not reconcile to the facet scope`,
          "invalid_contract",
        );
      }
    }

    return {
      selected_region: state.region || null,
      region_filter_mode: "facet_override",
      order: REGION_METADATA.map(({ code }) => code),
      basis: {
        date_from: state.dateFrom,
        date_to: state.dateTo,
        currency: state.currency || null,
        entity: state.entity || null,
        bank: state.bank || null,
        account_count: facetAccounts.length,
        regions_represented: rows.filter((row) => row.account_count > 0).length,
      },
      rows,
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

    const liquidity = summarizeLiquidity(asOfAccountDays, selectedAccounts.length, state.dateTo);
    liquidity.trend = summarizeLiquidityTrend(accountDays, selectedAccounts.length, state.dateFrom, state.dateTo);

    return {
      state,
      scope: {
        account_count: selectedAccounts.length,
        account_ids: selectedAccounts.map((account) => account.account_id).sort((left, right) => left.localeCompare(right, "en-US")),
        has_matches: selectedAccounts.length > 0,
      },
      visibility: summarizeVisibility(accountDays, selectedAccounts),
      liquidity,
      payments: summarizePayments(payments),
      closures: summarizeClosures(selectedAccounts),
      regional: summarizeRegionalFootprint(accounts, facts, state),
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
    REGION_METADATA,
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
