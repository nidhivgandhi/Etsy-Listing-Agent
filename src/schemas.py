"""
Defines what a finished Etsy listing must look like. Claude's final answer
gets parsed into this model before we trust it — if it doesn't fit, we know
immediately instead of saving malformed data.
"""

from pydantic import BaseModel, Field, field_validator


class Listing(BaseModel):
    title: str = Field(..., max_length=140)
    tags: list[str] = Field(..., min_length=1, max_length=13)
    description: str
    materials: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def tags_within_length(cls, tags: list[str]) -> list[str]:
        for t in tags:
            if len(t) > 20:
                raise ValueError(f"tag '{t}' exceeds Etsy's 20-character limit")
        return tags
