"""
Income model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, NUMERIC
from sqlalchemy.orm import relationship
from app.db.database import Base


class Income(Base):
    """
    incomes table
    """

    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(NUMERIC(precision=10, scale=2), nullable=False)
    source = Column(String, nullable=False)
    date = Column(TIMESTAMP, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="incomes")


    def __repr__(self):
        """
        String representation of the Income model
        """
        return f"<Income id={self.id} amount={self.amount} source={self.source} user_id={self.user_id}>"
