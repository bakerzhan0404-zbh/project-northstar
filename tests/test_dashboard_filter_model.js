"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const FilterModel = require(path.join(__dirname, "..", "docs", "dashboard", "filter_model.js"));

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

function findCompactRow(table, criteria) {
  const indexes = Object.fromEntries(
    Object.keys(criteria).map((column) => [column, table.columns.indexOf(column)]),
  );
  const row = table.rows.find((values) => (
    Object.entries(criteria).every(([column, expected]) => values[indexes[column]] === expected)
  ));
  assert.ok(row, `Expected compact row matching ${JSON.stringify(criteria)}`);
  return row;
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
  assert.equal(summary.visibility.same_day_account_share_pct, 58.18);
  assert.equal(summary.visibility.delayed_account_share_pct, 41.82);
  assert.deepEqual(
    summary.visibility.by_method.map((method) => ({
      method: method.method,
      accounts: method.accounts_total,
      account_share_pct: method.account_share_pct,
      observations: method.observations,
      maximum_delay_days: method.maximum_delay_days,
    })),
    [
      { method: "API", accounts: 30, account_share_pct: 54.55, observations: 5430, maximum_delay_days: 0 },
      { method: "Host-to-host", accounts: 1, account_share_pct: 1.82, observations: 181, maximum_delay_days: 0 },
      { method: "Portal", accounts: 9, account_share_pct: 16.36, observations: 1629, maximum_delay_days: 1 },
      { method: "Spreadsheet", accounts: 15, account_share_pct: 27.27, observations: 2715, maximum_delay_days: 2 },
    ],
  );
  assert.equal(summary.payments.overall.records, 7600);
  assert.equal(summary.payments.overall.exceptions, 479);
  assert.equal(summary.payments.overall.repair_minutes, 20080);
  assert.equal(summary.payments.overall.exception_rate_pct, 6.3);
  assert.equal(summary.payments.priority_union.records, 2839);
  assert.equal(summary.payments.priority_union.exceptions, 356);
  assert.equal(summary.payments.priority_union.repair_minutes, 14939);
  assert.equal(summary.payments.priority_union.record_share_pct, 37.36);
  assert.equal(summary.payments.priority_union.exception_share_pct, 74.32);
  assert.equal(summary.payments.priority_union.repair_share_pct, 74.4);
  assert.equal(summary.payments.priority_union.exception_rate_pct, 12.54);
  assert.deepEqual(summary.payments.cohort_order, [
    "Manual touch only",
    "Manual touch + cross-border wire",
    "Cross-border wire only",
    "Neither priority cohort",
  ]);
  assert.deepEqual(summary.payments.cohorts["Manual touch only"], {
    records: 2839,
    exceptions: 356,
    repair_minutes: 14939,
    record_contribution_pct: 37.36,
    exception_contribution_pct: 74.32,
    repair_contribution_pct: 74.4,
    exception_rate_pct: 12.54,
  });
  assert.deepEqual(summary.payments.cohorts["Manual touch + cross-border wire"], {
    records: 0,
    exceptions: 0,
    repair_minutes: 0,
    record_contribution_pct: 0,
    exception_contribution_pct: 0,
    repair_contribution_pct: 0,
    exception_rate_pct: null,
  });
  assert.equal(summary.liquidity.scenarios["7"].screen_usd, 42844787.78);
  assert.equal(summary.liquidity.scenarios["14"].screen_usd, 38127490.73);
  assert.equal(summary.closures.accounts_total, 55);
  assert.equal(summary.closures.validation_candidates, 4);
  assert.equal(summary.closures.non_candidates, 51);
  assert.equal(summary.closures.candidate_share_pct, 7.27);
  assert.equal(summary.closures.total_annual_fees_usd, 53700);
  assert.equal(summary.closures.estimated_annual_fees_usd, 7800);
  assert.equal(summary.closures.candidate_fee_share_pct, 14.53);
  assert.deepEqual(summary.closures.candidate_account_ids, ["AC0004", "AC0009", "AC0024", "AC0037"]);
});

