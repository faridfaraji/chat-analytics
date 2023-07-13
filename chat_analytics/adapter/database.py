import requests
from chat_analytics.config import config
from chat_analytics.schemas.conversation_summary import ConversationSummary


class DatabaseApiClient:
    # instance attribute
    config = config
    db_base_url = config.database.url_api_version

    @classmethod
    def _gen_url(cls, route):
        return f"{cls.db_base_url}/{route}"

    @classmethod
    def _make_request(cls, method, route, *args, **kwargs):
        response = method(
            cls._gen_url(route),
            *args,
            **kwargs,
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_conversation(cls, conversation_id):
        return cls._make_request(
            requests.get,
            f"conversations/{conversation_id}",
        )

    @classmethod
    def get_conversation_messages(cls, conversation_id):
        return cls._make_request(
            requests.get,
            f"conversations/{conversation_id}/messages",
        )

    @classmethod
    def add_conversation_summary(cls, summary: ConversationSummary):
        cls._make_request(
            requests.put,
            f"conversations/{summary.conversation_id}/summary",
            json=summary.to_dict(),
        )
