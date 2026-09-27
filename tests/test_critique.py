"""Tests for bmc.critique: scoring, penalties, rewards, cross-block checks."""

import pytest

from bmc.blocks import block_ids
from bmc.critique import critique_model, score_block
from bmc.sample import SAMPLE_MODEL


def blank_canvas():
    return {bid: "" for bid in block_ids()}


def test_empty_canvas_scores_zero():
    result = critique_model(blank_canvas())
    assert result["overall_score"] == 0
    assert all(v == 0 for v in result["per_block"].values())


def test_empty_block_scores_zero():
    assert score_block("") == 0
    assert score_block("   ") == 0


def test_vague_text_penalized():
    specific = (
        "Engineering managers at software companies with 50 to 500 staff. "
        "About 40000 companies. They pay $49 per seat per month."
    )
    vague = (
        "Everyone who wants the best world-class revolutionary solution. "
        "Anyone can use it. It is the best."
    )
    assert len(specific.split()) >= len(vague.split()) - 5
    assert score_block(specific) > score_block(vague)


def test_numbers_rewarded():
    plain = (
        "We charge customers a subscription fee for access to the dashboard "
        "and reporting features each month for every team that signs up."
    )
    with_numbers = (
        "We charge $49 per seat per month. Average deal is $11760 per year "
        "across 20 seats with 90% renewal."
    )
    assert score_block(with_numbers) > score_block(plain)


def test_named_entities_rewarded():
    plain = (
        "we integrate with the tools teams already use every day and list "
        "the product in the directories those tools run for their users"
    )
    named = (
        "we integrate with Jira and GitHub every day and list the product "
        "in their marketplaces for the teams that use those tools daily"
    )
    assert abs(len(plain.split()) - len(named.split())) <= 2
    assert score_block(named) > score_block(plain)


def test_sample_scores_well():
    result = critique_model(SAMPLE_MODEL)
    assert result["overall_score"] >= 60
    assert len(result["strengths"]) >= 3


def test_result_shape():
    result = critique_model(SAMPLE_MODEL)
    assert set(result.keys()) == {"overall_score", "per_block", "strengths", "risks"}
    assert 0 <= result["overall_score"] <= 100
    assert set(result["per_block"].keys()) == set(block_ids())
    assert all(0 <= v <= 100 for v in result["per_block"].values())


def test_risks_are_investor_questions():
    canvas = blank_canvas()
    canvas["customer_segments"] = "Some text here to trigger cross checks only."
    result = critique_model(canvas)
    assert result["risks"], "expected risks for a weak canvas"
    for r in result["risks"]:
        assert r.endswith("?") or r.endswith("."), r
    assert any("?" in r for r in result["risks"])


def test_missing_segment_mention_is_a_risk():
    canvas = blank_canvas()
    canvas["customer_segments"] = (
        "Heads of engineering at software companies with 50 to 500 employees."
    )
    canvas["value_propositions"] = (
        "A dashboard with charts and reports that loads quickly every morning."
    )
    result = critique_model(canvas)
    assert any("who exactly pays" in r.lower() for r in result["risks"])


def test_matching_segment_and_value_prop_is_a_strength():
    canvas = blank_canvas()
    canvas["customer_segments"] = (
        "Heads of engineering at software companies with 50 to 500 employees."
    )
    canvas["value_propositions"] = (
        "Heads of engineering at software companies get weekly reports "
        "without chasing status updates from their teams."
    )
    result = critique_model(canvas)
    assert any("investors like that" in s.lower() for s in result["strengths"])


def test_money_on_both_sides_is_a_strength():
    canvas = blank_canvas()
    canvas["revenue_streams"] = "We charge $49 per seat per month, billed annually."
    canvas["cost_structure"] = "Hosting costs $180000 per year and the team costs $2.1M."
    result = critique_model(canvas)
    assert any("both sides of the money equation" in s for s in result["strengths"])


def test_missing_price_is_a_risk():
    canvas = blank_canvas()
    canvas["revenue_streams"] = "Customers pay a subscription for access to the product."
    result = critique_model(canvas)
    assert any("put a number on it" in r.lower() for r in result["risks"])


def test_none_input_treated_as_empty():
    result = critique_model(None)
    assert result["overall_score"] == 0
