# Digikala MCP

A Python implementation of a **Model Context Protocol (MCP)** server for Digikala, built with **FastMCP**.

This project exposes Digikala functionality as MCP tools, enabling AI agents to search products, retrieve product details, discover similar products, and generate search suggestions through a standardized interface.


## Acknowledgements

This implementation is inspired by the TypeScript project:

🔗 [https://github.com/rezashahnazar/digikala-mcp-v2](https://github.com/rezashahnazar/digikala-mcp-v2) 

This repository contains a Python implementation tailored for the Shopping Agent project.

> **Note**
> For the original implementation, complete documentation, and standalone setup instructions, please refer to the TypeScript project linked above.

---

## Project Structure

```text
digikala_mcp/
│
├── server.py                 # MCP server entry point
│
├── digikala/
│   ├── __init__.py
│   ├── client.py             # Digikala API client
│   ├── endpoints.py          # API endpoints
│   ├── converters.py         # Utility functions
│   ├── parser.py             # API response parsing
│   ├── models.py             # Pydantic models
│   └── sort.py               # Sort mapping
│
└── tools/
    ├── __init__.py
    ├── get_search_suggestions.py
    ├── search_products.py
    ├── get_product_details.py
    └── get_similar_products.py
```

---

## MCP Inspector

The server was validated using **MCP Inspector**, which provides an interactive interface for inspecting available tools, invoking tool calls, and verifying structured MCP responses.

<img width="1920" height="945" alt="mcp" src="https://github.com/user-attachments/assets/5ad22efa-afa0-4980-8e32-62896673389d" />

---

## Available Tools

| Tool | Purpose |
|------|---------|
| `search_products` | Search products matching a user query. |
| `get_product_details` | Retrieve detailed information and specifications for a selected product. |
| `get_similar_products` | Find products related to a selected product. |
| `get_search_suggestions` | Provide search suggestions based on a partial user query. |

---

## Example Workflow

```text
User Request
      │
      ▼
search_products → Product List → get_product_details → Structured Product Information → AI Agent Response
```
