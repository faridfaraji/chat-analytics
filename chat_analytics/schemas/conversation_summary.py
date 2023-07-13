
from dataclasses import dataclass
from typing import List

from chat_analytics.schemas.artifact import Artifact


@dataclass
class ConversationSummary(Artifact):
    summary: str = ""
    ai_summary: str = ""
    user_summary: str = ""
    title: str = ""
    classifications: List[str] = None
    conversation_id: str = ""

    @classmethod
    def make_object(cls, data: dict):
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def to_dict(self):
        classification = ", ".join(self.classifications) if self.classifications else None
        return {
            "summary": self.summary,
            "title": self.title,
            "classifications": classification,
        }
