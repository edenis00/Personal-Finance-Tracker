"""
Expense model
"""
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, NUMERIC
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Expense(Base):
    """
    expenses table
    """

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(NUMERIC(precision=10, scale=2), nullable=False)
    category = Column(String, nullable=False)
    date = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="expenses")


    def __repr__(self):
        """
        String representation of the Expense model
        """
        return f"<Expense id={self.id} amount={self.amount} category={self.category} user_id={self.user_id}>"
