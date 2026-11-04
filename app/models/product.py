from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    particle_retention = Column(String(50), nullable=True)
    chlorine_reduction = Column(String(50), nullable=True)
    bacteriological_efficiency = Column(String(50), nullable=True)
    flow_rate = Column(String(50), nullable=True)
    filter_lifespan = Column(String(50), nullable=True)
    image_url = Column(String(255), nullable=True)
    alt_text = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    