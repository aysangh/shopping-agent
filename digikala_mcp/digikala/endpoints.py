class Endpoints:
    BASE = "https://api.digikala.com"

    # Search
    SEARCH = f"{BASE}/v3/search/"
    AUTOCOMPLETE = f"{BASE}/v1/autocomplete/"

    @staticmethod
    def category(category_id: int) -> str:
        """Category search endpoint."""
        return f"{Endpoints.BASE}/v2/category/{category_id}/"

    @staticmethod
    def product(product_id: int) -> str:
        """Product details endpoint."""
        return f"{Endpoints.BASE}/v2/product/{product_id}/"

    @staticmethod
    def similar_products(product_id: int) -> str:
        """Similar / recommended products."""
        return (
            f"{Endpoints.BASE}/v1/product/"
            f"{product_id}/tabular-recommendation/"
        )
