from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from datetime import datetime
from app.database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=True)

class ServiceOrder(Base):
    __tablename__ = "service_orders"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(150), nullable=False)
    client_phone = Column(String(20), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    equipment = Column(String(100), nullable=False)
    service_type = Column(String(100), nullable=False)
    status = Column(String(30), default="Pendente")
    scheduled_date = Column(String(50), nullable=True)
    
    # Detalhamento Financeiro e Fiscal
    value_parts = Column(Float, default=0.0)
    value_labor = Column(Float, default=0.0)
    total_value = Column(Float, default=0.0)
    payment_method = Column(String(50), nullable=True)
    invoice_number = Column(String(50), nullable=True)
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    next_maintenance_date = Column(String(50), nullable=True)
    
    notified = Column(Boolean, default=False)
    last_notified_at = Column(String(50), nullable=True)
    