test("regional facets reconcile the governed full-period dashboard data", () => {
  const actualPayload = JSON.parse(fs.readFileSync(
    path.join(__dirname, "..", "docs", "dashboard", "dashboard_data.json"),
    "utf8",
  ));
  const summary = FilterModel.summarize(actualPayload);

  assert.deepEqual(summary.regional.order, ["NA", "EMEA", "APAC"]);
  assert.equal(summary.regional.selected_region, null);
  assert.equal(summary.regional.region_filter_mode, "facet_override");
  assert.deepEqual(summary.regional.basis, {
    date_from: "2026-01-01",
    date_to: "2026-06-30",
    currency: null,
    entity: null,
    bank: null,
    account_count: 55,
    regions_represented: 3,
  });

  const controls = {
    NA: {
      label: "North America",
      accounts: 16,
      delayed: 7,
      accountDays: 2896,
      sameDay: 1629,
      sameDayRate: 56.25,
      records: 1934,
      priority: 713,
      priorityShare: 36.87,
      screen7: 15861417.406434,
      screen14: 14592195.604284,
      candidates: 2,
      fees: 4500,
    },
    EMEA: {
      label: "Europe, Middle East and Africa",
      accounts: 17,
      delayed: 8,
      accountDays: 3077,
      sameDay: 1629,
      sameDayRate: 52.94,
      records: 2353,
      priority: 958,
      priorityShare: 40.71,
      screen7: 18146838.600586,
      screen14: 15481097.288276,
      candidates: 1,
      fees: 2400,
    },
    APAC: {
      label: "Asia Pacific",
      accounts: 22,
      delayed: 8,
      accountDays: 3982,
      sameDay: 2534,
      sameDayRate: 63.64,
      records: 3313,
      priority: 1168,
      priorityShare: 35.26,
      screen7: 8836531.775847,
      screen14: 8054197.835004,
      candidates: 1,
      fees: 900,
    },
  };

  summary.regional.rows.forEach((row) => {
    const expected = controls[row.code];
    assert.equal(row.label, expected.label);
    assert.equal(row.status, "available");
    assert.equal(row.selected, false);
    assert.equal(row.account_count, expected.accounts);
    assert.equal(row.visibility.delayed_accounts, expected.delayed);
    assert.equal(row.visibility.account_days, expected.accountDays);
    assert.equal(row.visibility.same_day_account_days, expected.sameDay);
    assert.equal(row.visibility.same_day_rate_pct, expected.sameDayRate);
    assert.equal(row.payments.records, expected.records);
    assert.equal(row.payments.priority_union_records, expected.priority);
    assert.equal(row.payments.priority_union_record_share_pct, expected.priorityShare);
    assert.equal(row.liquidity.scenarios["7"].screen_usd, expected.screen7);
    assert.equal(row.liquidity.scenarios["14"].screen_usd, expected.screen14);
    assert.equal(row.closures.validation_candidates, expected.candidates);
    assert.equal(row.closures.estimated_annual_fees_usd, expected.fees);
  });

  assert.equal(summary.regional.rows.reduce((total, row) => total + row.account_count, 0), 55);
  assert.equal(summary.regional.rows.reduce((total, row) => total + row.visibility.delayed_accounts, 0), 23);
  assert.equal(summary.regional.rows.reduce((total, row) => total + row.visibility.same_day_account_days, 0), 5792);
  assert.equal(summary.regional.rows.reduce((total, row) => total + row.payments.records, 0), 7600);
  assert.equal(summary.regional.rows.reduce((total, row) => total + row.payments.exceptions, 0), 479);
  assert.equal(summary.regional.rows.reduce((total, row) => total + row.payments.repair_minutes, 0), 20080);
  assert.equal(summary.regional.rows.reduce((total, row) => total + row.payments.priority_union_records, 0), 2839);
  assert.equal(summary.regional.rows.reduce((total, row) => total + row.closures.validation_candidates, 0), 4);
  assert.equal(summary.regional.rows.reduce((total, row) => total + row.closures.estimated_annual_fees_usd, 0), 7800);
});

