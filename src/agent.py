"""
The control loop: this is the actual "agent." Anthropic's API only ever
answers one message at a time — this loop is what decides to call it again
with tool results, and when to stop. Everything here is yours; nothing here
is Anthropic's.
"""

import json
from urllib import response

from anthropic import Anthropic
from pydantic import ValidationError

from .prompts import SYSTEM_PROMPT
from .schemas import Listing
from .tools import TOOL_REGISTRY, TOOL_SCHEMAS

MODEL = "claude-sonnet-5"
MAX_ITERATIONS = 5


def generate_listing(raw_prompt: str) -> Listing:
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

    messages = [{"role": "user", "content": raw_prompt}]

    for _ in range(MAX_ITERATIONS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=8000,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            tool_calls = [b for b in response.content if b.type == "tool_use"]

            tool_results = []
            for tool_call in tool_calls:
                result = TOOL_REGISTRY[tool_call.name](**tool_call.input)
                tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": str(result),
            })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            continue

        # Claude is done — extract and validate its final answer
        text_blocks = [b.text for b in response.content if b.type == "text"]
        if not text_blocks:
            raise RuntimeError(f"No text block in response. stop_reason={response.stop_reason}, content={response.content}")
        final_text = text_blocks[0]

        cleaned = final_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.removeprefix("json").strip()
        raw_json = json.loads(cleaned)
        return Listing(**raw_json)

    raise RuntimeError(
        f"Exceeded {MAX_ITERATIONS} iterations without a final answer"
    )
