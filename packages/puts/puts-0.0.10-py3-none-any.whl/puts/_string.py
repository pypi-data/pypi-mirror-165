from typing import Tuple

_prepositions: Tuple[str] = (
    "aboard",
    "about",
    "above",
    "across",
    "after",
    "against",
    "along",
    "amid",
    "among",
    "anti",
    "around",
    "as",
    "at",
    "before",
    "behind",
    "below",
    "beneath",
    "beside",
    "besides",
    "between",
    "beyond",
    "but",
    "by",
    "concerning",
    "considering",
    "despite",
    "down",
    "during",
    "except",
    "excepting",
    "excluding",
    "following",
    "for",
    "from",
    "in",
    "inside",
    "into",
    "like",
    "minus",
    "near",
    "of",
    "off",
    "on",
    "onto",
    "opposite",
    "outside",
    "over",
    "past",
    "per",
    "plus",
    "regarding",
    "round",
    "save",
    "since",
    "than",
    "through",
    "to",
    "toward",
    "towards",
    "under",
    "underneath",
    "unlike",
    "until",
    "up",
    "upon",
    "versus",
    "via",
    "with",
    "within",
    "without",
)

_articles: Tuple[str] = (
    "a",
    "an",
    "the",
)

_conjunctions: Tuple[str] = (
    "for",
    "and",
    "nor",
    "but",
    "or",
    "yet",
    "so",
    "both",
    "either",
)

_NO_CAP_LIST: Tuple[str] = _prepositions + _articles + _conjunctions


def title_capitalize(string: str) -> str:
    """
    MLA Style Capitalization in Titles

    Prepositions, articles, and conjunctions aren't capitalized (unless they're the first or last word)

    Rule reference: https://www.grammarly.com/blog/capitalization-in-the-titles/
    """
    title = ""
    tokens = string.split()
    last_idx = len(tokens) - 1
    for idx, token in enumerate(tokens):
        if idx == 0:
            title += token.capitalize()
        elif idx == last_idx:
            title = title + " " + token.capitalize()
        else:
            if tokens[idx - 1].endswith(":"):
                title = title + " " + token.capitalize()
                continue

            if len(token) <= 3 or token in _NO_CAP_LIST:
                title = title + " " + token
            else:
                title = title + " " + token.capitalize()

    return title


title_cap = title_capitalize
