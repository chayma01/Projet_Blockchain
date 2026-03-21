-- USERS
INSERT INTO users (wallet_address, username, email, password_hash, role) VALUES
('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1', 'alice', 'alice@example.com', 'hashed_pwd', 'creator'),
('0x5aeda56215b167893e80b4fe645ba6d5bab767de', 'bob', 'bob@example.com', 'hashed_pwd', 'investor'),
('0x1d96f2f6bef1202e4ce1ff6dad0c2cb002861d3e', 'charlie', 'charlie@example.com', 'hashed_pwd', 'user');

-- PROJECTS
INSERT INTO projects (
    creator_id,
    titre,
    description,
    type_projet,
    objectif_financier,
    deadline,
    status
) VALUES
(
    (SELECT id FROM users WHERE username = 'alice'),
    'Projet Blockchain',
    'Une plateforme innovante',
    'Tech',
    10.0,
    CURRENT_TIMESTAMP + INTERVAL '30 days',
    'active'
);

-- MILESTONES
INSERT INTO milestones (
    project_id,
    titre,
    description,
    montant,
    deadline,
    ordre,
    status
) VALUES
(
    (SELECT id FROM projects WHERE titre = 'Projet Blockchain'),
    'Phase 1',
    'Développement backend',
    5.0,
    CURRENT_TIMESTAMP + INTERVAL '15 days',
    1,
    'active'
);

-- CONTRIBUTIONS
INSERT INTO contributions (
    project_id,
    contributor_id,
    montant,
    hash_transaction,
    status
) VALUES
(
    (SELECT id FROM projects WHERE titre = 'Projet Blockchain'),
    (SELECT id FROM users WHERE username = 'bob'),
    1.5,
    '0x123abc456def',
    'confirmed'
);

-- TEST
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM contributions;
SELECT * FROM milestones;