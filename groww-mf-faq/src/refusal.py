# Refuse opinionated/portfolio questions; return polite message + educational link
import re
from typing import Tuple

from config import EDUCATIONAL_LINK, AMFI_FAQ_LINK

# Patterns that suggest advice / recommendation / opinion (we refuse these)
ADVICE_PATTERNS = [
    r"\b(should i|can i|shall i|would you)\s*(buy|sell|invest|redeem|exit|switch)\b",
    r"\b(which (scheme|fund|mutual fund)|best (scheme|fund|mf|elss|sip))\b",
    r"\b(recommend|suggest|advice|advise)\b",
    r"\b(good (to|for)|worth (investing|buying)|better (than|to))\b",
    r"\b(return(s)?|performance|how much (will|did)|profit)\b",  # performance/return questions → link to factsheet
    r"\b(my portfolio|my (sip|investment)|when (to|should))\s*(buy|sell|redeem)\b",
    r"\b(compare|comparison)\s+(of|between).*(which (one|is better))\b",
]


def is_advice_or_opinion_query(query: str) -> bool:
    """True if the query asks for advice, recommendation, or opinion (we refuse)."""
    q = (query or "").strip().lower()
    if len(q) < 5:
        return False
    for pat in ADVICE_PATTERNS:
        if re.search(pat, q, re.IGNORECASE):
            return True
    return False


def get_refusal_response(query: str) -> Tuple[str, str]:
    """
    Returns (message, link) for advice/opinion questions.
    Message is polite, facts-only; link is Groww blog (factsheet/how to read).
    """
    message = (
        "I can only provide factual information about Groww Mutual Fund schemes. "
        "I cannot provide investment advice such as 'should I buy/sell' or portfolio recommendations. "
        "For understanding mutual fund factsheets and key information, please refer to the link below."
    )
    return message, EDUCATIONAL_LINK
