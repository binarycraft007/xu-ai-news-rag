# Product Requirements Document (PRD) for XU-News-AI-RAG

## 1. Introduction

*   **Background:** In an era of information overload, users struggle to find relevant news and analysis efficiently. XU-News-AI-RAG aims to solve this by creating a personalized, intelligent news knowledge base. The system will aggregate news from various sources, allow users to manage this information, and provide powerful semantic search capabilities to find the most relevant content.
*   **Target Users:** Information consumers, researchers, and analysts who need to track specific topics in the news and require a tool to organize, search, and analyze information from a variety of sources.
*   **Product Vision:** To become the go-to intelligent assistant for personalized news consumption and knowledge management, empowering users to stay informed and gain insights from a curated and searchable repository of information.

## 2. User Stories and Scenario Descriptions

*   **As a user, I want to...**
    *   ...have the system automatically aggregate news from various sources like RSS feeds and websites, so I can discover new information without manual searching.
    *   ...register for an account and log in securely to access my personalized knowledge base.
    *   ...view all my collected documents in a list, with options to filter them by type (e.g., article, document) and time, so I can easily find what I'm looking for.
    *   ...manage my knowledge base by deleting single or multiple documents at once, and edit metadata like tags and sources to keep it organized.
    *   ...upload my own structured (Excel) and unstructured documents through a simple web interface to enrich my knowledge base.
    *   ...use a semantic search bar to ask questions in natural language and receive a list of the most relevant documents from my knowledge base, ranked by similarity.
    *   ...get relevant information from an online search (like Bing) if my own knowledge base doesn't contain the answer, with the top 3 results summarized for me.
    *   ...view a data clustering analysis report that shows the top 10 keywords in my knowledge base, helping me identify key themes and trends.
    *   ...receive an email notification with a custom title and message whenever new information is added to my knowledge base, so I can stay up-to-date.

## 3. Product Scope and Feature List

### In-Scope Features:

*   **F1: Automated News Aggregation:**
    *   Scheduled tasks to fetch news via RSS, web scraping, and intelligent agents.
*   **F2: User Authentication:**
    *   Secure user login and registration system using JWT.
*   **F3: Knowledge Base Management:**
    *   Web interface to view the list of stored data.
    *   Filter data by type and time.
    *   Single and batch deletion of data.
    *   Edit metadata (tags, sources).
    *   Upload various data types (structured and unstructured) through the web page.
*   **F4: Intelligent Search:**
    *   Semantic search function to query the knowledge base using natural language.
    *   Results ranked by similarity.
    *   If no relevant data is found in the knowledge base, trigger an online search (Bing API) and return the top 3 summarized results.
*   **F5: Data Analysis and Reporting:**
    *   Generate a data clustering analysis report.
    *   Display the Top 10 keyword distribution.
*   **F6: Notifications:**
    *   Automatically send an email notification with a customizable title and content when new information is stored in the knowledge base.

### Out-of-Scope for v1:

*   Social sharing features.
*   Real-time collaboration.
*   Mobile-native application.

## 4. Product-Specific AI Requirements

*   **4.1. Model Requirements:**
    *   **Large Language Model (LLM):**
        *   **Function:** Used for semantic search, query understanding, and summarizing external search results.
        *   **Implementation:** Deployed via llama-server, using the `ggml-org/Qwen3-1.7B-GGUF` model as recommended.
        *   **Interaction:** Accessed through a standardized API.
    *   **Embedding Model:**
        *   **Function:** To convert text data into vector representations for storage and similarity search.
        *   **Model:** `ggml-org/embeddinggemma-300M-GGUF`.
    *   **Reranking Model:**
        *   **Function:** To refine the search results and improve the relevance ranking.
        *   **Model:** `gpustack/bge-reranker-v2-m3-GGUF`.
*   **4.2. Data Requirements:**
    *   **Source:** RSS feeds, web scraping, and user-uploaded documents (Excel for structured data, and other unstructured formats).
    *   **Quantity:** Capable of handling a growing repository of news articles and documents.
    *   **Quality:** Data will be processed as-is from sources. The system must be robust to variations in quality.
    *   **Annotation:** Metadata such as data ID, type, source, and tags will be stored.
*   **4.3. Algorithm Boundaries and Interpretability:**
    *   The system will prioritize results from the internal knowledge base.
    *   Search results will be presented with similarity scores to provide a degree of interpretability.
    *   External search is a fallback and will be clearly indicated to the user.
*   **4.4. Evaluation Criteria:**
    *   Search relevance measured by user feedback (future feature) and precision/recall on a test set of queries.
    *   Keyword clustering quality evaluated by topic coherence.
*   **4.5. Ethics and Compliance:**
    *   Web scraping will adhere to `robots.txt` and website terms of service.
    *   User data privacy and security will be paramount.

## 5. Non-Functional Requirements

*   **Performance:**
    *   Search queries should return results in under 3 seconds.
    *   The system should support at least 10 concurrent users for v1.
*   **Security:**
    *   User authentication will be implemented using JWT.
    *   All data transmission will be over HTTPS.
*   **Usability:**
    *   The user interface should be intuitive and easy to navigate.
    *   The process for uploading and managing data should be straightforward.
*   **Scalability:**
    *   The architecture should allow for future scaling of the user base and data volume. To achieve data classification management and efficient retrieval, metadata (such as data ID, data type, etc.) will be stored in a relational database, while vector data will be stored separately in a FAISS vector database.
*   **Technology Stack:**
    *   **Frontend:** React
    *   **Backend:** Flask
    *   **Relational Database:** SQLite
    *   **Vector Database:** FAISS
    *   **Core Framework:** LangChain will be used to orchestrate the core AI logic, including:
        *   **Data Ingestion:** Using Document Loaders and Text Splitters to process and prepare incoming data.
        *   **Knowledge Base Creation:** Managing the creation of text embeddings.
        *   **Vector Storage and Retrieval:** Interfacing with the FAISS vector database.
        *   **Semantic Search and Q&A:** Building and managing the retrieval, reranking, and question-answering chains that power the intelligent search feature.

## 6. Release Criteria and Measurement Indicators

*   **Release Criteria:**
    *   All features listed in the "Product Scope" are implemented and pass testing.
    *   Unit, integration, and API tests are written and achieve >80% code coverage.
    *   The application is successfully deployed and operational.
    *   No critical or major bugs are present in the production environment.
*   **Measurement Indicators (Post-Release):**
    *   **User Engagement:** Daily/Monthly Active Users.
    *   **Feature Adoption:** Frequency of use for search, upload, and analysis features.
    *   **System Performance:** Average search response time, server uptime.
    *   **User Satisfaction:** (To be measured via user surveys in a future release).

## 7. Pending Items and Future Plans

*   **Pending Items:**
    *   Finalize the exact format for email notifications.
    *   Design the specific UI/UX for the data clustering report.
*   **Future Plans:**
    *   Introduce user feedback mechanisms for search results.
    *   Expand the range of supported data sources.
    *   Develop a native mobile application.
    *   Implement more advanced data visualization and analytics features.
    *   Support for team collaboration and shared knowledge bases.
