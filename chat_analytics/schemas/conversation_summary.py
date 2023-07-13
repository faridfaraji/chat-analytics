
from dataclasses import dataclass
from typing import List

from chat_analytics.schemas.artifact import Artifact


@dataclass
class ConversationSummary(Artifact):
    summary: str = ""
    ai_summary: str = ""
    user_summary: str = ""
    title: str = ""
    classifications: str = ""
    conversation_id: str = ""

    @classmethod
    def make_object(cls, data: dict):
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def to_dict(self):
        return {
            "summary": self.summary,
            "title": self.title,
            "classifications": self.classifications
        }
