#Modèle User 
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from backend.config import Base
class User(Base):
    __tablename__ = "users"

    # Colonnes
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_address = Column(String(42), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)

    # Relations
    created_projects = relationship(
        "Project",
        back_populates="creator",
        cascade="all, delete"
    )

    contributions = relationship(
        "Contribution",
        back_populates="contributor",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"

    def to_dict(self):
        #Format JSON pour API
        return {
            "id": str(self.id),
            "wallet_address": self.wallet_address,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }

    def to_public_dict(self):
        #Version publique (sans informations sensibles)
        return {
            "id": str(self.id),
            "username": self.username,
            "wallet_address": self.wallet_address,
            "role": self.role
        }