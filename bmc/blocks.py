"""The nine Business Model Canvas blocks.

Each block carries plain-English guided questions (shown in the wizard) and
validation hints (used by the critique engine and shown as helper text).
"""

BLOCKS = [
    {
        "id": "customer_segments",
        "name": "Customer Segments",
        "tagline": "Who pays you? Be specific.",
        "questions": [
            "Name the exact group of people or companies who will pay. What job title, team, or company size?",
            "How many of them exist, and how do you know?",
            "Which segment will you serve first, and why them?",
        ],
        "hints": [
            "Name a real group, not 'everyone'.",
            "Add a number: how many potential customers are there?",
        ],
    },
    {
        "id": "value_propositions",
        "name": "Value Propositions",
        "tagline": "Why should they pick you?",
        "questions": [
            "What painful problem do you solve, in the customer's own words?",
            "What do they use today instead of you, and why is that worse?",
            "What changes for them in the first 30 days of using your product?",
        ],
        "hints": [
            "Describe the outcome, not the features.",
            "Say what the customer stops doing or stops paying for.",
        ],
    },
    {
        "id": "channels",
        "name": "Channels",
        "tagline": "How do customers find and buy you?",
        "questions": [
            "Where do your customers already hang out or shop?",
            "How will they hear about you the first time?",
            "How do they actually pay and get started?",
        ],
        "hints": [
            "Name real places: a marketplace, a community, a sales motion.",
            "A channel you do not control is a risk. Say who owns it.",
        ],
    },
    {
        "id": "customer_relationships",
        "name": "Customer Relationships",
        "tagline": "How do you win and keep them?",
        "questions": [
            "Do customers serve themselves, or does a human help them?",
            "What makes a customer stay after the first year?",
            "How do you hear about problems before customers leave?",
        ],
        "hints": [
            "Match the relationship to the price: high touch needs high price.",
            "Name one retention habit, not just acquisition.",
        ],
    },
    {
        "id": "revenue_streams",
        "name": "Revenue Streams",
        "tagline": "How does money come in?",
        "questions": [
            "What exactly do customers pay for, and how much?",
            "Is it one-time, monthly, yearly, or usage-based?",
            "What could you charge for later that you give away now?",
        ],
        "hints": [
            "Put real numbers in: price, billing period, who pays.",
            "If the user is free, say who pays instead.",
        ],
    },
    {
        "id": "key_resources",
        "name": "Key Resources",
        "tagline": "What do you need to deliver this?",
        "questions": [
            "What assets must exist for the product to work: data, tech, brand, people?",
            "Which of these are hard for a competitor to copy?",
            "What are you missing today?",
        ],
        "hints": [
            "Separate what you own from what you rent.",
            "Name the one resource that is hardest to replace.",
        ],
    },
    {
        "id": "key_activities",
        "name": "Key Activities",
        "tagline": "What work matters most?",
        "questions": [
            "What does the team do every week that keeps the value flowing?",
            "Which activity, if stopped, would break the product in a month?",
            "What will you deliberately not do?",
        ],
        "hints": [
            "List verbs: building, selling, supporting, not nouns.",
            "If everything is key, nothing is. Pick the top three.",
        ],
    },
    {
        "id": "key_partnerships",
        "name": "Key Partnerships",
        "tagline": "Who do you depend on?",
        "questions": [
            "Which outside companies or people does your product rely on?",
            "What happens if your biggest partner changes their terms?",
            "Which partnership saves you the most time or money?",
        ],
        "hints": [
            "Name real companies or platforms, not 'strategic partners'.",
            "Every dependency is a risk. Say what your backup is.",
        ],
    },
    {
        "id": "cost_structure",
        "name": "Cost Structure",
        "tagline": "Where does the money go?",
        "questions": [
            "What are your three biggest costs?",
            "Which costs grow with each new customer, and which stay flat?",
            "What does it cost you to serve one customer for a year?",
        ],
        "hints": [
            "Split costs that scale per customer from fixed costs.",
            "Put numbers in, even rough ones. Guesses beat blanks.",
        ],
    },
]


def block_ids():
    """Return the block ids in canvas order."""
    return [b["id"] for b in BLOCKS]


def get_block(block_id):
    """Return the block dict for an id, or None if unknown."""
    for b in BLOCKS:
        if b["id"] == block_id:
            return b
    return None
