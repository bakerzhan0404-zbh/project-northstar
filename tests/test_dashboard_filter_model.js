"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");

const FilterModel = require(path.join(__dirname, "..", "dashboard", "filter_model.js"));

const ACCOUNT_DAY_COLUMNS = [
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
];

const PAYMENT_COLUMNS = [
  "date",
  "account_id",
  "priority_cohort",
  "exception_flag",
  "repair_minutes",
];

function isoDates(start, end) {
  const dates = [];
  const cursor = new Date(`${start}T00:00:00Z`);
  const final = new Date(`${end}T00:00:00Z`);
  while (cursor <= final) {
    dates.push(cursor.toISOString().slice(0, 10));
    cursor.setUTCDate(cursor.getUTCDate() + 1);
  }
  return dates;
}

function compact(columns, objects) {
  return {
    columns,
    rows: objects.map((object) => columns.map((column) => object[column])),
  };
}

function distribute(total, count, index) {
  if (count === 0) return 0;
  const base = Math.floor(total / count);
  return base + (index < total % count ? 1 : 0);
}

function makeAccounts() {
  const entityNames = {
    E001: "Aurelius Group Holdings",
    E002: "Aurelius Home US",
    E003: "Aurelius Wellness US",
    E004: "Aurelius Canada",
    E005: "Aurelius UK",
    E006: "Aurelius Germany",
    E007: "Aurelius France",
    E008: "Aurelius Netherlands",
    E009: "Aurelius Spain",
    E010: "Aurelius Singapore",
    E011: "Aurelius Australia",
    E012: "Aurelius Japan",
    E013: "Aurelius Korea",
    E014: "Aurelius India",
    E015: "Aurelius Hong Kong",
    E016: "Aurelius Global Sourcing",
  };
  const accounts = Array.from({ length: 55 }, (_, offset) => {
    const number = offset + 1;
    const suffix = String(number).padStart(4, "0");
    const entityId = `E${String(((number - 1) % 16) + 1).padStart(3, "0")}`;
    return {
      account_id: `AC${suffix}`,
      entity_id: entityId,
      entity_name: entityNames[entityId],
      region: number <= 16 ? "NA" : number <= 33 ? "EMEA" : "APAC",
      currency: number <= 23 ? "USD" : number <= 33 ? "EUR" : "JPY",
      bank_name: number % 2 === 0 ? "Union Atlantic" : "Continental Trust",
      visibility_method: number <= 32 ? "API" : number <= 41 ? "Portal" : "Spreadsheet",
      closure_validation_candidate: false,
      annual_fee_usd: 900,
    };
  });
  const byId = Object.fromEntries(accounts.map((account) => [account.account_id, account]));

  Object.assign(byId.AC0024, {
    entity_id: "E006",
    entity_name: "Aurelius Germany",
    region: "EMEA",
    currency: "EUR",
    bank_name: "Pacific Crown",
    visibility_method: "Host-to-host",
    closure_validation_candidate: true,
    annual_fee_usd: 2400,
  });
  Object.assign(byId.AC0027, {
    entity_id: "E007",
    entity_name: "Aurelius France",
    region: "EMEA",
    currency: "EUR",
    bank_name: "Pacific Crown",
    visibility_method: "API",
  });
  Object.assign(byId.AC0001, {
    entity_id: "E001",
    entity_name: "Aurelius Group Holdings",
    region: "NA",
    currency: "USD",
    bank_name: "Union Atlantic",
    visibility_method: "Spreadsheet",
  });
  Object.assign(byId.AC0004, {
    closure_validation_candidate: true,
    annual_fee_usd: 900,
  });
  Object.assign(byId.AC0009, {
    closure_validation_candidate: true,
    annual_fee_usd: 3600,
  });
  Object.assign(byId.AC0037, {
    closure_validation_candidate: true,
    annual_fee_usd: 900,
  });
  return accounts;
}

