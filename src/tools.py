"""
Tools the agent can call mid-draft to check its own work. Each is a plain,
testable Python function — Claude never executes these itself, it asks for
one by name and arguments, the control loop runs it, and the result is fed
back as text.
"""


def check_char_limits(title: str, tags: list[str]) -> dict:
    """Validate title/tag lengths and tag count against Etsy's real limits."""
    bad_tags = [t for t in tags if len(t) > 20]
    return {
        "title_ok": len(title) <= 140,
        "title_length": len(title),
        "tag_count": len(tags),
        "tag_count_ok": len(tags) <= 13,
        "bad_tags": bad_tags,
    }


def check_tag_diversity(tags: list[str]) -> dict:
    """Flag tags that repeat the same words, wasting searchable keyword slots."""
    seen_words: set[str] = set()
    duplicated = []
    for tag in tags:
        words = set(tag.lower().split())
        if words & seen_words:
            duplicated.append(tag)
        seen_words |= words
    return {"duplicated_word_tags": duplicated}


# Anthropic tool schemas — how Claude knows these tools exist and how to call them
TOOL_SCHEMAS = [
    {
        "name": "check_char_limits",
        "description": "Validate a listing title and tags against Etsy's character/count limits.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["title", "tags"],
        },
    },
    {
        "name": "check_tag_diversity",
        "description": "Check whether tags repeat the same keywords, wasting search slots.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["tags"],
        },
    },
]

# Dispatch table: tool name -> actual function to run
TOOL_REGISTRY = {
    "check_char_limits": check_char_limits,
    "check_tag_diversity": check_tag_diversity,
}
