CREATE TABLE reference_table (
  id SERIAL PRIMARY KEY,
  reference_key TEXT UNIQUE NOT NULL,
  reference_type TEXT NOT NULL,
  reference_data JSONB NOT NULL
)