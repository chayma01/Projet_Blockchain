#Modèle Milestone 

from sqlalchemy import Column, String, Text, DateTime, Numeric, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

from backend.config import Base


class Milestone(Base):
    __tablename__ = "milestones"
    __table_args__ = (
        UniqueConstraint('project_id', 'ordre', name='unique_project_ordre'),
    )
    # Colonnes
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    titre = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    montant = Column(Numeric(18, 8), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    ordre = Column(Integer, nullable=False)
    # Status
    status = Column(String(20), default="pending", nullable=False)
    # Dates
    date_fin = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # Relations
    project = relationship("Project", back_populates="milestones")

    def __repr__(self):
        return f"<Milestone(titre='{self.titre}', ordre={self.ordre}, status='{self.status}')>"
    
    @property
    def is_completed(self):
        return self.status == "completed"

    def to_dict(self):
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "titre": self.titre,
            "description": self.description,
            "montant": float(self.montant),
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "ordre": self.ordre,
            "status": self.status,
            "date_fin": self.date_fin.isoformat() if self.date_fin else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }