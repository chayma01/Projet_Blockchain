#Configuration de la base de données PostgreSQL avec SQLAlchemy
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# URL de connexion
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://crowdfunding_user:IA20cs26@localhost:5432/crowdfunding_db"
)

# Engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True, # Vérifie la connexion avant chaque utilisation
    echo=False  #mettre à True pour debug SQL 
)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Dependency pour FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonction d'initialisation de la base de données
def init_db():
    #Creation des tables de la base de données
    Base.metadata.create_all(bind=engine)
    
# Test connexion
def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Connexion réussie")
        return True
    except Exception as e:
        print(f" Erreur DB: {e}")
        return False