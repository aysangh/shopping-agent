import asyncio
import streamlit as st
from pathlib import Path
from mem0 import Memory
from agents import Runner, trace

from agent.app import create_agent
from agent.settings import Settings


settings = Settings()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = PROJECT_ROOT / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

@st.cache_resource
def load_memory():
    config = {
        "llm": {
            "provider": "openai",
            "config": {
                "api_key": settings.openai_api_key,
                "model": "gpt-4o-mini",  
            },
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "api_key": settings.openai_api_key,
                "model": "text-embedding-3-small",
            },
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "path": str(MEMORY_DIR / "qdrant"),
                "collection_name": "user_memory",
            },
        },
        "history_db_path": str(MEMORY_DIR / "user_pref.db"),
    }

    return Memory.from_config(config)


memory = load_memory()

st.set_page_config(
    page_title="Digikala Shopping Assistant",
    page_icon="🛒",
)
st.title("🛒 Digikala Shopping Assistant")

@st.cache_resource
def load_agent():
    return create_agent()

agent, mcp_server = load_agent()

# UI display history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Agent conversation memory
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

async def ask_agent(
    agent,
    mcp_server,
    conversation,
    user_input,
    max_turns,
    user_id="u1",
):

    # Save current user message
    memory.add(user_input, user_id=user_id)

    # Retrieve relevant memories
    memories = memory.search(
        user_input,
        filters={"user_id": user_id},
    )

    memory_lines = []
    for m in memories:
        if isinstance(m, dict):
            text = m.get("memory") or m.get("text")
            if text:
                memory_lines.append(f"- {text}")

    memory_text = "\n".join(memory_lines)

    # Add memory preferences to the user input
    enhanced_user_input = user_input

    if memory_text:
        enhanced_user_input = (
            "Known user preferences:\n"
            f"{memory_text}\n\n"
            f"User request: {user_input}"
        )

    async with mcp_server:
        with trace("shopping_agent"):

            result = await Runner.run(
                agent,
                conversation + [
                    {
                        "role": "user",
                        "content": enhanced_user_input,
                    }
                ],
                max_turns=max_turns,
            )

    return result
    
user_input = st.chat_input("Ask about products...")

if user_input:
    # Store user message 
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("🔍 Searching products and preparing an answer..."):

            try:
                result = asyncio.run(
                    ask_agent(
                        agent,
                        mcp_server,
                        st.session_state.conversation,
                        user_input,
                        settings.max_turns,
                    )
                )
                response = result.final_output

                # Save full conversation for continuity
                st.session_state.conversation = (
                    result.to_input_list()
                )

                # Save assistant message 
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

            except Exception as e:
                response = f"⚠️ Sorry, something went wrong: {e}"
                
            st.markdown(response)
