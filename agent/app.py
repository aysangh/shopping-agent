from agents import Agent, OpenAIResponsesModel
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI

from .settings import Settings


settings = Settings()

openai_client = AsyncOpenAI(timeout=180)
model = OpenAIResponsesModel(
    model=settings.openai_model,
    openai_client=openai_client,
)

def create_agent():
    # Digikala MCP server
    digikala_server = MCPServerStdio(
        params={
            "command": "python",
            "args": [
                "digikala_mcp/server.py"
            ],
        },
        client_session_timeout_seconds=settings.mcp_timeout,
    )
    agent = Agent(
        name="Digikala Shopping Assistant",
        model=model,
        instructions=settings.system_prompt,
        mcp_servers=[
            digikala_server,
        ],
    )
    return agent, digikala_server
