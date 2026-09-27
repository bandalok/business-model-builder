"""Tests for bmc.blocks: the nine canvas blocks."""

from bmc.blocks import BLOCKS, block_ids, get_block


def test_nine_blocks_present():
    assert len(BLOCKS) == 9


def test_block_ids_unique_and_in_order():
    ids = block_ids()
    assert len(ids) == len(set(ids)) == 9
    assert ids[0] == "customer_segments"
    assert ids[-1] == "cost_structure"


def test_expected_ids():
    expected = {
        "customer_segments", "value_propositions", "channels",
        "customer_relationships", "revenue_streams", "key_resources",
        "key_activities", "key_partnerships", "cost_structure",
    }
    assert set(block_ids()) == expected


def test_each_block_has_name_tagline_questions_hints():
    for b in BLOCKS:
        assert b["name"], b["id"]
        assert b["tagline"], b["id"]
        assert 2 <= len(b["questions"]) <= 3, b["id"]
        assert len(b["hints"]) >= 1, b["id"]
        assert all(isinstance(q, str) and q.strip() for q in b["questions"])
        assert all(isinstance(h, str) and h.strip() for h in b["hints"])


def test_get_block_known_id():
    b = get_block("revenue_streams")
    assert b is not None
    assert b["name"] == "Revenue Streams"


def test_get_block_unknown_id_returns_none():
    assert get_block("not_a_block") is None


def test_questions_are_plain_english():
    for b in BLOCKS:
        for q in b["questions"]:
            assert q.endswith("?"), q
            assert len(q.split()) >= 5, q
