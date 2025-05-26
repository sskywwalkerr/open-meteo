from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from app.database.db import Base


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    search_time = Column(DateTime, default=datetime.utcnow)