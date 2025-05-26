from datetime import datetime
from sqlmodel import SQLModel, Field


class SearchHistory(SQLModel, table=True):
    __tablename__ = "search_history"
    id: int = Field(default=None, primary_key=True)
    city: str = Field(index=True, max_length=100)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