test("regional facets hold non-region filters constant while exposing region selection", () => {
  const active = FilterModel.summarize(payload, { region: "EMEA" });
  const emea = active.regional.rows.find((row) => row.code === "EMEA");
  assert.equal(active.regional.selected_region, "EMEA");
  assert.equal(emea.selected, true);
  assert.equal(emea.account_count, active.scope.account_count);
  assert.equal(emea.visibility.delayed_accounts, active.visibility.delayed_accounts);
  assert.equal(emea.payments.records, active.payments.overall.records);
  assert.equal(active.regional.rows.find((row) => row.code === "NA").status, "available");

  const narrowed = FilterModel.summarize(payload, { currency: "EUR", bank: "Pacific Crown" });
  assert.deepEqual(
    narrowed.regional.rows.map((row) => [row.code, row.status, row.account_count]),
    [
      ["NA", "no_matching_accounts", 0],
      ["EMEA", "available", 2],
      ["APAC", "no_matching_accounts", 0],
    ],
  );
  const narrowedEmea = narrowed.regional.rows[1];
  assert.equal(narrowedEmea.visibility.delayed_accounts, 0);
  assert.equal(narrowedEmea.payments.records, 79);
  assert.equal(narrowedEmea.liquidity.scenarios["14"].screen_usd, 9571.396398);
  assert.equal(narrowedEmea.closures.validation_candidates, 1);
  assert.equal(narrowedEmea.closures.estimated_annual_fees_usd, 2400);
  assert.equal(narrowed.regional.rows[0].visibility.same_day_rate_pct, null);
  assert.equal(narrowed.regional.rows[0].liquidity.scenarios["14"].screen_usd, null);
});