function makeAccountDays(accounts) {
  const dates = isoDates("2026-01-01", "2026-06-30");
  const rows = [];
  const global = {
    positive: 57_801_215.46,
    restricted: 8_053_700.97,
    negative: -2_138_293.09,
    buffer7: 5_485_896.33,
    screen7: 42_844_787.78,
    buffer14: 10_828_186.91,
    screen14: 38_127_490.73,
  };
  const combo = {
    positive: 379_896.51184192166,
    restricted: 370_325.1154437162,
    screen: 9_571.3963982055,
  };

  for (const date of dates) {
    for (const account of accounts) {
      const number = Number(account.account_id.slice(2));
      const row = {
        date,
        account_id: account.account_id,
        reporting_delay_days: number <= 32 ? 0 : number <= 41 ? 1 : 2,
        positive_available_usd: 1,
        restricted_positive_available_usd: 0,
        negative_available_usd: 0,
        unflagged_payment_buffer_7d_usd: date < "2026-01-07" ? null : 0,
        net_screen_contribution_7d_usd: date < "2026-01-07" ? null : 1,
        unflagged_payment_buffer_14d_usd: date < "2026-01-14" ? null : 0,
        net_screen_contribution_14d_usd: date < "2026-01-14" ? null : 1,
      };
      if (date === "2026-06-30") {
        Object.assign(row, {
          positive_available_usd: 0,
          restricted_positive_available_usd: 0,
          negative_available_usd: 0,
          unflagged_payment_buffer_7d_usd: 0,
          net_screen_contribution_7d_usd: 0,
          unflagged_payment_buffer_14d_usd: 0,
          net_screen_contribution_14d_usd: 0,
        });
        if (account.account_id === "AC0024") {
          row.positive_available_usd = combo.screen;
          row.net_screen_contribution_7d_usd = combo.screen;
          row.net_screen_contribution_14d_usd = combo.screen;
        } else if (account.account_id === "AC0027") {
          row.positive_available_usd = combo.positive - combo.screen;
          row.restricted_positive_available_usd = combo.restricted;
        } else if (account.account_id === "AC0001") {
          row.positive_available_usd = global.positive - combo.positive;
          row.restricted_positive_available_usd = global.restricted - combo.restricted;
          row.negative_available_usd = global.negative;
          row.unflagged_payment_buffer_7d_usd = global.buffer7;
          row.net_screen_contribution_7d_usd = global.screen7 - combo.screen;
          row.unflagged_payment_buffer_14d_usd = global.buffer14;
          row.net_screen_contribution_14d_usd = global.screen14 - combo.screen;
        }
      }
      rows.push(row);
    }
  }
  return rows;
}

function appendPaymentSegment(rows, options) {
  const {
    count,
    priorityCount,
    exceptionCount,
    priorityExceptionCount,
    repairTotal,
    priorityRepairTotal,
    dateForIndex,
    accountForIndex,
  } = options;
  const outsideCount = count - priorityCount;
  const outsideExceptions = exceptionCount - priorityExceptionCount;
  const outsideRepair = repairTotal - priorityRepairTotal;
  assert.ok(priorityCount >= 0 && outsideCount >= 0);
  assert.ok(priorityExceptionCount <= priorityCount && outsideExceptions <= outsideCount);

  for (let index = 0; index < count; index += 1) {
    const inPriority = index < priorityCount;
    const localIndex = inPriority ? index : index - priorityCount;
    rows.push({
      date: dateForIndex(index),
      account_id: accountForIndex(index),
      priority_cohort: inPriority ? "Manual touch only" : "Neither priority cohort",
      exception_flag: inPriority
        ? localIndex < priorityExceptionCount
        : localIndex < outsideExceptions,
      repair_minutes: inPriority
        ? distribute(priorityRepairTotal, priorityCount, localIndex)
        : distribute(outsideRepair, outsideCount, localIndex),
    });
  }
}

