from infrastructure.database.models import ProcessingStatus


class ProcessingStatusRepository:
    def __init__(self, db_session):
        self.db = db_session

    def get_by_message_id(self, message_id: str):
        return self.db.query(ProcessingStatus).filter(ProcessingStatus.message_id == message_id).first()

    def start(self, message_id: str, event_type: str):
        existing = self.get_by_message_id(message_id)
        if existing:
            return existing

        status = ProcessingStatus(
            message_id=message_id,
            event_type=event_type,
            status="processing",
        )
        self.db.add(status)
        self.db.commit()
        self.db.refresh(status)
        return status

    def mark_done(self, message_id: str):
        status = self.get_by_message_id(message_id)
        if status:
            status.status = "done"
            self.db.commit()

    def mark_failed(self, message_id: str, reason: str):
        status = self.get_by_message_id(message_id)
        if status:
            status.status = "failed"
            status.error_reason = reason
            self.db.commit()
