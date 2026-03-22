#Modèle Contribution 

from sqlalchemy import Column, String, DateTime, Numeric, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

from backend.config import Base

class Contribution(Base):
    __tablename__ = "contributions"
    # Colonnes
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    contributor_id = Column(UUID(as_uuid=True),ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    # Montant
    montant = Column(Numeric(18, 8), nullable=False)
    # Blockchain
    hash_transaction = Column(String(66), unique=True, nullable=False)
    numero_block = Column(BigInteger, nullable=True)
    # Status
    status = Column(String(20), default="pending", nullable=False)
    # Dates
    date_contribution = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    refunded_at = Column(DateTime(timezone=True), nullable=True)
    # Remboursement
    refund_tx_hash = Column(String(66), nullable=True)
    # Relations
    project = relationship("Project", back_populates="contributions")
    contributor = relationship("User", back_populates="contributions")

    def __repr__(self):
        return f"<Contribution(montant={self.montant}, status='{self.status}')>"

    @property
    def is_confirmed(self):
        return self.status == "confirmed"

    @property
    def is_refunded(self):
        return self.status == "refunded"

    def to_dict(self):
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "contributor_id": str(self.contributor_id),
            "montant": float(self.montant),
            "hash_transaction": self.hash_transaction,
            "numero_block": self.numero_block,
            "status": self.status,
            "date_contribution": self.date_contribution.isoformat() if self.date_contribution else None,
            "refunded_at": self.refunded_at.isoformat() if self.refunded_at else None,
            "refund_tx_hash": self.refund_tx_hash
        }

    def to_dict_with_relations(self):
        data = self.to_dict()
        if self.project:
            data["project"] = {
                "id": str(self.project.id),
                "titre": self.project.titre,
                "status": self.project.status
            }

        if self.contributor:
            data["contributor"] = self.contributor.to_public_dict()

        return data