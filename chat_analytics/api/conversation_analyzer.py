
from flask_restx import Namespace, Resource
from chat_analytics.celery.tasks import save_conversation_analysis_task

from chat_analytics.core.analyzer import analyze_conversation, analyze_conversations


ns = Namespace(
    "conversations", "This namespace is responsible for conversation analysis"
)


conversation_parser = ns.parser()
conversation_parser.add_argument("conversation_id", type=str, default=None, location="values")


@ns.route("/<conversation_id>/analyze-now")
class ConversationAnalyzerPriority(Resource):
    def post(self, conversation_id):
        # Analyze convo conversation_id
        summary = analyze_conversation(conversation_id)
        return summary, 200


@ns.route("/<conversation_id>/analyze")
class ConversationAnalyzer(Resource):
    def post(self, conversation_id):
        save_conversation_analysis_task.delay(conversation_id)
        return {"message": "Conversation under analysis"}, 200
