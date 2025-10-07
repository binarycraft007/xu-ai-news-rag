# Technical Architecture Document for XU-News-AI-RAG

## 1. Introduction

This document outlines the technical architecture of the XU-News-AI-RAG system. It details the technology stack, component interactions, data flows, and deployment considerations.

## 2. Technology Stack

*   **Frontend:**
    *   **Framework:** React
    *   **UI Library:** Bootstrap
    *   **HTTP Client:** Axios
    *   **Package Manager:** npm

*   **Backend:**
    *   **Framework:** Flask
    *   **ORM:** SQLAlchemy
    *   **Authentication:** Flask-JWT-Extended (JWT-based)
    *   **Package Manager:** `uv`
    *   **WSGI Server:** Werkzeug (for development)

*   **Databases:**
    *   **Relational Database:** SQLite (for storing user data, document metadata, and RSS feeds)
    *   **Vector Database:** FAISS (for storing and searching text embeddings)

*   **AI/ML:**
    *   **Orchestration:** LangChain
    *   **Model Serving:** Llama.cpp server
    *   **Models:**
        *   **LLM:** `ggml-org/Qwen3-1.7B-GGUF`
        *   **Embedding:** `ggml-org/embeddinggemma-300M-GGUF`
        *   **Reranking:** `gpustack/bge-reranker-v2-m3-GGUF`

## 3. System Architecture Diagram

```
+-----------------+      +-------------------+      +---------------------+
|                 |      |                   |      |                     |
|  React Frontend |<---->|    Flask Backend  |<---->|   Llama.cpp Server  |
| (Browser)       |      |      (API)        |      | (LLM, Embedding, etc) |
|                 |      |                   |      |                     |
+-----------------+      +---------+---------+      +---------------------+
                                   |
                                   |
               +-------------------+-------------------+
               |                                       |
      +--------v--------+                     +--------v--------+
      |                 |                     |                 |
      |     SQLite      |                     |   FAISS Index   |
      | (Metadata)      |                     |   (Vectors)     |
      |                 |                     |                 |
      +-----------------+                     +-----------------+
```

## 4. Backend Architecture

The backend is a monolithic Flask application with a service-oriented architecture.

*   **`app.py`:** The main entry point, responsible for creating the Flask app, initializing extensions (CORS, SQLAlchemy, JWT), and registering blueprints.
*   **`config.py`:** Manages application configuration, loading values from environment variables.
*   **`models.py`:** Defines the SQLAlchemy database models (`User`, `Document`, `RssFeed`).
*   **Blueprints (`routes/` & `auth/`):**
    *   **`auth_bp`:** Handles user registration and login, issuing JWTs.
    *   **`main_bp`:** Defines the main API endpoints for document management, search, reporting, and feed management. It is protected by JWT authentication.
*   **Services (`services/`):**
    *   **`knowledge_base.py`:** Manages the lifecycle of documents. This includes uploading, processing, splitting, embedding, and indexing documents into FAISS. It also handles metadata operations in SQLite.
    *   **`search.py`:** Orchestrates the RAG pipeline using LangChain. It builds the retrieval and generation chain, interfaces with the vector store, and calls the reranking and LLM models. It also contains the fallback logic for Bing search.
    *   **`aggregation.py`:** Contains the logic for the background scheduler to fetch and process RSS feeds.
    *   **`clustering.py`:** Implements the logic for generating clustering reports using scikit-learn.
    *   **`custom_llm.py`, `custom_cross_encoder.py`:** Custom LangChain components that act as clients to the Llama.cpp server endpoints for the LLM and reranker models.
    *   **`notification.py`:** Handles sending email notifications.

## 5. Data Flow

### 5.1. Document Ingestion

1.  A user uploads a file via the React frontend.
2.  The Flask backend receives the file.
3.  `knowledge_base.py` saves the file to the `uploads/` directory.
4.  A LangChain `DocumentLoader` reads the file content.
5.  A `TextSplitter` splits the content into chunks.
6.  The `LlamaServerEmbeddings` service is called, which makes an HTTP request to the Llama.cpp server's embedding endpoint.
7.  The returned vectors are stored in the user-specific FAISS index file located at `faiss_index/user_<id>`.
8.  Metadata about the document is saved to the SQLite database.

### 5.2. Search Query (RAG)

1.  A user submits a query from the React frontend.
2.  The Flask backend's search endpoint is called.
3.  `search.py` takes the query and uses `LlamaServerEmbeddings` to vectorize it.
4.  The vectorized query is used to perform a similarity search against the user's FAISS index, retrieving the top-k document chunks.
5.  The `CrossEncoderReranker` (via `LlamaServerCrossEncoder`) is used to rerank these chunks for relevance.
6.  The top-n reranked chunks are formatted and inserted into a prompt template along with the original query.
7.  The final prompt is sent to the `LlamaServerLLM`, which generates an answer.
8.  The answer and the source document metadata are returned to the frontend.

## 6. Database Schema

The schema is defined by the SQLAlchemy models in `models.py`. See `database.sql` for the raw SQL statements.

*   **`user` table:** Stores user credentials.
*   **`document` table:** Stores metadata for uploaded documents and aggregated articles.
*   **`rss_feed` table:** Stores the RSS feed URLs for each user.

## 7. Deployment Considerations

*   **Backend:** The Flask application can be deployed using a production-ready WSGI server like Gunicorn or uWSGI behind a reverse proxy like Nginx.
*   **Frontend:** The React application should be built into static files (`npm run build`) and served by a web server like Nginx.
*   **AI Services:** The Llama.cpp server must be running as a separate, persistent service accessible by the backend. For production, it should be managed by a process supervisor like `systemd`.
*   **Environment Variables:** All sensitive information (secret keys, API keys, database URIs) must be configured via environment variables and not hardcoded.
