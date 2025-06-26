CREATE EXTENSION IF NOT EXISTS vector;

DO $$
BEGIN
    RAISE NOTICE 'pgvector extension installed successfully';
END $$;
