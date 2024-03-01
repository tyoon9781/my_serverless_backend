from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.connection import Base


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
