"""Tests for bmc.sample: the SampleCo fixture used by tests and the demo."""

from bmc.blocks import block_ids
from bmc.critique import critique_model
from bmc.sample import SAMPLE_MODEL, SAMPLE_ECONOMICS
from bmc.unit_economics import calculate_economics


def test_sample_covers_all_blocks():
    assert set(SAMPLE_MODEL.keys()) == set(block_ids())


def test_sample_blocks_are_substantive():
    for bid, text in SAMPLE_MODEL.items():
        assert len(text.split()) >= 20, bid


def test_sample_mentions_price():
    assert "$49" in SAMPLE_MODEL["revenue_streams"]


def test_sample_critique_passes():
    result = critique_model(SAMPLE_MODEL)
    assert result["overall_score"] >= 60
    assert len(result["risks"]) <= 2


def test_sample_economics_inputs_valid():
    result = calculate_economics(**SAMPLE_ECONOMICS)
    assert result["gross_margin_pct"] > 50
    assert result["break_even_customers"] is not None
