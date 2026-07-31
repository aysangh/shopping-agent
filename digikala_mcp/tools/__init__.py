from fastmcp import FastMCP

from .get_search_suggestions import register_get_search_suggestions
from .search_products import register_search_products
from .get_product_details import register_get_product_details
from .get_similar_products import register_get_similar_products


def register_all_tools(mcp: FastMCP) -> None:
    register_get_search_suggestions(mcp)
    register_search_products(mcp)
    register_get_product_details(mcp)
    register_get_similar_products(mcp)
