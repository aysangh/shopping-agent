from typing import Any

from fastmcp import FastMCP

from digikala.client import client
from digikala.parser import (
    parse_autocomplete_categories,
    parse_autocomplete_keywords,
)


def register_get_search_suggestions(mcp: FastMCP) -> None:
    @mcp.tool(
        name="get_search_suggestions",
        description=(
            "Suggest corrected or expanded search keywords for Digikala. "
            "Use when the user's query is ambiguous, incomplete, unusually short, "
            "or likely misspelled before calling search_products."
        ),
    )
    async def get_search_suggestions(query: str) -> dict[str, Any]:
        """Get Digikala autocomplete suggestions.

        Args:
            query: Short product query or keyword (for example: "laptop",
                "گوشی", or "perfume").

        Returns:
            A dictionary containing autocomplete keyword suggestions and
            matching categories.
        """
        query = query.strip()
        if not query:
            raise ValueError("query cannot be empty")

        response = await client.autocomplete(query)
        data = response.get("data", {})

        return {
            "query": query,
            "categories": parse_autocomplete_categories(data),
            "auto_complete": parse_autocomplete_keywords(data),
        }
