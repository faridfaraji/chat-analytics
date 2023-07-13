

from chat_analytics.adapter.database import DatabaseApiClient
from chat_analytics.adapter.open_ai import OpenAI
from chat_analytics.schemas.conversation_summary import ConversationSummary

CLASSIFIER = {
    "Product Information": "Visitors may have questions about specific products, such as features, specifications, availability, and pricing. They may seek assistance in understanding the product details, comparing options, or finding alternatives.",

    "Order Status and Tracking": "Customers often want to know the status of their orders, including tracking information, estimated delivery dates, and any potential delays. They may inquire about order modifications, cancellations, or returns as well.",

    "Technical Support": "Some customers may encounter technical issues while using the online store, such as problems with the website, payment processing, or account access. They may seek assistance in troubleshooting these issues or require guidance to complete a transaction.",

    "Returns and Refunds": "Customers may have questions about the store's return policy, refund procedures, or how to initiate a return. They may require guidance on the necessary steps, documentation, or any specific conditions for returning products and obtaining refunds.",

    "Account Management": "Visitors might need help with account-related tasks, such as creating a new account, updating personal information, changing passwords, or recovering lost account access. They may also seek guidance on managing subscriptions or loyalty programs.",

    "Promotions and Discounts": "Customers may have queries about ongoing promotions, discounts, or coupon codes. They might seek clarification on the terms and conditions of offers, eligibility criteria, or how to apply promotional codes during checkout.",

    "General Inquiries and Complaints": "Visitors may have miscellaneous questions or concerns that do not fall under specific categories. These can include inquiries about store policies, shipping options, gift cards, or resolving any complaints or issues they have encountered while browsing or purchasing from the online store."
}


PROMPT = """
HERE IS LIST OF A CONVERSATION BETWEEN A CUSTOMER AND A SUPPORT AGENT, each conversation is a json with the following keys:
- conversation_id: str
- messages: list of json with the key of type which shows if the message is from the user or the ai.

You are the best and most efficient summarizer being a harvard professor in language and grammar. give me back a LIST of conversation summary between the AI and the USER for EACH conversation.
the result should be a LIST of Json (each string must be double quoted. DON't ADD newlines,  \n anywhere in your output) where EACH json has the following keys: conversation_id, summary, user_summary, ai_summary, title, classifications. 
Here are the descriptions of each key in the json:
the summary is the summary of the whole messages the ai_summary is the summary of the ai messages the user_summary is the summary of the user messages 
the title is a title you give to this conversation based on what the conversation is about 
the classification is a list of tags you give to this conversation based on what the conversation is about 
use the following json to choose the correct tags for each conversation {classifier}. 
IT IS VERY IMPORTANT THAT YOU OUTPUT YOUR RESPONSE IN EXACTLY THE FORMAT DESCRIBED.  
here is the list of conversations: {conversations}
"""


def get_conversation(conversation_id: str):
    messages = DatabaseApiClient.get_conversation_messages(conversation_id=conversation_id)
    return {
        "conversation_id": conversation_id,
        "messages": messages
    }


def validated_summaries(unvalidated_summaries: dict) -> list[ConversationSummary]:
    summaries = []
    for summary in unvalidated_summaries:
        summaries.append(ConversationSummary.make_object(summary))
    return summaries


def insert_summaries(summaries: ConversationSummary):
    for summary in summaries:
        DatabaseApiClient.add_conversation_summary(
            summary
        )


def analyze_conversation(conversation_id: str):
    conversations = []
    conversations.append(get_conversation(conversation_id))
    prompt = PROMPT.format(conversations=conversations, classifier=CLASSIFIER)
    result = OpenAI.summarize(prompt)
    insert_summaries(validated_summaries(result))
    return result


def analyze_conversations(conversation_ids: list[str]):
    conversations = []
    result = None
    for conversation_id in conversation_ids:
        conversations.append(get_conversation(conversation_id))
    if conversations:
        result = OpenAI.summarize(PROMPT.format(conversations=conversations))
        insert_summaries(validated_summaries(result))
    return result
