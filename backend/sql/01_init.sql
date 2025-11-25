CREATE TABLE IF NOT EXISTS company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    logo_url VARCHAR(500),
    primary_color VARCHAR(7),
    secondary_color VARCHAR(7),
    instagram_handle VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS campaign (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS influencer (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES campaign(id) ON DELETE CASCADE,
    username VARCHAR(100) NOT NULL,
    platform VARCHAR(20) NOT NULL,
    full_name VARCHAR(255),
    followers_count INTEGER NOT NULL DEFAULT 0,
    aqs_score NUMERIC(5, 2) NOT NULL DEFAULT 0,
    quality_audience INTEGER NOT NULL DEFAULT 0,
    budget NUMERIC(12, 2),
    roi NUMERIC(12, 2),
    status VARCHAR(20) NOT NULL DEFAULT 'suggested',
    hypeauditor_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    company_id INTEGER REFERENCES company(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_company_slug ON company(slug);
CREATE INDEX idx_campaign_company ON campaign(company_id);
CREATE INDEX idx_influencer_campaign ON influencer(campaign_id);
CREATE INDEX idx_user_email ON "user"(email);
