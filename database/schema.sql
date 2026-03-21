-- Extension UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- USERS
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    wallet_address VARCHAR(42) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'creator', 'investor', 'admin'))
);

-- PROJECTS
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    creator_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    contract_address VARCHAR(42) UNIQUE,
    wallet_address VARCHAR(42) UNIQUE,
    wallet_private_key TEXT,
    
    titre VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    type_projet VARCHAR(50) NOT NULL,
    objectif_financier DECIMAL(18, 8) NOT NULL,
    deadline TIMESTAMP NOT NULL,
    
    montant_collecte DECIMAL(18, 8) DEFAULT 0,
    nombre_contributeurs INTEGER DEFAULT 0,
    
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN (
        'draft','pending','active','successful','failed','completed','refunded','cancelled'
    )),
    
    deployed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MILESTONES
CREATE TABLE milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    
    titre VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    montant DECIMAL(18, 8) NOT NULL,
    deadline TIMESTAMP NOT NULL,
    ordre INTEGER NOT NULL,
    
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN (
        'pending','active','completed','failed'
    )),
    
    date_fin TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_id, ordre)
);

-- CONTRIBUTIONS
CREATE TABLE contributions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    contributor_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    montant DECIMAL(18, 8) NOT NULL,
    hash_transaction VARCHAR(66) UNIQUE NOT NULL,
    numero_block BIGINT,
    
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN (
        'pending','confirmed','refunded','failed'
    )),
    
    date_contribution TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    refund_tx_hash VARCHAR(66),
    refunded_at TIMESTAMP
);
