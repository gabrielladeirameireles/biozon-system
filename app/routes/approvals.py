from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.change_request import ChangeRequest, RequestStatusEnum

router = APIRouter(prefix="/admin/approvals", tags=["Aprovações"])

@router.get("/")
def list_pending_requests(db: Session = Depends(get_db)):
    return db.query(ChangeRequest).filter(ChangeRequest.status == RequestStatusEnum.PENDING).all()

@router.post("/{request_id}/approve")
def approve_request(request_id: int, db: Session = Depends(get_db)):
    req = db.query(ChangeRequest).filter(ChangeRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    req.status = RequestStatusEnum.APPROVED
    db.commit()
    return {"status": "success", "message": "Alteração aprovada com sucesso!"}

@router.post("/{request_id}/reject")
def reject_request(request_id: int, db: Session = Depends(get_db)):
    req = db.query(ChangeRequest).filter(ChangeRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    req.status = RequestStatusEnum.REJECTED
    db.commit()
    return {"status": "success", "message": "Alteração rejeitada."}
