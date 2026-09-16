from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["GENAI_API_KEY"])

check_char_limits_schema = {
    "name": "check_char_limits",
    "description": "A function that checks if the title and tags meet character limits.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title to check (max 140 characters)."
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "A tag to check (max 20 characters)."
                },
            }
        },
        "required": ["title", "tags"],
    }
}

def check_char_limits(title: str, tags: list[str]) -> dict:
    bad_tags = [t for t in tags if len(t) > 20]
    return {
        "title_ok": len(title) <= 140,
        "tag_count_ok": len(tags) <= 13,
        "bad_tags": bad_tags,
    }

messages = [
    types.Content(
        role="user",
        parts=[types.Part.from_text(
            text="Check if the title and tags meet character limits: "
                 "title='handmade walnut cutting board', tags=['walnut', 'cutting board', 'kitchen']"
        )],
    )
]

while True:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[types.Tool(function_declarations=[check_char_limits_schema])],
        ),
    )
    part = response.candidates[0].content.parts[0]

    if part.function_call is not None:
        result = check_char_limits(**part.function_call.args)

        messages.append(response.candidates[0].content)  # Gemini's function_call turn
        messages.append(types.Content(
            role="user",
            parts=[types.Part.from_function_response(
                name=part.function_call.name,
                response=result,
            )],
        ))
        continue  # now safe — messages actually changed, so Gemini sees new info

    elif part.text is not None:
        print(part.text)
        break
    else:
        raise ValueError("Unexpected response format")
