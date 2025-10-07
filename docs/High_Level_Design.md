# High-Level Design Document for XU-News-AI-RAG

## 1. System Overview

XU-News-AI-RAG is a web-based application designed to be a personalized, intelligent news aggregation and knowledge management system. It allows users to create their own curated knowledge base from various sources, including RSS feeds and document uploads. The core functionality revolves around providing powerful semantic search capabilities over this knowledge base, assisted by Large Language Models (LLMs).

## 2. Key Goals and Objectives

*   **Personalization:** Allow users to build and manage a knowledge base tailored to their specific interests.
*   **Intelligence:** Use AI models to provide semantic search, summarization, and data analysis.
*   **Efficiency:** Automate the aggregation of news and provide a fast, intuitive interface for information retrieval.
*   **Extensibility:** Create a system that can be expanded with new data sources and AI capabilities in the future.

## 3. Major Components

The system is divided into three main components:

1.  **Frontend Application:** A single-page application (SPA) built with React that provides the user interface for all system interactions.
2.  **Backend Application:** A Flask-based API server that handles business logic, user authentication, data processing, and orchestration of AI services.
3.  **AI Services Layer:** A set of external services, including a Llama.cpp server, that provide the core AI functionalities (LLM, embeddings, reranking).

## 4. User Flow

1.  **Onboarding:**
    *   A new user visits the **HomePage**.
    *   They navigate to the **RegisterPage** to create an account.
    *   After successful registration, they are redirected to the **LoginPage**.

2.  **Authentication:**
    *   The user logs in with their credentials on the **LoginPage**.
    *   The backend authenticates the user and returns a JWT token.
    *   The frontend stores the token and redirects the user to their **DashboardPage**.

3.  **Knowledge Base Management (on Dashboard):**
    *   **View:** The user sees a list of their documents. They can filter this list by type and date.
    *   **Upload:** The user can upload new documents (PDF, TXT, XLSX). The backend processes and indexes these files.
    *   **RSS Feeds:** The user can add or remove RSS feed URLs. The backend periodically fetches new articles from these feeds and adds them to the user's knowledge base.
    *   **Manage:** The user can delete single or multiple documents and edit document metadata (source, tags).

4.  **Information Retrieval (on Dashboard):**
    *   **Search:** The user enters a natural language query into the search bar.
    *   The backend performs a semantic search on the user's knowledge base, reranks the results for relevance, and uses an LLM to generate a concise answer based on the retrieved documents.
    *   If no relevant documents are found, the system performs an external search (Bing API) and returns a summary of the top results.
    *   The results, including the answer and source documents, are displayed to the user.

5.  **Data Analysis (on Dashboard):**
    *   The user can request a **Keyword Report** to see the most frequent terms in their knowledge base.
    *   The user can request a **Clustering Report** to see documents grouped by topic.

## 5. Data Model

*   **User Data:** User account information (username, hashed password) is stored in a relational database (SQLite).
*   **Document Metadata:** Information about each document (file path, source, user ID, timestamps) is stored in the relational database.
*   **Vector Embeddings:** The vectorized content of the documents is stored in a FAISS index, with a separate index for each user to ensure data isolation.
*   **RSS Feeds:** URLs of RSS feeds subscribed to by users are stored in the relational database.

This high-level design ensures a separation of concerns between the user interface, business logic, and AI services, creating a modular and scalable system.
