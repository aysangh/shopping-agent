from fastmcp import FastMCP
from tools import register_all_tools


mcp = FastMCP(
    "Digikala MCP",
    instructions="""
You have access to tools for searching and retrieving Digikala products.

General workflow:
- Use search_products for most shopping requests.
- Search for products before requesting product details.
- Start with page=1 and avoid additional pages unless needed.
- Use get_search_suggestions only for ambiguous or misspelled queries.
- Use get_similar_products for unavailable products or when the user asks for alternatives.
- If the user asks to compare products, retrieve details for each product before comparing.
- When the user asks to buy a product, purchase it, order it, or view it on Digikala, include the product URL returned by get_product_details.

Important:
- Do not invent product information, prices, ratings, specifications, availability, or reviews.
- Use only information returned by the tools.
- If no suitable products are found, say so clearly and ask whether the user wants to broaden the search.
"""
)

register_all_tools(mcp)

if __name__ == "__main__":
    mcp.run()
