"""
Entry point. Run with: python cli.py
Type a raw item description, get back a validated, saved Etsy listing.
"""

from dotenv import load_dotenv
from pydantic import ValidationError

from src.agent import generate_listing
from src.storage import save_listing

load_dotenv()


def main():
    raw_prompt = input("Describe your item: ").strip()
    if not raw_prompt:
        print("Nothing entered — exiting.")
        return

    try:
        listing = generate_listing(raw_prompt)
    except ValidationError as e:
        print("Claude's output didn't match the required listing shape:")
        print(e)
        return
    except RuntimeError as e:
        print(f"Agent didn't finish: {e}")
        return

    print("\n--- Generated Listing ---")
    print(f"Title: {listing.title}")
    print(f"Tags: {', '.join(listing.tags)}")
    print(f"Materials: {', '.join(listing.materials)}")
    print(f"\nDescription:\n{listing.description}")

    save_listing(listing.model_dump())
    print("\nSaved to listing_history.json")


if __name__ == "__main__":
    main()
