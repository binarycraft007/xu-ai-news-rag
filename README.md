# XU-News-AI-RAG

XU-News-AI-RAG is a personalized, intelligent news knowledge base system. It aggregates news from various sources, allows users to manage this information, and provides powerful semantic search capabilities to find the most relevant content.

## Project Structure

-   `frontend/`: Contains the React frontend application.
-   `backend/`: Contains the Flask backend application.

## Features

-   **Automated News Aggregation:** Scheduled tasks to fetch news via RSS.
-   **User Authentication:** Secure user login and registration system using JWT.
-   **Knowledge Base Management:** Web interface to upload, view, and delete documents.
-   **Intelligent Search:** Semantic search with reranking and Bing search fallback.
-   **Data Analysis and Reporting:** Generates a data clustering analysis report with top keywords.
-   **Notifications:** Sends email notifications when new information is stored in the knowledge base.

## Documentation

Detailed project documentation can be found in the `docs/` directory:

-   [**Product Requirements Document (PRD)**](./docs/PRD.md)
-   [**High-Level Design**](./docs/High_Level_Design.md)
-   [**Technical Architecture**](./docs/Technical_Architecture.md)

## Technology Stack

-   **Frontend:** React, Bootstrap
-   **Backend:** Flask, SQLAlchemy, `uv`
-   **Database:** SQLite, FAISS
-   **AI:** LangChain, Llama.cpp server

## Setup and Deployment

### Prerequisites

-   Python 3.11+
-   Node.js and npm
-   `uv` (Python package manager) - see [uv setup guide](./docs/uv.md) for installation.
-   A running `llama-server` instance with the required models.

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Configure environment variables:**
    Create a `.env` file in the `backend` directory and populate it with the necessary values (see `.env.example` for a template).

4.  **Run the backend server:**
    ```bash
    uv run -m flask run --host=0.0.0.0
    ```

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the frontend development server:**
    ```bash
    npm start
    ```

The application will be available at `http://localhost:3000`.

## Usage

1.  **Register an account:** Create a new user account.
2.  **Login:** Log in to access your dashboard.
3.  **Upload Documents:** Upload your own documents (TXT, PDF, XLSX) to build your knowledge base.
4.  **Search:** Use the semantic search bar to ask questions in natural language.
5.  **Reports:** Generate a keyword report to identify key themes in your knowledge base.

## Llama Server Setup

Refer to the [**Llama Server Setup Guide**](./docs/llama-server.md) for detailed instructions on how to set up and run the `llama-server` from the original `llama.cpp` project.

### Building and Running llama.cpp

These commands assume you have cloned the `llama.cpp` repository and are in its root directory.

**Build:**
```bash
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release
```

**Run:**
Create a logs directory and run the servers in the background:
```bash
mkdir -p logs
./build/bin/llama-server -hf ggml-org/Qwen3-1.7B-GGUF --log-file logs/llm.txt &
./build/bin/llama-server -hf ggml-org/embeddinggemma-300M-GGUF --embeddings --port 8081 --log-file logs/embedding.txt &
./build/bin/llama-server -hf gpustack/bge-reranker-v2-m3-GGUF --reranking --port 8082 --log-file logs/reranking.txt &
```

The required models are:

-   **LLM:** `ggml-org/Qwen3-1.7B-GGUF`
-   **Embedding Model:** `ggml-org/embeddinggemma-300M-GGUF`
-   **Reranking Model:** `gpustack/bge-reranker-v2-m3-GGUF`
