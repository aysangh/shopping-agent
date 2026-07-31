from enum import IntEnum


class Sort(IntEnum):
    RELEVANCE = 1
    PRICE_LOW_TO_HIGH = 2
    PRICE_HIGH_TO_LOW = 3
    NEWEST = 4
    BEST_SELLING = 5
    MOST_VIEWED = 6
    FASTEST_SHIPPING = 7
    BUYER_RECOMMENDATIONS = 8
    SELECTED = 9


_API_SORT_IDS = {
    Sort.RELEVANCE: 22,
    Sort.PRICE_LOW_TO_HIGH: 20,
    Sort.PRICE_HIGH_TO_LOW: 21,
    Sort.NEWEST: 1,
    Sort.BEST_SELLING: 7,
    Sort.MOST_VIEWED: 4,
    Sort.FASTEST_SHIPPING: 25,
    Sort.BUYER_RECOMMENDATIONS: 27,
    Sort.SELECTED: 29,
}

_SORT_LABELS = {
    Sort.RELEVANCE: "Relevance",
    Sort.PRICE_LOW_TO_HIGH: "Price Low-High",
    Sort.PRICE_HIGH_TO_LOW: "Price High-Low",
    Sort.NEWEST: "Newest",
    Sort.BEST_SELLING: "Best Selling",
    Sort.MOST_VIEWED: "Most Viewed",
    Sort.FASTEST_SHIPPING: "Fastest Shipping",
    Sort.BUYER_RECOMMENDATIONS: "Buyer Recommendations",
    Sort.SELECTED: "Selected",
}


def api_sort_id(sort: Sort | int) -> int:
    """
    Convert UI sort enum to Digikala API sort id.
    """
    return _API_SORT_IDS[Sort(sort)]


def sort_label(sort: Sort | int) -> str:
    """
    Human-readable sort label.
    """
    return _SORT_LABELS[Sort(sort)]