test("liquidity visualization summaries reconcile account-floor waterfalls and preserve daily gaps", () => {
  const liquidity = FilterModel.summarize(payload).liquidity;
  assert.deepEqual(Object.keys(liquidity.waterfalls), ["7", "14"]);
  assert.deepEqual(
    liquidity.waterfalls["7"].steps.map((step) => ({
      key: step.key,
      role: step.role,
      delta_usd: step.delta_usd,
      total_usd: step.total_usd,
    })),
    [
      {
        key: "gross_positive_estimated_availability",
        role: "starting_total",
        delta_usd: 57801215.46,
        total_usd: 57801215.46,
      },
      {
        key: "preliminary_restrictions",
        role: "deduction",
        delta_usd: -8053700.97,
        total_usd: 49747514.49,
      },
      {
        key: "negative_positions",
        role: "deduction",
        delta_usd: -2138293.09,
        total_usd: 47609221.4,
      },
      {
        key: "apparent_net_before_buffer",
        role: "subtotal",
        delta_usd: null,
        total_usd: 47609221.4,
      },
      {
        key: "effective_buffer_after_account_floors",
        role: "deduction",
        delta_usd: -4764433.62,
        total_usd: 42844787.78,
      },
      {
        key: "modeled_screen",
        role: "resulting_total",
        delta_usd: null,
        total_usd: 42844787.78,
      },
    ],
  );
  assert.equal(liquidity.waterfalls["7"].raw_buffer_usd, 5485896.33);
  assert.equal(liquidity.waterfalls["7"].effective_buffer_deduction_usd, 4764433.62);
  assert.equal(liquidity.waterfalls["7"].unapplied_buffer_due_to_floor_usd, 721462.71);
  assert.equal(liquidity.waterfalls["14"].raw_buffer_usd, 10828186.91);
  assert.equal(liquidity.waterfalls["14"].effective_buffer_deduction_usd, 9481730.67);
  assert.equal(liquidity.waterfalls["14"].unapplied_buffer_due_to_floor_usd, 1346456.24);
  assert.equal(liquidity.waterfalls["14"].steps.at(-1).total_usd, 38127490.73);

  assert.equal(liquidity.trend.length, 181);
  assert.equal(liquidity.trend[0].date, "2026-01-01");
  assert.equal(liquidity.trend[0].base_complete, true);
  assert.equal(liquidity.trend[0].scenarios["7"].screen_usd, null);
  assert.equal(liquidity.trend[0].scenarios["14"].screen_usd, null);
  assert.equal(liquidity.trend.filter((point) => point.scenarios["7"].complete).length, 175);
  assert.equal(liquidity.trend.find((point) => point.scenarios["7"].complete).date, "2026-01-07");
  assert.equal(liquidity.trend.filter((point) => point.scenarios["14"].complete).length, 168);
  assert.equal(liquidity.trend.find((point) => point.scenarios["14"].complete).date, "2026-01-14");
  assert.equal(liquidity.trend.at(-1).date, "2026-06-30");
  assert.equal(liquidity.trend.at(-1).scenarios["7"].screen_usd, 42844787.78);
  assert.equal(liquidity.trend.at(-1).scenarios["14"].screen_usd, 38127490.73);
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
  assert.deepEqual(
    summary.visibility.by_method.map((method) => [method.method, method.accounts_total, method.account_share_pct]),
    [
      ["API", 1, 50],
      ["Host-to-host", 1, 50],
      ["Portal", 0, 0],
      ["Spreadsheet", 0, 0],
    ],
  );
  assert.equal(summary.payments.overall.records, 79);
  assert.equal(summary.payments.overall.exceptions, 3);
  assert.equal(summary.payments.overall.repair_minutes, 120);
  assert.equal(summary.payments.overall.exception_rate_pct, 3.8);
  assert.equal(summary.payments.priority_union.records, 19);
  assert.equal(summary.payments.priority_union.exceptions, 1);
  assert.equal(summary.payments.priority_union.repair_minutes, 53);
  assert.equal(summary.payments.priority_union.record_share_pct, 24.05);
  assert.equal(summary.payments.priority_union.exception_share_pct, 33.33);
  assert.equal(summary.payments.priority_union.repair_share_pct, 44.17);
  assert.equal(summary.payments.priority_union.exception_rate_pct, 5.26);
  assert.deepEqual(summary.payments.cohorts["Manual touch only"], {
    records: 19,
    exceptions: 1,
    repair_minutes: 53,
    record_contribution_pct: 24.05,
    exception_contribution_pct: 33.33,
    repair_contribution_pct: 44.17,
    exception_rate_pct: 5.26,
  });
  assert.deepEqual(summary.payments.cohorts["Neither priority cohort"], {
    records: 60,
    exceptions: 2,
    repair_minutes: 67,
    record_contribution_pct: 75.95,
    exception_contribution_pct: 66.67,
    repair_contribution_pct: 55.83,
    exception_rate_pct: 3.33,
  });
  assert.equal(summary.liquidity.scenarios["7"].screen_usd, 9571.396398);
  assert.equal(summary.liquidity.scenarios["14"].screen_usd, 9571.396398);
  assert.equal(summary.liquidity.waterfalls["7"].effective_buffer_deduction_usd, 0);
  assert.equal(summary.liquidity.waterfalls["14"].effective_buffer_deduction_usd, 0);
  assert.equal(summary.liquidity.waterfalls["14"].steps.at(-1).total_usd, 9571.396398);
  assert.equal(summary.closures.accounts_total, 2);
  assert.equal(summary.closures.validation_candidates, 1);
  assert.equal(summary.closures.non_candidates, 1);
  assert.equal(summary.closures.candidate_share_pct, 50);
  assert.equal(summary.closures.total_annual_fees_usd, 3300);
  assert.equal(summary.closures.estimated_annual_fees_usd, 2400);
  assert.equal(summary.closures.candidate_fee_share_pct, 72.73);
  assert.deepEqual(summary.closures.candidate_accounts, [{
    account_id: "AC0024",
    entity_id: "E006",
    entity_name: "Aurelius Germany",
    region: "EMEA",
    currency: "EUR",
    bank_name: "Pacific Crown",
    visibility_method: "Host-to-host",
    annual_fee_usd: 2400,
  }]);
});

