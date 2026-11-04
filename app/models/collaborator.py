from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from app.database import Base

class RoleEnum(str, Enum):
    COORDINATOR = "COORDINATOR"  # Getúlio (ou a quem ele delegar)
    SUPERVISOR = "SUPERVISOR"    # Pode aprovar edições e gerenciar colaboradores
    COLLABORATOR = "COLLABORATOR"  # Pode propor edições (rascunhos)

class StatusEnum(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"

class Collaborator(Base):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.COLLABORATOR, nullable=False)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.PENDING, nullable=False)
    
    invite_token = Column(String(100), unique=True, nullable=True)
    invited_by = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    