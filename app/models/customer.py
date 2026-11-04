from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(120), nullable=True)
    product_model = Column(String(120), nullable=True)
    installation_date = Column(DateTime, default=datetime.utcnow)
    next_maintenance_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    