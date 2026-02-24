from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class QueueMessage:
    message_id: str
    event_type: str
    user_id: int
    payload: dict[str, Any]
    occurred_at: str
    schema_version: str = "1.0"

    @classmethod
    def create(cls, event_type: str, user_id: int, payload: dict[str, Any]) -> "QueueMessage":
        return cls(
            message_id=str(uuid4()),
            event_type=event_type,
            user_id=user_id,
            payload=payload,
            occurred_at=datetime.now(timezone.utc).isoformat(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "event_type": self.event_type,
            "user_id": self.user_id,
            "payload": self.payload,
            "occurred_at": self.occurred_at,
            "schema_version": self.schema_version,
        }
