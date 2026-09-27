"""Rule-based investor-style critique engine.

Input:  dict of block_id -> free text.
Output: dict with overall_score (0-100), per_block scores, strengths and risks.

No AI calls, no network. Scores reward specific numbers and named things,
penalize empty blocks and vague filler words, and cross-check that the
blocks agree with each other.
"""

import re

VAGUE_WORDS = [
    "everyone",
    "anyone",
    "everybody",
    "best",
    "world-class",
    "world class",
    "cutting-edge",
    "cutting edge",
    "revolutionary",
    "disruptive",
    "synergy",
    "synergies",
    "next-generation",
    "next generation",
    "game-changing",
    "game changing",
    "best-in-class",
    "best in class",
]

MONEY_RE = re.compile(
    r"\$\s?[\d,]+(?:\.\d+)?|\b\d+\s?%|\b\d[\d,]*(?:\.\d+)?\b"
)
MONEY_WORDS_RE = re.compile(
    r"\b(per month|per year|per seat|per user|monthly|yearly|annual|"
    r"subscription|pricing|price|cost|costs|revenue|arr|mrr)\b",
    re.IGNORECASE,
)
PRICE_RE = re.compile(
    r"\$|\bper month\b|\bper year\b|\bper seat\b|\bper user\b|"
    r"\bpricing\b|\bmrr\b|\barr\b",
    re.IGNORECASE,
)

CAPITALIZED_RE = re.compile(r"\b[A-Z][a-zA-Z]+\b")

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "your", "you",
    "our", "are", "will", "can", "have", "has", "into", "each", "per",
    "they", "them", "their", "who", "what", "when", "how", "why",
    "not", "but", "all", "any", "its", "it's", "via", "use", "using",
    "used", "get", "gets", "one", "two", "new", "than", "then", "also",
    "such", "more", "most", "over", "under", "between", "through",
}

BLOCK_RISKS = {
    "customer_segments": (
        "Who exactly pays you? 'Everyone' is not a customer segment. "
        "Name a real group."
    ),
    "value_propositions": (
        "Why would anyone switch? Your value prop does not say what "
        "changes for the customer."
    ),
    "channels": (
        "Where do the first 100 customers come from? Name a real channel."
    ),
    "customer_relationships": (
        "How do you keep customers after year one? High touch needs "
        "high prices to work."
    ),
    "revenue_streams": (
        "What is the price? No investor funds a business with no "
        "numbers on revenue."
    ),
    "key_resources": (
        "What do you own that is hard to copy? If the honest answer is "
        "'the team', say so plainly."
    ),
    "key_activities": (
        "What does the team do every week? List the work, not the job titles."
    ),
    "key_partnerships": (
        "Who can break you? Name the dependency and your backup plan."
    ),
    "cost_structure": (
        "What does one customer cost you per year? If you do not know, "
        "your pricing is a guess."
    ),
}

BLOCK_NAMES = {
    "customer_segments": "Customer Segments",
    "value_propositions": "Value Propositions",
    "channels": "Channels",
    "customer_relationships": "Customer Relationships",
    "revenue_streams": "Revenue Streams",
    "key_resources": "Key Resources",
    "key_activities": "Key Activities",
    "key_partnerships": "Key Partnerships",
    "cost_structure": "Cost Structure",
}


def _words(text):
    return re.findall(r"[A-Za-z0-9']+", text)


def _vague_hits(text):
    lowered = " " + text.lower() + " "
    return sum(lowered.count(" " + w + " ") for w in VAGUE_WORDS)


def _number_hits(text):
    return len(MONEY_RE.findall(text))


def _named_hits(text):
    count = 0
    for m in CAPITALIZED_RE.finditer(text):
        prev = text[: m.start()].rstrip()
        if not prev or prev[-1] in ".!?":
            continue
        count += 1
    return count


def score_block(text):
    """Score one block of text from 0 to 100."""
    if not text or not text.strip():
        return 0
    n = len(_words(text))
    score = min(n, 45) / 45 * 55
    score -= min(_vague_hits(text) * 6, 24)
    score += min(_number_hits(text) * 4, 16)
    score += min(_named_hits(text) * 2, 10)
    return max(0, min(100, round(score)))


