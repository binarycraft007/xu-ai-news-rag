-- This SQL file provides the necessary statements to create the database schema
-- for the XU-News-AI-RAG application, matching the SQLAlchemy models.

-- Create the 'user' table
CREATE TABLE user (
    id INTEGER NOT NULL,
    username VARCHAR(80) NOT NULL,
    password_hash VARCHAR(128),
    PRIMARY KEY (id),
    UNIQUE (username)
);

-- Create the 'document' table
CREATE TABLE document (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    source VARCHAR(255),
    tags VARCHAR(255),
    uploaded_at DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES user (id)
);

-- Create the 'rss_feed' table
CREATE TABLE rss_feed (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    url VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES user (id)
);
