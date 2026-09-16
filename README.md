# Etsy Listing Agent

Takes a raw item description and generates an SEO-optimized Etsy listing
(title, tags, description, materials) using Claude, with tool-calling to
validate the draft against Etsy's actual constraints before returning it.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env          # then add your ANTHROPIC_API_KEY
```

Get a key at console.anthropic.com (Settings → API Keys). Requires adding
billing (prepaid credits, $5 minimum) — leave auto-reload off to cap spend
at your balance.

## Run

```bash
python cli.py
```

## Test

```bash
pytest
```

## Structure

- `cli.py` — entry point: takes your prompt, prints the result, saves it
- `src/agent.py` — the control loop (the actual agent logic)
- `src/tools.py` — functions Claude can call to check its own draft
- `src/schemas.py` — Pydantic model defining the final listing shape
- `src/prompts.py` — system prompt with Etsy SEO rules (edit this often)
- `src/storage.py` — saves generated listings to `listing_history.json`
- `tests/test_tools.py` — unit tests for the tools (no API calls)

## Roadmap

- Competitor tag research (web search tool)
- Real performance feedback (Etsy Open API v3 — views/favorites/sales
  feeding back into future generations)
- Image-based prompts (vision on a product photo)
- Direct posting via Etsy's API (OAuth2)
