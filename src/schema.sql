CREATE TABLE reference_table (
  id SERIAL PRIMARY KEY,
  reference_key TEXT UNIQUE NOT NULL,
  reference_type TEXT NOT NULL,
  reference_data JSONB NOT NULL,
  comment TEXT DEFAULT ''
);

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
);

CREATE TABLE referece_x_tags (
  reference_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY (reference_id, tag_id),
  FOREIGN KEY (reference_id) REFERENCES reference_table(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);