function makePayments(accounts) {
  const rows = [];
  const otherAccounts = accounts
    .map((account) => account.account_id)
    .filter((accountId) => !["AC0024", "AC0027"].includes(accountId));
  const cycleOther = (index) => otherAccounts[index % otherAccounts.length];

  appendPaymentSegment(rows, {
    count: 79,
    priorityCount: 19,
    exceptionCount: 3,
    priorityExceptionCount: 1,
    repairTotal: 120,
    priorityRepairTotal: 53,
    dateForIndex: () => "2026-01-15",
    accountForIndex: () => "AC0027",
  });
  appendPaymentSegment(rows, {
    count: 45,
    priorityCount: 18,
    exceptionCount: 2,
    priorityExceptionCount: 2,
    repairTotal: 53,
    priorityRepairTotal: 53,
    dateForIndex: () => "2026-06-30",
    accountForIndex: cycleOther,
  });
  const juneDates = isoDates("2026-06-01", "2026-06-29");
  appendPaymentSegment(rows, {
    count: 1276,
    priorityCount: 454,
    exceptionCount: 62,
    priorityExceptionCount: 46,
    repairTotal: 2563,
    priorityRepairTotal: 1974,
    dateForIndex: (index) => juneDates[index % juneDates.length],
    accountForIndex: cycleOther,
  });
  appendPaymentSegment(rows, {
    count: 6200,
    priorityCount: 2348,
    exceptionCount: 412,
    priorityExceptionCount: 307,
    repairTotal: 17344,
    priorityRepairTotal: 12859,
    dateForIndex: () => "2026-02-15",
    accountForIndex: cycleOther,
  });
  return rows;
}

function makePayload() {
  const accounts = makeAccounts();
  return {
    meta: {
      period_start: "2026-01-01",
      period_end: "2026-06-30",
    },
    filtering: {
      dimensions: { accounts },
      facts: {
        account_days: compact(ACCOUNT_DAY_COLUMNS, makeAccountDays(accounts)),
        payments: compact(PAYMENT_COLUMNS, makePayments(accounts)),
      },
    },
  };
}

const payload = makePayload();

test("default state reproduces the governed full-period controls", () => {
  assert.deepEqual(FilterModel.createDefaultState(payload), {
    dateFrom: "2026-01-01",
    dateTo: "2026-06-30",
    currency: "",
    region: "",
    entity: "",
    bank: "",
  });

  const summary = FilterModel.summarize(payload);
  assert.equal(summary.scope.account_count, 55);
  assert.equal(summary.visibility.observations, 9955);
  assert.equal(summary.visibility.same_day_accounts, 32);
  assert.equal(summary.visibility.delayed_accounts, 23);
  assert.equal(summary.payments.overall.records, 7600);
  assert.equal(summary.payments.overall.exceptions, 479);
  assert.equal(summary.payments.overall.repair_minutes, 20080);
  assert.equal(summary.payments.priority_union.records, 2839);
  assert.equal(summary.payments.priority_union.exceptions, 356);
  assert.equal(summary.payments.priority_union.repair_minutes, 14939);
  assert.equal(summary.payments.priority_union.record_share_pct, 37.36);
  assert.equal(summary.payments.priority_union.exception_share_pct, 74.32);
  assert.equal(summary.payments.priority_union.repair_share_pct, 74.4);
  assert.equal(summary.liquidity.scenarios["7"].screen_usd, 42844787.78);
  assert.equal(summary.liquidity.scenarios["14"].screen_usd, 38127490.73);
  assert.equal(summary.closures.validation_candidates, 4);
  assert.equal(summary.closures.estimated_annual_fees_usd, 7800);
});

test("single-select dimension filters combine with AND semantics", () => {
  const summary = FilterModel.summarize(payload, {
    region: "EMEA",
    currency: "EUR",
    bank: "Pacific Crown",
  });
  assert.deepEqual(summary.scope.account_ids, ["AC0024", "AC0027"]);
  assert.equal(summary.visibility.accounts_total, 2);
  assert.equal(summary.visibility.observations, 362);
  assert.equal(summary.visibility.same_day_observations, 362);
  assert.equal(summary.payments.overall.records, 79);
  assert.equal(summary.payments.overall.exceptions, 3);
  assert.equal(summary.payments.overall.repair_minutes, 120);
  assert.equal(summary.payments.priority_union.records, 19);
  assert.equal(summary.payments.priority_union.exceptions, 1);
  assert.equal(summary.payments.priority_union.repair_minutes, 53);
  assert.equal(summary.payments.priority_union.record_share_pct, 24.05);
  assert.equal(summary.payments.priority_union.exception_share_pct, 33.33);
  assert.equal(summary.payments.priority_union.repair_share_pct, 44.17);
  assert.equal(summary.liquidity.scenarios["7"].screen_usd, 9571.396398);
  assert.equal(summary.liquidity.scenarios["14"].screen_usd, 9571.396398);
  assert.equal(summary.closures.validation_candidates, 1);
  assert.equal(summary.closures.estimated_annual_fees_usd, 2400);
});

