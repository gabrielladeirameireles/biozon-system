import enum
from sqlalchemy import Column, Integer, String, Enum, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class RequestStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# Alias para compatibilidade com rotas existentes
RequestStatus = RequestStatusEnum

class ChangeRequest(Base):
    __tablename__ = "change_requests"

    id = Column(Integer, primary_key=True, index=True)
    target_entity = Column(String, nullable=False)
    target_id = Column(Integer, nullable=True)
    proposed_data = Column(Text, nullable=False)
    status = Column(Enum(RequestStatusEnum), default=RequestStatusEnum.PENDING)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    