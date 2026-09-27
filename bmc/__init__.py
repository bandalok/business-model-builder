"""Business Model Builder: an interactive Business Model Canvas toolkit for product managers.

Zero third-party dependencies. Everything here runs on plain rule-based logic.
"""

from bmc.blocks import BLOCKS, get_block, block_ids
from bmc.critique import critique_model
from bmc.unit_economics import calculate_economics
from bmc.sample import SAMPLE_MODEL, SAMPLE_ECONOMICS

__all__ = [
    "BLOCKS",
    "get_block",
    "block_ids",
    "critique_model",
    "calculate_economics",
    "SAMPLE_MODEL",
    "SAMPLE_ECONOMICS",
]
