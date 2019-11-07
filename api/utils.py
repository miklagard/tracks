import api.chat as chat
from django.conf import settings

def get_chatbot_respond(user_message, session):
    chat_node = session.get("chat_node")
    
    if chat_node == None:
        # Initial welcome message
        node = getattr(chat, settings.CHAT_START_NODE)(session)
        session["chat_node"] = settings.CHAT_START_NODE
    else:
        getattr(chat, chat_node)(session, user_message)

    next_chat_node = session.get("next_chat_node")

    if next_chat_node:
        session['chat_node'] = next_chat_node
        node = getattr(chat, next_chat_node)(session)

    return dict(
        message=node.text,
        terminate=node.terminate
    )
