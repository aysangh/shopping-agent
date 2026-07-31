from typing import Any

from fastmcp import FastMCP

from digikala.client import client
from digikala.converters import tooman_to_rial
from digikala.parser import (
    extract_available_filters,
    extract_pager,
    parse_products_from_widgets,
)
from digikala.sort import api_sort_id, sort_label

SORT_MIN = 1
SORT_MAX = 9


def _validate_search_params(
    keyword: str,
    page: int,
    sort: int,
    category_id: int | None,
    price_min_tooman: int | None,
    price_max_tooman: int | None,
) -> None:
    if not keyword:
        raise ValueError("keyword cannot be empty")
    if page < 1:
        raise ValueError("page must be >= 1")
    if not (SORT_MIN <= sort <= SORT_MAX):
        raise ValueError(f"sort must be between {SORT_MIN} and {SORT_MAX}")
    if category_id is not None and category_id <= 0:
        raise ValueError("category_id must be positive")
    if (
        price_min_tooman is not None
        and price_max_tooman is not None
        and price_min_tooman > price_max_tooman
    ):
        raise ValueError("price_min_tooman cannot exceed price_max_tooman")


def _build_query(
    keyword: str,
    page: int,
    sort: int,
    price_min_tooman: int | None,
    price_max_tooman: int | None,
    colors: list[int] | None,
) -> dict[str, Any]:
    query: dict[str, Any] = {
        "q": keyword,
        "page": page,
        "sort": api_sort_id(sort),
    }
    if colors:
        query["colors[]"] = colors
    if price_min_tooman is not None:
        query["price[min]"] = tooman_to_rial(price_min_tooman)
    if price_max_tooman is not None:
        query["price[max]"] = tooman_to_rial(price_max_tooman)
    return query


def register_search_products(mcp: FastMCP) -> None:
    @mcp.tool(
        name="search_products",
        description=(
            "Primary product search tool. Use this directly for most shopping queries. "
            "Start with page=1 and avoid exploring additional pages unless the user asks "
            "for more options or the first page is insufficient. Default sort=1 returns "
            "the most relevant results. Change the sort only when the user expresses a "
            "preference such as cheapest, most expensive, newest, best selling, most viewed, "
            "fastest shipping, buyer recommendations, or selected products. If the query is "
            "very short, ambiguous, incomplete, or appears misspelled, consider calling "
            "get_search_suggestions first."
        ),
    )
    async def search_products(
        keyword: str,
        page: int = 1,
        sort: int = 1,
        category_id: int | None = None,
        price_min_tooman: int | None = None,
        price_max_tooman: int | None = None,
        colors: list[int] | None = None,
    ) -> dict[str, Any]:
        """Search Digikala products by keyword.

        This is the primary product search tool for shopping queries. In most
        cases, use ``page=1`` and avoid requesting additional pages unless the
        user explicitly asks for more options or the first page does not contain
        suitable products.

        Sort options:
            1: Relevance (default)
            2: Price low to high
            3: Price high to low
            4: Newest
            5: Best selling
            6: Most viewed
            7: Fastest shipping
            8: Buyer recommendations
            9: Selected products

        Examples:
            - "cheapest phone" -> sort=2
            - "newest laptop" -> sort=4
            - "best selling headphones" -> sort=5

        Args:
            keyword: Product name, brand, or search phrase.
            page: Result page number starting from 1. Keep the default unless
                additional pages are specifically needed.
            sort: Sort option ID from 1 to 9.
            category_id: Optional Digikala category identifier.
            price_min_tooman: Optional minimum price in Tooman.
            price_max_tooman: Optional maximum price in Tooman.
            colors: Optional list of Digikala color IDs.

        Returns:
            A dictionary containing the normalized query, selected sort,
            pagination information, product summaries, and available filters.

        Raises:
            ValueError: If the keyword is empty, page < 1, sort is outside the
            allowed range, category_id is invalid, or the minimum price exceeds
            the maximum price.
        """
        keyword = keyword.strip()
        _validate_search_params(
            keyword, page, sort, category_id, price_min_tooman, price_max_tooman
        )

        query = _build_query(
            keyword,
            page,
            sort,
            price_min_tooman,
            price_max_tooman,
            colors,
        )

        response = await client.search(
            query,
            category_id=category_id,
        )
        
        widgets = response.get("data", {}).get("widgets", [])
        products = parse_products_from_widgets(widgets)

        return {
            "keyword": keyword,
            "sort": {"id": sort, "name": sort_label(sort)},
            "pagination": extract_pager(widgets),
            "products": [p.model_dump() for p in products],
            "available_filters": extract_available_filters(widgets),
        }
