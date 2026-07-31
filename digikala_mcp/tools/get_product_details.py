from typing import Any

from fastmcp import FastMCP

from digikala.client import client
from digikala.parser import (
    first_image,
    parse_colors,
    parse_comments_overview,
    parse_digiplus,
    parse_price,
    parse_rating,
    parse_review,
    parse_seller,
    parse_suggestion,
    parse_variants,
    parse_warranty,
)

UNAVAILABLE_MESSAGE = (
    "This product is currently unavailable. "
    "Use get_similar_products or perform another search."
)

def register_get_product_details(mcp: FastMCP) -> None:
    @mcp.tool(
        name="get_product_details",
        description=(
        "Get detailed information for a single Digikala product by its product_id. "
        "Use this after search_products when the user wants more details about a specific item. "
        "Returns product title, category, brand, price, rating, seller, warranty, Digiplus eligibility, "
        "images, color options, available variants, review summary, recommendation score, comments count, "
        "and comments overview. If the product is unavailable, returns unavailable=True and a message."
        ),
    )
    async def get_product_details(product_id: int) -> dict[str, Any]:
        """Retrieve detailed information for a Digikala product.

        Args:
            product_id: Numeric Digikala product identifier obtained from search_products.

        Returns:
            A dictionary containing pricing, rating, seller, warranty, variants,
            reviews, comments overview, and availability information.
        """        
        if product_id <= 0:
            raise ValueError("product_id must be positive")

        response = await client.product(product_id)
        product = response.get("data", {}).get("product", {})

        if product.get("status") != "marketable":
            return {
                "unavailable": True,
                "product_id": product_id,
                "message": UNAVAILABLE_MESSAGE,
            }

        variant = product.get("default_variant", {})

        return {
            "id": product_id,
            "title_fa": product.get("title_fa", ""),
            "url": product.get("url", {}).get("uri", ""),
            "category": product.get("category", {}).get("title_fa", ""),
            "brand": product.get("brand", {}).get("title_fa", ""),
            "price": parse_price(product),
            "rating": parse_rating(product),
            "seller": parse_seller(product),
            "warranty": parse_warranty(variant),
            "digiplus": parse_digiplus(variant),
            "image_url": first_image(product),
            "colors": parse_colors(product),
            "variants": parse_variants(product),
            "review": parse_review(product),
            "suggestion": parse_suggestion(product),
            "comments_count": product.get("comments_count"),
            "comments_overview": parse_comments_overview(product),
        }
