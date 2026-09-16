from pydantic import BaseModel, Field

class Listing(BaseModel):
    title: str = Field(..., max_length=140)
    tags: list[str] = Field(..., min_length=1, max_length=13)
    description: str


    # should succeed
good = Listing(title="Walnut cutting board", tags=["kitchen", "handmade"], description="...")
print(good)

# should fail — title too long, see what the error looks like
bad = Listing(title="x", tags=["kitchen"], description="...")
