"""Pure-function unit economics calculator.

All inputs are annual unless noted. Raises ValueError on bad input
(negatives, non-numbers, zero where division needs a positive).
"""

import math
import numbers


def _check(name, value, allow_zero=True):
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError("%s must be a number, got %r" % (name, value))
    if value < 0:
        raise ValueError("%s cannot be negative, got %r" % (name, value))
    if not allow_zero and value == 0:
        raise ValueError("%s must be greater than zero" % name)
    return float(value)


def calculate_economics(
    price_per_unit,
    units_per_customer_per_year,
    customers,
    variable_cost_per_unit,
    fixed_costs_annual,
    cac,
    avg_customer_years,
):
    """Return a dict of unit economics. See module docstring for validation."""
    price = _check("price_per_unit", price_per_unit)
    units = _check("units_per_customer_per_year", units_per_customer_per_year)
    cust = _check("customers", customers)
    var_cost = _check("variable_cost_per_unit", variable_cost_per_unit)
    fixed = _check("fixed_costs_annual", fixed_costs_annual)
    cac = _check("cac", cac)
    years = _check("avg_customer_years", avg_customer_years, allow_zero=False)

    annual_revenue = price * units * cust
    total_variable_cost = var_cost * units * cust
    gross_profit = annual_revenue - total_variable_cost
    gross_margin_pct = (gross_profit / annual_revenue * 100) if annual_revenue > 0 else 0.0
    contribution = gross_profit - fixed

    contribution_per_customer = (price - var_cost) * units
    if contribution_per_customer > 0:
        break_even_customers = math.ceil(fixed / contribution_per_customer)
    else:
        break_even_customers = None

    ltv = contribution_per_customer * years
    ltv_cac_ratio = (ltv / cac) if cac > 0 else None

    monthly_contribution = contribution_per_customer / 12
    if monthly_contribution > 0 and cac > 0:
        cac_payback_months = cac / monthly_contribution
    else:
        cac_payback_months = None

    return {
        "annual_revenue": annual_revenue,
        "total_variable_cost": total_variable_cost,
        "gross_profit": gross_profit,
        "gross_margin_pct": gross_margin_pct,
        "contribution": contribution,
        "break_even_customers": break_even_customers,
        "ltv": ltv,
        "ltv_cac_ratio": ltv_cac_ratio,
        "cac_payback_months": cac_payback_months,
    }
