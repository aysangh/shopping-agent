from typing import Any

from fastmcp import FastMCP

from digikala.client import client
from digikala.parser import parse_products_from_api, parse_recommendation_tabs


def register_get_similar_products(mcp: FastMCP) -> None:
    @mcp.tool(
        name="get_similar_products",
        description=(
        "Get similar or recommended products for a Digikala product. "
        "Use this when a product is unavailable or when the user asks for "
        "alternatives, similar items, or more options. Start without an offset "
        "to get the default recommendation group. Use an offset from "
        "available_tabs only if the user wants additional recommendation groups."
        ),
    )
    async def get_similar_products(
        product_id: int,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Get similar or recommended products for a Digikala product.

        Use this tool to find alternative products related to a known
        ``product_id``. It is especially useful when a product is unavailable
        or when the user requests similar items.

        Start with ``offset=None`` to retrieve the default recommendation
        group. Additional recommendation groups may be available through the
        returned ``available_tabs`` values. To reduce unnecessary API calls,
        request another offset only if the user asks for more alternatives.

        Args:
            product_id: Digikala product identifier.
            offset: Optional recommendation group offset returned in
                ``available_tabs``.

        Returns:
            A dictionary containing:
                - product_id: Requested product identifier.
                - recommendation_type: Title of the recommendation group.
                - available_tabs: Additional recommendation group offsets.
                - products: Recommended product summaries.

        Raises:
            ValueError: If ``product_id`` is not positive or ``offset`` is
                negative.
        """
        if product_id <= 0:
            raise ValueError("product_id must be positive.")
        if offset is not None and offset < 0:
            raise ValueError("offset must be >= 0.")

        response = await client.similar_products(
            product_id=product_id,
            offset=offset,
        )
        payload = response.get("data", {})
        recommendation = payload.get("data", {})
        meta = payload.get("meta", {})

        available_tabs = parse_recommendation_tabs(meta)
        recommendation_title = recommendation.get("title", "")
        products = parse_products_from_api(recommendation.get("products", []))

        return {
            "product_id": product_id,
            "recommendation_type": recommendation_title or None,
            "available_tabs": available_tabs or None,
            "products": [product.model_dump() for product in products],
        }
