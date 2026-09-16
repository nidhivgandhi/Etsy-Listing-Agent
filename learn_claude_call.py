from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

check_char_limits_schema = {
    "name" : "check_char_limits",
    "description" : "Validate a listing title and tags against Etsy's character limits.",
    "input_schema" : {
        "type" : "object",
        "properties" : {
            "title": {"type" : "string", "description": "The title to check (max 140 characters)."},
            "tags": {
                "type" : "array",
                "items" : {"type" : "string"},
                "description": "The tags to check (each max 20 characters)."
            },
        },
        "required" : ["title", "tags"],
    },
}

def check_char_limits(title: str, tags: list[str]) -> dict:
    bad_tags = [t for t in tags if len(t) > 20]
    return {
        "title_ok": len(title) <= 140,
        "tag_count_ok": len(tags) <= 13,
        "bad_tags": bad_tags,
    }

TOOL_REGISTRY = {"check_char_limits": check_char_limits,}

messages = [{
    "role": "user",
    "content": "Check if the title and tags meet character limits: "
               "title='handmade walnut cutting board', tags=['walnut', 'cutting board', 'kitchen']"
}]

for _ in range(5):
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=500,
        tools=[check_char_limits_schema],
        messages=messages,
    )

    if response.stop_reason == "tool_use":
        tool_call = next(b for b in response.content if b.type == "tool_use")
        result = TOOL_REGISTRY[tool_call.name](**tool_call.input)

        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": str(result),
            }],
        })
        continue

    else:
        final_text = next(b.text for b in response.content if b.type == "text")
        print(final_text)
        break
else:
    raise RuntimeError("Exceeded max loop iterations without a final answer")