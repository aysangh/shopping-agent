from typing import Any

from .converters import rial_to_tooman
from .models import Seller, Rating, ProductSummary


DIGIKALA_BASE_URL = "https://www.digikala.com"

def absolute_url(path: str | None) -> str | None:
    """Convert a Digikala relative path to an absolute URL."""
    if not path:
        return None
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{DIGIKALA_BASE_URL}{path}"

def _rating_stars(count: int, rate: float) -> float | None:
    """
    Digikala exposes ratings on a 0-100 scale. Convert to 0-5 stars.
    Hide the star score when there are too few ratings to be meaningful.
    """
    if count < 10:
        return None
    return round(rate / 20.0, 1)

def _parse_badges(product: dict[str, Any]) -> list[str]:
    """Parse promotional badges shown on a product listing."""
    variant = product.get("default_variant") or {}
    price = variant.get("price") or {}
    badges: list[str] = []
    if price.get("is_incredible"):
        badges.append("شگفت‌انگیز")
    if variant.get("digiplus", {}).get("is_jet_eligible"):
        badges.append("دیجی‌پلاس جت")
    return badges


def first_image(product: dict[str, Any]) -> str | None:
    """Return the first product image URL, preferring webp."""
    main = product.get("images", {}).get("main", {})
    for key in ("webp_url", "url"):
        urls = main.get(key)
        if urls:
            return str(urls[0])
    return None

def parse_price(product: dict[str, Any]) -> int:
    """Parse the price of a product's default variant."""
    variant = product.get("default_variant") or {}
    price = variant.get("price") or {}
    selling = int(price.get("selling_price", 0))
    return rial_to_tooman(selling)
        
def parse_rating(product: dict[str, Any]) -> Rating:
    """Parse a product's rating."""
    rating = product.get("rating") or {}
    count = int(rating.get("count", 0))
    rate = float(rating.get("rate", 0))
    return Rating(stars=_rating_stars(count, rate), count=count)

def parse_seller(product: dict[str, Any]) -> Seller | None:
    """Parse the default seller of a product's default variant."""
    variant = product.get("default_variant") or {}
    seller = variant.get("seller") or {}
    if not seller:
        return None
    properties = seller.get("properties", {})
    return Seller(
        name=seller.get("title", ""),
        rating=float(seller.get("stars", 0)),
        trusted=bool(properties.get("is_trusted", False)),
        official=bool(properties.get("is_official", False)),
    )

def parse_colors(product: dict[str, Any]) -> list[dict[str, str]]:
    """Parse available product colors as {name, hex} pairs."""
    return [
        {
            "name": color.get("title", ""),
            "hex": color.get("hex_code", ""),
        }
        for color in product.get("colors", [])
    ]


def parse_product_summary(product: dict[str, Any]) -> ProductSummary:
    """Parse a single product as returned by search/recommendation APIs."""
    data_layer = product.get("data_layer") or {}
    colors = [c["title"] for c in product.get("colors", []) if c.get("title")]

    return ProductSummary(
        id=int(product.get("id", 0)),
        title_fa=product.get("title_fa", ""),
        title_en=product.get("title_en"),
        url=absolute_url(product.get("url", {}).get("uri")),
        image_url=first_image(product),
        price=parse_price(product),
        rating=parse_rating(product),
        brand=data_layer.get("brand"),
        category=data_layer.get("category"),
        badges=_parse_badges(product),
        colors=colors,
        in_stock=product.get("status") == "marketable",
    )


def parse_products_from_api(
    products: list[dict[str, Any]],
) -> list[ProductSummary]:
    """Parse a flat list of products, as returned directly by an API."""
    return [
        parse_product_summary(product)
        for product in products
        if product.get("status") == "marketable"
    ]

def parse_products_from_widgets(
    widgets: list[dict[str, Any]],
) -> list[ProductSummary]:
    """Search endpoints return widgets instead of a flat product list."""
    products: list[ProductSummary] = []
    for widget in widgets:
        if widget.get("type") != "vertical_product_listing":
            continue
        for item in widget.get("data", {}).get("widgets", []):
            if item.get("type") != "product":
                continue
            product = item.get("data")
            if not product or product.get("status") != "marketable":
                continue
            products.append(parse_product_summary(product))
    return products


def extract_pager(widgets: list[dict[str, Any]]) -> dict[str, int]:
    """Extract pagination metadata from search widgets."""
    for widget in widgets:
        if widget.get("type") != "vertical_product_listing":
            continue
        pager = widget.get("data", {}).get("pager")
        if pager:
            return {
                "current_page": int(pager.get("current_page", 1)),
                "total_pages": int(pager.get("total_pages", 1)),
                "total_items": int(pager.get("total_items", 0)),
            }
    return {"current_page": 1, "total_pages": 1, "total_items": 0}


