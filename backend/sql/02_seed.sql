INSERT INTO company (name, slug, logo_url, primary_color, secondary_color, instagram_handle)
VALUES 
    ('Papelito', 'papelito', 'https://example.com/logo.png', '#FF6B6B', '#4ECDC4', 'papelitobrasil'),
    ('Demo Company', 'demo', NULL, '#3498db', '#2ecc71', NULL)
ON CONFLICT (slug) DO NOTHING;

INSERT INTO campaign (company_id, name, description, status)
VALUES 
    (1, 'Campanha Verão 2024', 'Campanha de influenciadores para o verão', 'active'),
    (2, 'Lançamento de Produto', 'Divulgação do novo produto', 'draft')
ON CONFLICT DO NOTHING;
