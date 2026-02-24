from dataclasses import dataclass

from sqlalchemy import text


@dataclass
class ProcessingStatusRecord:
    message_id: str
    event_type: str
    status: str
    error_reason: str | None


class ProcessingStatusRepository:
    def __init__(self, db_session):
        self.db = db_session

    def get_by_message_id(self, message_id: str):
        query = text(
            """
            SELECT message_id, event_type, status, error_reason
            FROM processing_status
            WHERE message_id = :message_id
            LIMIT 1
            """
        )

        row = self.db.execute(query, {"message_id": message_id}).mappings().first()

        if not row:
            return None

        return ProcessingStatusRecord(
            message_id=row["message_id"],
            event_type=row["event_type"],
            status=row["status"],
            error_reason=row["error_reason"],
        )

    def start(self, message_id: str, event_type: str):
        existing = self.get_by_message_id(message_id)
        if existing:
            return existing

        insert_query = text(
            """
            INSERT INTO processing_status (message_id, event_type, status)
            VALUES (:message_id, :event_type, 'processing')
            """
        )
        self.db.execute(insert_query, {"message_id": message_id, "event_type": event_type})
        self.db.commit()

        return self.get_by_message_id(message_id)

    def mark_done(self, message_id: str):
        update_query = text(
            """
            UPDATE processing_status
            SET status = 'done',
                error_reason = NULL
            WHERE message_id = :message_id
            """
        )
        self.db.execute(update_query, {"message_id": message_id})
        self.db.commit()

    def mark_failed(self, message_id: str, reason: str):
        update_query = text(
            """
            UPDATE processing_status
            SET status = 'failed',
                error_reason = :reason
            WHERE message_id = :message_id
            """
        )
        self.db.execute(update_query, {"message_id": message_id, "reason": reason})
        self.db.commit()
