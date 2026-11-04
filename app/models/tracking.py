from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.database import Base

class TrackingTag(Base):
    __tablename__ = "tracking_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    code = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    