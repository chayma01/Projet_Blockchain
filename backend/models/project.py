# Modèle Project 

from sqlalchemy import Column, String, Text, DateTime, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

from backend.config import Base


class Project(Base):
    __tablename__ = "projects"

    # Colonnes
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Blockchain
    contract_address = Column(String(42), unique=True, nullable=True)
    wallet_address = Column(String(42), unique=True, nullable=True)
    wallet_private_key = Column(Text, nullable=True)  # ⚠️ à chiffrer

    # Informations projet
    titre = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type_projet = Column(String(50), nullable=False)
    objectif_financier = Column(Numeric(18, 8), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)

    # Statistiques
    montant_collecte = Column(Numeric(18, 8), default=0)
    nombre_contributeurs = Column(Integer, default=0)

    # Status
    status = Column(String(20), default="draft", nullable=False)

    # Dates 
    deployed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relations
    creator = relationship("User", back_populates="created_projects")

    milestones = relationship(
        "Milestone",
        back_populates="project",
        cascade="all, delete"
    )

    contributions = relationship(
        "Contribution",
        back_populates="project",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Project(titre='{self.titre}', status='{self.status}')>"

    @property
    def pourcentage_atteint(self):
        if self.objectif_financier == 0:
            return 0
        return float((self.montant_collecte / self.objectif_financier) * 100)

    @property
    def jours_restants(self):
        if not self.deadline:
            return 0
        now = datetime.now(timezone.utc)
        delta = self.deadline - now
        return max(0, delta.days)

    @property
    def is_active(self):
        return self.status == "active"

    def to_dict(self):
        return {
            "id": str(self.id),
            "creator_id": str(self.creator_id),
            "contract_address": self.contract_address,
            "wallet_address": self.wallet_address,
            "titre": self.titre,
            "description": self.description,
            "type_projet": self.type_projet,
            "objectif_financier": float(self.objectif_financier),
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "montant_collecte": float(self.montant_collecte),
            "nombre_contributeurs": self.nombre_contributeurs,
            "pourcentage_atteint": self.pourcentage_atteint,
            "jours_restants": self.jours_restants,
            "status": self.status,
            "deployed_at": self.deployed_at.isoformat() if self.deployed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def to_dict_with_creator(self):
        data = self.to_dict()
        if self.creator:
            data["creator"] = self.creator.to_public_dict()
        return data