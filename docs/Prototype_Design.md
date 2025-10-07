# Product Prototype Design for XU-News-AI-RAG

## 1. Introduction

This document describes the user interface (UI) and user experience (UX) design for the XU-News-AI-RAG prototype. It outlines the layout and functionality of each page in the web application. The design prioritizes simplicity, clarity, and ease of use.

## 2. General Layout & Style

*   **Framework:** Bootstrap 5 is used for a responsive, mobile-first layout.
*   **Theme:** A clean and modern dark theme is used for the navigation bar, with a standard light theme for the main content area.
*   **Navigation:** A persistent top navigation bar provides access to major sections of the application.

## 3. Page Designs

### 3.1. Home Page (`/`)

*   **Purpose:** To introduce the application to new users and provide entry points for login and registration.
*   **Layout:**
    *   Centered content area.
    *   **Header:** "Welcome to XU-News-AI-RAG"
    *   **Subheading:** "Your intelligent assistant for personalized news consumption and knowledge management."
    *   **Call to Action Buttons:**
        *   A primary "Get Started" button that links to the Register page.
        *   A secondary "Login" button that links to the Login page.

### 3.2. Register Page (`/register`)

*   **Purpose:** To allow new users to create an account.
*   **Layout:**
    *   A standard form layout.
    *   **Header:** "Register"
    *   **Form Fields:**
        *   Username (Email address recommended) input field.
        *   Password input field.
    *   **Action Button:** A "Register" button to submit the form.
    *   **Error Display:** An alert box will appear above the button if registration fails (e.g., username already exists).

### 3.3. Login Page (`/login`)

*   **Purpose:** To allow existing users to sign in.
*   **Layout:**
    *   A standard form layout, similar to the Register page.
    *   **Header:** "Login"
    *   **Form Fields:**
        *   Username input field.
        *   Password input field.
    *   **Action Button:** A "Login" button to submit the form.
    *   **Error Display:** An alert box will appear if login fails.

### 3.4. Dashboard Page (`/dashboard`)

*   **Purpose:** This is the main workspace for authenticated users. It provides access to all core features of the application.
*   **Layout:** A multi-section page.

    *   **Section 1: Intelligent Search**
        *   **Header:** "Intelligent Search"
        *   **Component:** A search bar with a "Search" button.
        *   **Interaction:** User types a natural language question and clicks "Search".
        *   **Results Display:** Below the search bar, a card appears with the generated answer. The sources for the answer are listed in the footer of the card.

    *   **Section 2: Knowledge Base Management**
        *   **Header:** "Knowledge Base"
        *   **Component 1: File Upload:** An input group with a file selector and an "Upload" button.
        *   **Component 2: Document Filters:** A row of dropdowns and date pickers to filter the document list by type (All, TXT, PDF, Excel) and date range. A "Reset" button clears the filters.
        *   **Component 3: Document List:**
            *   A list of the user's documents.
            *   A "Delete Selected" button appears when one or more documents are selected.
            *   Each item in the list has:
                *   A checkbox for selection.
                *   The document's name/source.
                *   An "Edit" button to modify metadata.
                *   A "Delete" button.

    *   **Section 3: Edit Metadata Modal**
        *   **Trigger:** Appears when a user clicks the "Edit" button on a document.
        *   **Layout:** A modal dialog overlay.
        *   **Content:**
            *   A form with fields for "Source" and "Tags".
            *   A "Save Changes" button.
            *   A close button in the header.

    *   **Section 4: Data Analysis**
        *   **Header:** "Data Analysis"
        *   **Actions:**
            *   "Generate Keyword Report" button.
            *   "Generate Clustering Report" button.
        *   **Display Area:** When a report is generated, the results appear below the buttons.
            *   **Keywords:** Displayed as a simple list of the top 10 keywords.
            *   **Clustering:** Displayed as a series of lists, with each list representing a cluster and containing the top terms for that cluster.

    *   **Section 5: RSS Feed Management**
        *   **Header:** "RSS Feeds"
        *   **Component 1: Add Feed:** An input field for a URL with an "Add Feed" button.
        *   **Component 2: Feed List:** A list of the user's subscribed feeds. Each item shows the URL and has a "Delete" button.

## 4. Navigation Bar

*   **Appearance:** A dark, fixed-top navigation bar.
*   **Content (Unauthenticated):**
    *   Brand Name: "XU-News-AI-RAG" (links to Home).
    *   "Login" link.
    *   "Register" link.
*   **Content (Authenticated):**
    *   Brand Name: "XU-News-AI-RAG" (links to Home).
    *   "Dashboard" link.
    *   "Logout" button.