def _content_words(text):
    words = set()
    for w in _words(text or ""):
        w = w.lower()
        if len(w) > 3 and w not in STOPWORDS:
            words.add(w)
    return words


def _has_money_terms(text):
    return bool(MONEY_WORDS_RE.search(text or ""))


def _has_price_terms(text):
    """True when the text names an actual price: a $ amount, a billing
    period, pricing language, or any number. 'Subscription' alone is not
    a price."""
    return bool(PRICE_RE.search(text or "") or MONEY_RE.search(text or ""))


def critique_model(blocks):
    """Critique a full canvas. Returns overall score, per-block scores,
    strengths and risks (risks phrased as blunt investor questions)."""
    blocks = blocks or {}
    per_block = {bid: score_block(blocks.get(bid, "")) for bid in BLOCK_NAMES}

    strengths = []
    risks = []
    cross_strengths = 0

    for bid, score in per_block.items():
        if score >= 70:
            strengths.append(
                "%s is specific and concrete. Keep it." % BLOCK_NAMES[bid]
            )
        elif score < 40:
            risks.append(BLOCK_RISKS[bid])

    # Vague filler anywhere is a red flag on its own.
    total_vague = sum(_vague_hits(blocks.get(bid, "")) for bid in BLOCK_NAMES)
    if total_vague >= 2:
        risks.append(
            "Cut the filler words ('everyone', 'world-class', 'best'). "
            "Investors read them as 'we have not thought about this.'"
        )

    # Cross-block check 1: value prop should name the segment.
    seg_words = _content_words(blocks.get("customer_segments"))
    vp_words = _content_words(blocks.get("value_propositions"))
    if seg_words and vp_words and len(seg_words & vp_words) >= 2:
        cross_strengths += 1
        strengths.append(
            "Your value prop names the same customers as your segments. "
            "Investors like that."
        )
    else:
        risks.append(
            "Who is the value prop for? It never names your customer "
            "segment. An investor will ask: who exactly pays?"
        )

    # Cross-block check 2: money on both sides of the equation.
    rev_money = _has_price_terms(blocks.get("revenue_streams"))
    cost_money = _has_money_terms(blocks.get("cost_structure"))
    if rev_money and cost_money:
        cross_strengths += 1
        strengths.append(
            "You put numbers on both sides of the money equation. "
            "That is rarer than it should be."
        )
    if not rev_money:
        risks.append(
            "How do you make money, exactly? Your revenue streams name "
            "no price. Put a number on it."
        )
    if not cost_money:
        risks.append(
            "What does it cost to run this? Your cost structure has no "
            "numbers. Rough guesses beat blanks."
        )

    # Cross-block check 3: channels should reach the stated segments.
    ch_words = _content_words(blocks.get("channels"))
    if seg_words and ch_words and (seg_words & ch_words):
        cross_strengths += 1
        strengths.append(
            "Your channels speak to the same audience you named in segments."
        )
    else:
        risks.append(
            "How do these channels reach those customers? Your channels do "
            "not mention your segment. Where do the first 100 come from?"
        )

    # Cross-block check 4: resources should support activities.
    res_words = _content_words(blocks.get("key_resources"))
    act_words = _content_words(blocks.get("key_activities"))
    if res_words and act_words and (res_words & act_words):
        cross_strengths += 1
        strengths.append(
            "Your key activities line up with your key resources. "
            "The story holds together."
        )
    else:
        risks.append(
            "What do you actually do all day? Your key activities do not "
            "connect to your key resources. Pick the work that matters."
        )

    overall = round(sum(per_block.values()) / len(per_block))
    overall += 2 * cross_strengths
    overall -= 3 * len(risks)
    overall = max(0, min(100, overall))

    return {
        "overall_score": overall,
        "per_block": per_block,
        "strengths": strengths,
        "risks": risks,
    }
