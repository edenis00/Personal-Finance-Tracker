"""
savings model
"""
from sqlalchemy import Column, Integer, Float, String, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Savings(Base):
    """
    Savings model to track user's savings
    """
    __tablename__ = "savings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    current_amount = Column(Float, nullable=True)
    target_date = Column(TIMESTAMP(timezone=True), nullable=True)
    duration_months = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="savings")

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    def __repr__(self):
        return f"Savings: (id={self.id}, user_id={self.user_id}, amount={self.amount}, goal={self.goal})"