test("an account with no supplied payments returns null shares rather than a false zero rate", () => {
  const summary = FilterModel.summarize(payload, { entity: "E006", bank: "Pacific Crown" });
  assert.deepEqual(summary.scope.account_ids, ["AC0024"]);
  assert.equal(summary.payments.overall.records, 0);
  assert.equal(summary.payments.priority_union.record_share_pct, null);
  assert.equal(summary.payments.priority_union.exception_share_pct, null);
  assert.equal(summary.payments.priority_union.repair_share_pct, null);
});

test("inclusive June and single-day date ranges retain both endpoints", () => {
  const june = FilterModel.summarize(payload, {
    dateFrom: "2026-06-01",
    dateTo: "2026-06-30",
  });
  assert.equal(june.visibility.observations, 1650);
  assert.equal(june.visibility.same_day_observations, 960);
  assert.equal(june.visibility.within_one_day_observations, 1230);
  assert.equal(june.payments.overall.records, 1321);
  assert.equal(june.payments.overall.exceptions, 64);
  assert.equal(june.payments.overall.repair_minutes, 2616);
  assert.equal(june.payments.priority_union.records, 472);
  assert.equal(june.payments.priority_union.exceptions, 48);
  assert.equal(june.payments.priority_union.repair_minutes, 2027);

  const singleDay = FilterModel.summarize(payload, {
    dateFrom: "2026-06-30",
    dateTo: "2026-06-30",
  });
  assert.equal(singleDay.visibility.observations, 55);
  assert.equal(singleDay.payments.overall.records, 45);
  assert.equal(singleDay.payments.overall.exceptions, 2);
  assert.equal(singleDay.payments.overall.repair_minutes, 53);
  assert.equal(singleDay.liquidity.as_of_date, "2026-06-30");
  assert.equal(singleDay.liquidity.scenarios["14"].screen_usd, 38127490.73);
});

test("liquidity horizons become available independently on their first complete dates", () => {
  const daySeven = FilterModel.summarize(payload, {
    dateFrom: "2026-01-07",
    dateTo: "2026-01-07",
  });
  assert.equal(daySeven.liquidity.panel_complete, true);
  assert.equal(daySeven.liquidity.base_complete, true);
  assert.equal(daySeven.liquidity.scenarios["7"].complete, true);
  assert.equal(daySeven.liquidity.scenarios["7"].screen_usd, 55);
  assert.equal(daySeven.liquidity.scenarios["14"].complete, false);
  assert.equal(daySeven.liquidity.scenarios["14"].buffer_usd, null);
  assert.equal(daySeven.liquidity.scenarios["14"].screen_usd, null);
  assert.equal(daySeven.liquidity.complete, false);

  const dayFourteen = FilterModel.summarize(payload, {
    dateFrom: "2026-01-14",
    dateTo: "2026-01-14",
  });
  assert.equal(dayFourteen.liquidity.base_complete, true);
  assert.equal(dayFourteen.liquidity.scenarios["7"].complete, true);
  assert.equal(dayFourteen.liquidity.scenarios["14"].complete, true);
  assert.equal(dayFourteen.liquidity.scenarios["7"].screen_usd, 55);
  assert.equal(dayFourteen.liquidity.scenarios["14"].screen_usd, 55);
  assert.equal(dayFourteen.liquidity.complete, true);
});

test("invalid dates and array-valued dimensions fail before summary derivation", () => {
  assert.throws(
    () => FilterModel.summarize(payload, { dateFrom: "2026-06-30", dateTo: "2026-06-01" }),
    (error) => error instanceof FilterModel.FilterModelError && error.code === "invalid_date_range",
  );
  assert.throws(
    () => FilterModel.summarize(payload, { dateFrom: "2026-02-30" }),
    (error) => error instanceof FilterModel.FilterModelError && error.code === "invalid_date",
  );
  assert.throws(
    () => FilterModel.summarize(payload, { currency: ["EUR", "USD"] }),
    (error) => error instanceof FilterModel.FilterModelError && error.code === "invalid_state",
  );
});

test("empty intersections preserve null rates and incomplete liquidity", () => {
  const summary = FilterModel.summarize(payload, { region: "EMEA", currency: "JPY" });
  assert.equal(summary.scope.has_matches, false);
  assert.equal(summary.visibility.same_day_rate_pct, null);
  assert.equal(summary.payments.priority_union.record_share_pct, null);
  assert.equal(summary.liquidity.complete, false);
  assert.equal(summary.liquidity.scenarios["7"].screen_usd, null);
  assert.equal(summary.liquidity.scenarios["14"].screen_usd, null);
});

test("liquidity summary deliberately excludes mobility and funded-case claims", () => {
  const liquidity = FilterModel.summarize(payload).liquidity;
  assert.equal(Object.hasOwn(liquidity, "validated_mobility"), false);
  assert.equal(Object.hasOwn(liquidity, "funded_case"), false);
  assert.doesNotMatch(JSON.stringify(liquidity), /mobility|funded/iu);
});

test("reset creates a fresh default state and options preserve literal NA", () => {
  const reset = FilterModel.resetState(payload);
  const secondReset = FilterModel.resetState(payload);
  assert.deepEqual(reset, FilterModel.createDefaultState(payload));
  assert.notEqual(reset, secondReset);
  reset.region = "EMEA";
  assert.equal(secondReset.region, "");

  const options = FilterModel.getFilterOptions(payload);
  assert.ok(options.regions.includes("NA"));
  assert.ok(options.currencies.includes("EUR"));
  assert.ok(options.banks.includes("Pacific Crown"));
  assert.ok(options.entities.some((entity) => entity.value === "E006" && entity.label === "Aurelius Germany"));
});

test("search matches metric definitions and dimension/account values with literal tokens", () => {
  const index = FilterModel.buildSearchIndex(payload);
  const metricResults = FilterModel.querySearchIndex(index, "screening sensitivity");
  assert.ok(metricResults.some((entry) => entry.kind === "metric" && entry.id === "liquidity-screen"));

  const accountResults = FilterModel.querySearchIndex(index, "EMEA Pacific", { limit: 100 });
  assert.deepEqual(
    accountResults.filter((entry) => entry.kind === "account").map((entry) => entry.id),
    ["AC0024", "AC0027"],
  );
  assert.ok(FilterModel.querySearchIndex(index, "ac0024").some((entry) => entry.id === "AC0024"));
  assert.deepEqual(FilterModel.querySearchIndex(index, "["), []);
  assert.deepEqual(FilterModel.querySearchIndex(index, "   "), []);
});

test("a missing 14-day value preserves complete base and 7-day results", () => {
  const incomplete = structuredClone(payload);
  const columns = incomplete.filtering.facts.account_days.columns;
  const dateIndex = columns.indexOf("date");
  const accountIndex = columns.indexOf("account_id");
  const bufferIndex = columns.indexOf("unflagged_payment_buffer_14d_usd");
  const row = incomplete.filtering.facts.account_days.rows.find(
    (values) => values[dateIndex] === "2026-06-30" && values[accountIndex] === "AC0001",
  );
  row[bufferIndex] = null;

  const summary = FilterModel.summarize(incomplete);
  assert.equal(summary.liquidity.complete, false);
  assert.equal(summary.liquidity.panel_complete, true);
  assert.equal(summary.liquidity.base_complete, true);
  assert.equal(summary.liquidity.positive_available_usd, 57801215.46);
  assert.equal(summary.liquidity.scenarios["7"].complete, true);
  assert.equal(summary.liquidity.scenarios["7"].screen_usd, 42844787.78);
  assert.equal(summary.liquidity.scenarios["14"].complete, false);
  assert.equal(summary.liquidity.scenarios["14"].buffer_usd, null);
  assert.equal(summary.liquidity.scenarios["14"].screen_usd, null);
});

test("unknown priority cohort values fail closed", () => {
  const invalid = structuredClone(payload);
  const columns = invalid.filtering.facts.payments.columns;
  invalid.filtering.facts.payments.rows[0][columns.indexOf("priority_cohort")] = "Priority-ish";
  assert.throws(
    () => FilterModel.summarize(invalid),
    /Unknown priority cohort/u,
  );
});
