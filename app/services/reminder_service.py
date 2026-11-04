from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.customer import Customer

class ReminderService:
    @staticmethod
    def calculate_next_maintenance(installation_date: datetime, months: int = 6) -> datetime:
        return installation_date + timedelta(days=months * 30)

    @staticmethod
    def get_pending_maintenances(db: Session):
        now = datetime.utcnow()
        thirty_days_ahead = now + timedelta(days=30)
        return db.query(Customer).filter(Customer.next_maintenance_date <= thirty_days_ahead).all()

    