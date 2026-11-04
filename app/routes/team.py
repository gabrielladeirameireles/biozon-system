from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.collaborator import Collaborator, RoleEnum, StatusEnum
from app.services.invite_service import InviteService

router = APIRouter(prefix="/admin/team", tags=["Gestão de Equipe"])

@router.post("/invite")
def invite_collaborator(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    target_role: RoleEnum = Form(RoleEnum.COLLABORATOR),
    send_via: str = Form("whatsapp"),
    db: Session = Depends(get_db)
):
    existing = db.query(Collaborator).filter(Collaborator.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")

    token = InviteService.generate_token()
    new_user = Collaborator(
        full_name=full_name,
        email=email,
        phone=phone,
        role=target_role,
        status=StatusEnum.PENDING,
        invite_token=token,
        invited_by="Getúlio"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if send_via == "whatsapp":
        link = InviteService.build_whatsapp_invite_link(phone, full_name, token)
        return {"status": "success", "channel": "whatsapp", "invite_url": link}
    else:
        email_data = InviteService.build_email_invite_payload(email, full_name, token)
        return {"status": "success", "channel": "email", "payload": email_data}

@router.post("/delegate-coordinator/{target_user_id}")
def delegate_coordinator_role(
    target_user_id: int,
    current_user_id: int = 1,
    db: Session = Depends(get_db)
):
    current_user = db.query(Collaborator).filter(Collaborator.id == current_user_id).first()
    if not current_user or current_user.role != RoleEnum.COORDINATOR:
        raise HTTPException(status_code=403, detail="Apenas o Coordenador atual pode transferir seu cargo.")

    target_user = db.query(Collaborator).filter(Collaborator.id == target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Colaborador destino não encontrado.")

    current_user.role = RoleEnum.SUPERVISOR
    target_user.role = RoleEnum.COORDINATOR
    
    db.commit()
    return {"status": "success", "message": f"O cargo de Coordenador foi transferido para {target_user.full_name}."}


