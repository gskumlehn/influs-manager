CREATE TABLE IF NOT EXISTS company (
  id INT64 NOT NULL,
  name STRING NOT NULL,
  slug STRING NOT NULL,
  logo_url STRING,
  primary_color STRING,
  secondary_color STRING,
  instagram_handle STRING,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS campaign (
  id INT64 NOT NULL,
  company_id INT64 NOT NULL,
  name STRING NOT NULL,
  description STRING,
  status STRING NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS user (
  id INT64 NOT NULL,
  email STRING NOT NULL,
  password_hash STRING NOT NULL,
  role STRING NOT NULL,
  company_id INT64,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS influencer (
  id INT64 NOT NULL,
  campaign_id INT64 NOT NULL,
  username STRING NOT NULL,
  platform STRING NOT NULL,
  full_name STRING,
  followers_count INT64 NOT NULL,
  aqs_score FLOAT64 NOT NULL,
  quality_audience INT64 NOT NULL,
  budget FLOAT64,
  roi FLOAT64,
  status STRING NOT NULL,
  hypeauditor_data STRING,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
