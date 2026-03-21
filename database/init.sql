-- Script d'initialisation de la base de données PostgreSQL
CREATE USER crowdfunding_user WITH PASSWORD 'IA20cs26';

-- Création de la base de données
CREATE DATABASE crowdfunding_db
    OWNER = crowdfunding_user
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Accorder tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE crowdfunding_db TO crowdfunding_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO crowdfunding_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO crowdfunding_user;

-- Modification du owner du schéma public
ALTER SCHEMA public OWNER TO crowdfunding_user;
