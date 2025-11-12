CREATE TABLE citations (
  id SERIAL PRIMARY KEY,
  citation_key TEXT UNIQUE NOT NULL,
  citation_type TEXT NOT NULL,
  citation_data JSONB NOT NULL
)