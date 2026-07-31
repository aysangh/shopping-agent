from pydantic import BaseModel, Field


class Seller(BaseModel):
    name: str
    rating: float = 0
    trusted: bool = False
    official: bool = False

class Rating(BaseModel):
    stars: float | None = None
    count: int = 0

class ProductSummary(BaseModel):
    id: int
    title_fa: str
    title_en: str | None = None
    url: str | None = None
    image_url: str | None = None
    price: int
    rating: Rating | None = None
    brand: str | None = None
    category: str | None = None
    badges: list[str] = Field(default_factory=list)
    colors: list[str] = Field(default_factory=list)
    in_stock: bool = True
