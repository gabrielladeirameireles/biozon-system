from datetime import datetime
from sqlalchemy.orm import Session
from app.models.change_request import ChangeRequest, RequestStatus
from app.models.content import SiteContent  # Tabela final de dados do site

class ApprovalService:

    @staticmethod
    def approve_change(db: Session, request_id: int, reviewer_id: int) -> bool:
        change_req = db.query(ChangeRequest).filter(ChangeRequest.id == request_id).first()
        if not change_req or change_req.status != RequestStatus.PENDING:
            return False

        # Atualiza a tabela oficial de publicação
        content_item = db.query(SiteContent).filter(SiteContent.key == change_req.section_name).first()
        if content_item:
            content_item.value = change_req.proposed_content
            if change_req.media_url:
                content_item.media_url = change_req.media_url
            content_item.updated_at = datetime.utcnow()
        else:
            new_content = SiteContent(
                key=change_req.section_name,
                value=change_req.proposed_content,
                media_url=change_req.media_url
            )
            db.add(new_content)

        # Atualiza o status do rascunho
        change_req.status = RequestStatus.APPROVED
        change_req.reviewer_id = reviewer_id
        change_req.reviewed_at = datetime.utcnow()

        db.commit()
        return True

    @staticmethod
    def reject_change(db: Session, request_id: int, reviewer_id: int, reason: str) -> bool:
        change_req = db.query(ChangeRequest).filter(ChangeRequest.id == request_id).first()
        if not change_req or change_req.status != RequestStatus.PENDING:
            return False

        change_req.status = RequestStatus.REJECTED
        change_req.reviewer_id = reviewer_id
        change_req.rejection_reason = reason
        change_req.reviewed_at = datetime.utcnow()

        db.commit()
        return True


    