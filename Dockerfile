FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "ui/streamlit_app.py", "--server.address=0.0.0.0"]