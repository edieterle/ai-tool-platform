-- Enable pgvector for embedding support 
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the regular documents table
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Insert a sample document for testing
INSERT INTO documents (title, content)
VALUES (
    'Test Text Document Title',
    'Test text document content'
)
ON CONFLICT (title) DO NOTHING;
