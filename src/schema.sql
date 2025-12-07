CREATE TABLE reference_table (
  id SERIAL PRIMARY KEY,
  reference_key TEXT UNIQUE NOT NULL,
  reference_type TEXT NOT NULL,
  reference_data JSONB NOT NULL,
  comment TEXT DEFAULT ''
);

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE reference_taggins (
  reference_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY (reference_id, tag_id),
  FOREIGN KEY (reference_id) REFERENCES reference_table(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);


-- INDEXES for the full JSONB and most commonly searched keys for speed --
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE INDEX idx_reference_data_ft
ON reference_table USING GIN (
    to_tsvector('english', reference_data::text)
);

CREATE INDEX idx_reference_data_trgm
ON reference_table USING GIN ((reference_data::text) gin_trgm_ops);

CREATE INDEX idx_reference_year
ON reference_table ((CAST(reference_data->>'year' AS INT)));

CREATE INDEX idx_reference_title_trgm
ON reference_table USING GIN ((reference_data->>'title') gin_trgm_ops);

CREATE INDEX idx_reference_author_trgm
ON reference_table USING GIN ((reference_data->>'author') gin_trgm_ops);

CREATE INDEX idx_reference_publisher_trgm
ON reference_table USING GIN ((reference_data->>'publisher') gin_trgm_ops);

CREATE INDEX idx_reference_key_trgm
ON reference_table USING GIN (reference_key gin_trgm_ops);
