import httpx
from typing import Any

from .endpoints import Endpoints


DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "X-Web-Client": "desktop",
    "X-Web-Client-Id": "web",
    "Referer": "https://www.digikala.com/",
}

class DigikalaClient:
    def __init__(self, timeout: float = 60):
        self.client = httpx.AsyncClient(timeout=timeout, headers=DEFAULT_HEADERS, follow_redirects=True)

    async def close(self):
        await self.client.aclose()

    async def get(self, url: str, params: dict[str, Any] | None = None) -> dict:
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def autocomplete(self, query: str) -> dict:
        return await self.get(Endpoints.AUTOCOMPLETE, {"q": query})

    async def search(
        self,
        params: dict[str, Any],
        *,
        category_id: int | None = None,
    ) -> dict:
        return await self.get(
            Endpoints.category(category_id) if category_id else Endpoints.SEARCH,
            params,
        )

    async def product(self, product_id: int) -> dict:
        return await self.get(Endpoints.product(product_id))

    async def similar_products(self, product_id: int, offset: int | None = None) -> dict:
        return await self.get(
            Endpoints.similar_products(product_id),
            {"offset": offset} if offset is not None else None,
        )


client = DigikalaClient()