test("an account with no supplied payments returns null shares rather than a false zero rate", () => {
  const summary = FilterModel.summarize(payload, { entity: "E006", bank: "Pacific Crown" });
  assert.deepEqual(summary.scope.account_ids, ["AC0024"]);
  assert.equal(summary.payments.overall.records, 0);
  assert.equal(summary.payments.overall.exception_rate_pct, null);
  assert.equal(summary.payments.priority_union.record_share_pct, null);
  assert.equal(summary.payments.priority_union.exception_share_pct, null);
  assert.equal(summary.payments.priority_union.repair_share_pct, null);
  assert.equal(summary.payments.priority_union.exception_rate_pct, null);
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
  assert.equal(singleDay.liquidity.trend.length, 1);
  assert.equal(singleDay.liquidity.trend[0].date, "2026-06-30");
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

test("unknown account regions fail closed even when a filter excludes the mutated account", () => {
  const invalid = structuredClone(payload);
  invalid.filtering.dimensions.accounts[0].region = "LATAM";
  assert.throws(
    () => FilterModel.summarize(invalid, { currency: "EUR" }),
    /Unknown account region: LATAM/u,
  );
});

test("empty intersections preserve null rates and incomplete liquidity", () => {
  const summary = FilterModel.summarize(payload, { region: "EMEA", currency: "JPY" });
  assert.equal(summary.scope.has_matches, false);
  assert.equal(summary.visibility.same_day_rate_pct, null);
  assert.equal(summary.visibility.same_day_account_share_pct, null);
  assert.equal(summary.visibility.delayed_account_share_pct, null);
  assert.deepEqual(
    summary.visibility.by_method.map((method) => [method.method, method.accounts_total, method.account_share_pct]),
    [
      ["API", 0, null],
      ["Host-to-host", 0, null],
      ["Portal", 0, null],
      ["Spreadsheet", 0, null],
    ],
  );
  assert.equal(summary.payments.priority_union.record_share_pct, null);
  assert.equal(summary.payments.overall.exception_rate_pct, null);
  assert.equal(summary.payments.priority_union.exception_rate_pct, null);
  for (const cohort of summary.payments.cohort_order) {
    assert.equal(summary.payments.cohorts[cohort].record_contribution_pct, null);
    assert.equal(summary.payments.cohorts[cohort].exception_contribution_pct, null);
    assert.equal(summary.payments.cohorts[cohort].repair_contribution_pct, null);
    assert.equal(summary.payments.cohorts[cohort].exception_rate_pct, null);
  }
  assert.equal(summary.liquidity.complete, false);
  assert.equal(summary.liquidity.scenarios["7"].screen_usd, null);
  assert.equal(summary.liquidity.scenarios["14"].screen_usd, null);
  for (const horizon of ["7", "14"]) {
    assert.equal(summary.liquidity.waterfalls[horizon].complete, false);
    assert.equal(summary.liquidity.waterfalls[horizon].raw_buffer_usd, null);
    assert.ok(summary.liquidity.waterfalls[horizon].steps.every((step) => (
      step.delta_usd === null && step.total_usd === null
    )));
  }
  assert.equal(summary.liquidity.trend.length, 181);
  assert.ok(summary.liquidity.trend.every((point) => (
    point.base_complete === false
      && point.positive_available_usd === null
      && point.scenarios["7"].screen_usd === null
      && point.scenarios["14"].screen_usd === null
  )));
  assert.equal(summary.closures.accounts_total, 0);
  assert.equal(summary.closures.validation_candidates, 0);
  assert.equal(summary.closures.non_candidates, 0);
  assert.equal(summary.closures.candidate_share_pct, null);
  assert.equal(summary.closures.total_annual_fees_usd, 0);
  assert.equal(summary.closures.estimated_annual_fees_usd, 0);
  assert.equal(summary.closures.candidate_fee_share_pct, null);
  assert.deepEqual(summary.closures.candidate_accounts, []);
  assert.equal(summary.regional.basis.account_count, 22);
  assert.equal(summary.regional.basis.regions_represented, 1);
  assert.deepEqual(
    summary.regional.rows.map((row) => [row.code, row.status, row.account_count, row.selected]),
    [
      ["NA", "no_matching_accounts", 0, false],
      ["EMEA", "no_matching_accounts", 0, true],
      ["APAC", "available", 22, false],
    ],
  );
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
  assert.equal(summary.liquidity.waterfalls["7"].complete, true);
  assert.equal(summary.liquidity.waterfalls["14"].complete, false);
  assert.ok(summary.liquidity.waterfalls["14"].steps.every((step) => (
    step.delta_usd === null && step.total_usd === null
  )));
  assert.equal(summary.liquidity.trend.at(-1).scenarios["7"].complete, true);
  assert.equal(summary.liquidity.trend.at(-1).scenarios["14"].complete, false);
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

test("visualization fact domains and reconciliations fail closed on mutation", () => {
  const mutations = [
    {
      label: "unknown visibility method",
      change(invalid) {
        invalid.filtering.dimensions.accounts[0].visibility_method = "Email";
      },
      message: /Unknown visibility method/u,
    },
    {
      label: "fractional reporting delay",
      change(invalid) {
        const table = invalid.filtering.facts.account_days;
        const row = findCompactRow(table, { date: "2026-01-01", account_id: "AC0001" });
        row[table.columns.indexOf("reporting_delay_days")] = 1.5;
      },
      message: /reporting_delay_days must be an integer from 0 to 3/u,
    },
    {
      label: "restriction above positive availability",
      change(invalid) {
        const table = invalid.filtering.facts.account_days;
        const row = findCompactRow(table, { date: "2026-01-01", account_id: "AC0001" });
        row[table.columns.indexOf("restricted_positive_available_usd")] = 2;
      },
      message: /restrictions exceed positive availability/u,
    },
    {
      label: "positive negative-position value",
      change(invalid) {
        const table = invalid.filtering.facts.account_days;
        const row = findCompactRow(table, { date: "2026-01-01", account_id: "AC0001" });
        row[table.columns.indexOf("negative_available_usd")] = 1;
      },
      message: /negative availability must be nonpositive/u,
    },
    {
      label: "negative payment buffer",
      change(invalid) {
        const table = invalid.filtering.facts.account_days;
        const row = findCompactRow(table, { date: "2026-06-30", account_id: "AC0002" });
        row[table.columns.indexOf("unflagged_payment_buffer_7d_usd")] = -1;
      },
      message: /unflagged_payment_buffer_7d_usd must be nonnegative/u,
    },
    {
      label: "screen inconsistent with account floor",
      change(invalid) {
        const table = invalid.filtering.facts.account_days;
        const row = findCompactRow(table, { date: "2026-06-30", account_id: "AC0002" });
        row[table.columns.indexOf("net_screen_contribution_7d_usd")] = 1;
      },
      message: /7-day screen does not reconcile to the account-level floor/u,
    },
    {
      label: "missing account-day row",
      change(invalid) {
        invalid.filtering.facts.account_days.rows.pop();
      },
      message: /one row per account and calendar date/u,
    },
    {
      label: "fractional repair minutes",
      change(invalid) {
        const table = invalid.filtering.facts.payments;
        table.rows[0][table.columns.indexOf("repair_minutes")] = 0.5;
      },
      message: /repair_minutes must be an integer/u,
    },
  ];

  for (const mutation of mutations) {
    const invalid = structuredClone(payload);
    mutation.change(invalid);
    assert.throws(
      () => FilterModel.summarize(invalid),
      mutation.message,
      mutation.label,
    );
  }
});
