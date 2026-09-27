"""Tests for bmc.unit_economics: math and input validation."""

import math

import pytest

from bmc.unit_economics import calculate_economics
from bmc.sample import SAMPLE_ECONOMICS

BASE = dict(
    price_per_unit=49,
    units_per_customer_per_year=240,
    customers=120,
    variable_cost_per_unit=6,
    fixed_costs_annual=850000,
    cac=1800,
    avg_customer_years=3.5,
)


def test_annual_revenue():
    r = calculate_economics(**BASE)
    assert r["annual_revenue"] == 49 * 240 * 120 == 1411200


def test_gross_profit_and_margin():
    r = calculate_economics(**BASE)
    assert r["total_variable_cost"] == 6 * 240 * 120 == 172800
    assert r["gross_profit"] == 1411200 - 172800 == 1238400
    assert r["gross_margin_pct"] == pytest.approx(1238400 / 1411200 * 100)


def test_break_even_customers():
    r = calculate_economics(**BASE)
    # contribution per customer = (49-6)*240 = 10320; 850000/10320 = 82.36 -> 83
    assert r["break_even_customers"] == 83
    assert r["break_even_customers"] == math.ceil(850000 / 10320)


def test_ltv_and_ltv_cac():
    r = calculate_economics(**BASE)
    assert r["ltv"] == pytest.approx(10320 * 3.5) == pytest.approx(36120)
    assert r["ltv_cac_ratio"] == pytest.approx(36120 / 1800)


def test_cac_payback_months():
    r = calculate_economics(**BASE)
    assert r["cac_payback_months"] == pytest.approx(1800 / (10320 / 12))


def test_contribution_subtracts_fixed_costs():
    r = calculate_economics(**BASE)
    assert r["contribution"] == pytest.approx(1238400 - 850000)


def test_zero_customers_gives_zero_revenue_and_margin():
    args = dict(BASE, customers=0)
    r = calculate_economics(**args)
    assert r["annual_revenue"] == 0
    assert r["gross_margin_pct"] == 0.0
    assert r["break_even_customers"] == 83  # fixed costs still need covering


def test_no_contribution_margin_gives_no_break_even():
    args = dict(BASE, price_per_unit=6, variable_cost_per_unit=6)
    r = calculate_economics(**args)
    assert r["break_even_customers"] is None
    assert r["ltv"] == 0
    assert r["cac_payback_months"] is None


def test_zero_cac_gives_no_ratios():
    args = dict(BASE, cac=0)
    r = calculate_economics(**args)
    assert r["ltv_cac_ratio"] is None
    assert r["cac_payback_months"] is None


def test_negative_input_raises():
    with pytest.raises(ValueError):
        calculate_economics(**dict(BASE, price_per_unit=-5))


def test_zero_customer_years_raises():
    with pytest.raises(ValueError):
        calculate_economics(**dict(BASE, avg_customer_years=0))


def test_non_number_raises():
    with pytest.raises(ValueError):
        calculate_economics(**dict(BASE, customers="lots"))


def test_sample_economics_run_clean():
    r = calculate_economics(**SAMPLE_ECONOMICS)
    assert r["annual_revenue"] > 0
    assert r["ltv_cac_ratio"] > 3  # healthy sample business