def extract_available_filters(
    widgets: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Extract the filter options (price range, brands, colors, ...) offered
    by a search's listing widget, if present."""
    listing = next(
        (w for w in widgets if w.get("type") == "vertical_product_listing"),
        None,
    )
    if listing is None:
        return None
    filters = listing.get("data", {}).get("filters")
    if not filters:
        return None
    result: dict[str, Any] = {}
    if price := filters.get("price", {}).get("options"):
        result["price_range_tooman"] = {
            "min": rial_to_tooman(price.get("min", 0)),
            "max": rial_to_tooman(price.get("max", 0)),
        }
    if brands := filters.get("brands", {}).get("options", []):
        result["brands"] = [
            {
                "id": b.get("id"),
                "title_fa": b.get("title_fa"),
                "title_en": b.get("title_en"),
            }
            for b in brands
        ]
    if colors := filters.get("color_palettes", {}).get("options", []):
        result["colors"] = [
            {
                "id": c.get("id"),
                "title": c.get("title"),
                "hex_code": c.get("hex_code"),
            }
            for c in colors
        ]
    if sub_categories := filters.get("categories", {}).get("options", []):
        result["sub_categories"] = [
            {
                "id": sc.get("id"),
                "title_fa": sc.get("title_fa"),
                "products_count": sc.get("products_count"),
            }
            for sc in sub_categories
        ]
    return result or None


def parse_variants(product: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse in-stock variants of a product, with seller and price."""
    variants: list[dict[str, Any]] = []
    for variant in product.get("variants", []):
        if variant.get("status") != "marketable":
            continue
        price = variant.get("price", {})
        variants.append(
            {
                "id": int(variant.get("id", 0)),
                "seller": variant.get("seller", {}).get("title", ""),
                "price": rial_to_tooman(int(price.get("selling_price", 0))),
            }
        )
    return variants


def parse_review(product: dict[str, Any]) -> dict[str, Any] | None:
    """Parse the expert review of a product, if any."""
    review = product.get("review") or {}
    if not review:
        return None
    attributes = [
        {
            "title": attr.get("title", ""),
            "values": [str(v) for v in attr.get("values", [])],
        }
        for attr in review.get("attributes", [])
    ]
    return {
        "description": review.get("description"),
        "attributes": attributes or None,
    }


def parse_suggestion(product: dict[str, Any]) -> dict[str, Any] | None:
    """Parse the 'would you suggest this product' summary, if any."""
    suggestion = product.get("suggestion") or {}
    if not suggestion:
        return None
    return {
        "count": suggestion.get("count"),
        "percentage": suggestion.get("percentage"),
    }

def parse_comments_overview(product: dict[str, Any]) -> dict[str, Any] | None:
    """Parse the comments overview (pros/cons summary), if any."""
    overview = product.get("comments_overview") or {}
    if not overview:
        return None
    return {
        "id": overview.get("id"),
        "overview": overview.get("overview"),
        "advantages": overview.get("advantages", []),
        "disadvantages": overview.get("disadvantages", []),
    }

def parse_warranty(variant: dict[str, Any]) -> str | None:
    """Parse the warranty title of a variant, if any."""
    warranty = variant.get("warranty")
    return warranty.get("title_fa") if warranty else None

def parse_digiplus(variant: dict[str, Any]) -> dict[str, Any] | None:
    """Parse DigiPlus (Jet delivery) info of a variant, if eligible."""
    digiplus = variant.get("digiplus") or {}
    if not digiplus.get("is_jet_eligible"):
        return None
    return {
        "jet_eligible": True,
        "fast_shipping": digiplus.get("fast_shipping_text"),
    }


def parse_autocomplete_keywords(data: dict[str, Any]) -> list[str]:
    """Parse plain keyword suggestions from an autocomplete response."""
    return [
        item["keyword"]
        for item in data.get("auto_complete", [])
        if item.get("keyword")
    ]

def parse_autocomplete_categories(
    data: dict[str, Any],
) -> list[dict[str, Any]]:
    """Parse category matches from an autocomplete response."""
    matches: list[dict[str, Any]] = []
    for item in data.get("categories", []):
        keyword = item.get("keyword")
        category = item.get("category") or {}
        category_id = category.get("id")
        if not keyword or not category_id:
            continue
        url = category.get("url")
        matches.append(
            {
                "keyword": keyword,
                "category": {
                    "id": category_id,
                    "title_fa": category.get("title_fa", ""),
                    "title_en": category.get("title_en"),
                    "code": category.get("code"),
                    "url": absolute_url(url.get("uri")) if url else None,
                },
            }
        )
    return matches


def parse_recommendation_tabs(meta: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse the available recommendation tabs (e.g. 'similar', 'also
    bought') exposed by the similar-products endpoint."""
    return [
        {
            "offset": int(tab.get("offset", 0)),
            "type": tab.get("type", ""),
            "title": tab.get("title", ""),
        }
        for tab in meta.get("offsets", [])
    ]
