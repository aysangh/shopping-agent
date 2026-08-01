# 🛒 Shopping Agent

An AI-powered shopping assistant for [Digikala](https://www.digikala.com/), an Iranian e-commerce platform, that uses an LLM agent, MCP-based product retrieval, and persistent memory for personalized product search and recommendations.

The project demonstrates:
- MCP tool integration
- LLM agent orchestration
- Short-term and long-term memory management
- Observability and tracing
- Containerized deployment with Docker
- Cloud deployment using AWS ECS Fargate

---

## 🏗️ Project Architecture

```
shopping-agent/

├── agent/
│   ├── app.py              # Agent creation and MCP connection
│   └── settings.py         # Configuration management
│
├── digikala_mcp/           # MCP server (see its own README)
│
├── ui/
│   └── streamlit_app.py    # User interface
│
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── README.md
```

---

# Overview

The system consists of three main layers: an agent layer for reasoning and orchestration, an MCP layer for product retrieval, and a memory layer for maintaining user preferences across conversations.

<p align="center">
  <img width="541" height="560" alt="overview" src="https://github.com/user-attachments/assets/82951c8c-35b6-426d-9432-a698f90b5526" />
</p>

---

# 🛠️ Technologies

| Category | Technology |
|-|-|
| Agent Framework | OpenAI Agents SDK |
| MCP Framework | FastMCP |
| UI | Streamlit |
| Memory | Mem0 |
| Vector Database | Qdrant |
| LLM | GPT-4o-nano |
| Embeddings | text-embedding-3-small |
| Containerization | Docker |
| Deployment | AWS ECS Fargate |

---

# 🔌 MCP Integration

The project uses a dedicated MCP server for product operations.

➡️ See [`digikala_mcp/README.md`](digikala_mcp/README.md)

---

# 🧠 Memory System

The agent supports both short-term and long-term memory to maintain conversation continuity and personalize responses.

### Short-term Memory

Short-term memory maintains the current conversation context during an active session. It is implemented using Streamlit session state.

### Long-term Memory

Long-term memory stores and retrieves user preferences across conversations using Mem0 with Qdrant-based vector storage, allowing the agent to provide personalized recommendations based on previous interactions.

<img width="990" height="595" alt="agent_memory" src="https://github.com/user-attachments/assets/f8e3fc8e-533b-410a-992a-4a3650f4696d" />

---

# 🔎 Observability

The agent execution was monitored using OpenAI Agent SDK tracing.
The trace provides visibility into the complete workflow, including
LLM calls, MCP tool invocations, tool arguments, execution order,
and latency measurements.

Example workflow:

1. User asks for product recommendations.
2. Agent calls `search_products` MCP tool.
3. Agent analyzes returned products.
4. Agent calls `get_product_details` for selected items.
5. Agent generates the final response.

<img width="1920" height="945" alt="trace" src="https://github.com/user-attachments/assets/e19d0540-6e50-434b-b3e7-0e66debe6d38" />


---

# 🚀 Running Locally

## Option 1: Virtual Environment

Clone the repository:

```bash
git clone https://github.com/aysangh/shopping-agent
cd shopping-agent
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -e .
```

Create the environment file and add required API keys:

```bash
echo "OPENAI_API_KEY=your_key_here" >> .env
```

Run:

```bash
streamlit run ui/streamlit_app.py
```

---

## Option 2: Docker

Build image:

```bash
docker build -t shopping-agent .
```

Run:

```bash
docker run --env-file .env -p 8501:8501 --name shopping-agent-app shopping-agent
```

---

# ☁️ AWS Deployment

The Docker image was pushed to Amazon Elastic Container Registry (ECR) and deployed using Amazon ECS Fargate. ECS Fargate provides serverless container execution with AWS-managed infrastructure for running the application.

The screenshot below shows the Amazon ECS Fargate task in the **Running** state, demonstrating a successful deployment of the shopping agent on AWS.


<img width="1447" height="623" alt="33" src="https://github.com/user-attachments/assets/74df9c48-7ed7-4fab-9621-6cbc1de4e1eb" />


---

## 🔄 CI/CD Pipeline

The CI/CD pipeline automates the process of validating, building, and deploying the application. 
Each push to the `main` branch triggers security checks with Trivy, builds a Docker image, scans the image for vulnerabilities, pushes it to Amazon ECR, and deploys the latest version to AWS ECS Fargate.

```text
Push to main
     |
     v
Trivy scan → Docker build → Trivy image scan → Push to ECR → Update ECS Fargate service
```

---

# 🎥 Demo

The demo video demonstrates the deployed application running on AWS ECS Fargate and accessed through its assigned public IP address.

[Watch the demo video](https://github.com/user-attachments/assets/415d6297-de16-409a-8a6d-e80ee37f665e)


---
