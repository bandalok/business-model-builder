"""SampleCo: a filled-in realistic sample canvas.

SampleCo is a fictional B2B SaaS company selling team analytics at
$49 per seat per month. Used by the test suite and preloaded in the
web demo so it is useful on first open.
"""

SAMPLE_MODEL = {
    "customer_segments": (
        "Heads of engineering and product operations at software companies "
        "with 50 to 500 employees. About 40,000 such companies exist in the "
        "US and Europe. We start with engineering leaders because they feel "
        "the reporting pain every sprint review."
    ),
    "value_propositions": (
        "Engineering leaders get a clear weekly picture of team output "
        "without chasing status updates. SampleCo pulls data from tools "
        "like Jira and GitHub and turns it into one dashboard the whole "
        "team trusts. Managers stop spending Friday afternoons building "
        "spreadsheet reports by hand."
    ),
    "channels": (
        "Content marketing: a weekly newsletter read by 12,000 engineering "
        "managers. Product-led signup with a 14-day free trial. Two "
        "integration partners, Jira and GitHub marketplaces, list us in "
        "their directories. A 3-person sales team closes deals over 50 seats."
    ),
    "customer_relationships": (
        "Self-serve onboarding with a setup checklist that most teams finish "
        "in under an hour. A customer success manager is assigned to every "
        "account over 50 seats. Quarterly business reviews for accounts over "
        "$10,000 per year keep renewals above 90%."
    ),
    "revenue_streams": (
        "Subscription at $49 per seat per month, billed annually. Average "
        "customer starts with 20 seats, about $11,760 per year. A $499 per "
        "month enterprise tier adds single sign-on and audit logs. Services "
        "revenue is zero on purpose: the product must sell itself."
    ),
    "key_resources": (
        "The analytics engine that cleans and joins data from 8 integrations. "
        "A data pipeline team of 6 engineers. Brand trust from 400 published "
        "customer case metrics. SOC 2 certification, renewed every year."
    ),
    "key_activities": (
        "Shipping product improvements to the dashboard every two weeks. "
        "Maintaining the 8 data integrations so they never break. Publishing "
        "one useful engineering-management article per week. Supporting "
        "trial users within 4 business hours."
    ),
    "key_partnerships": (
        "Jira and GitHub list us in their marketplaces and drive 30% of "
        "trials. AWS hosts everything; if prices rose 20% we would move "
        "batch jobs to a second cloud provider within a quarter. Stripe "
        "handles all billing."
    ),
    "cost_structure": (
        "Biggest costs: 14-person team at about $2.1M per year, AWS hosting "
        "at $180,000 per year, and marketing spend of $240,000 per year. "
        "Variable cost per seat per month is about $6 for hosting and support. "
        "Fixed costs run about $850,000 per year excluding the team."
    ),
}

# Unit economics inputs for SampleCo.
# Unit = one seat for one month. Average customer: 20 seats x 12 months.
SAMPLE_ECONOMICS = {
    "price_per_unit": 49,
    "units_per_customer_per_year": 240,
    "customers": 120,
    "variable_cost_per_unit": 6,
    "fixed_costs_annual": 850000,
    "cac": 1800,
    "avg_customer_years": 3.5,
}
