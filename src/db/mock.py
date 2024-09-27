from src.db.repository import create_chat

def createMockUserChat():
    thread_id = '661e4c51-c649-4429-a0fd-9b245c2dc42d'

    new_chat_data = {
        'message': 'Hello, world!',
        'messageType': 'prompt',
        'metaData': {},
        'senderName': 'John Doe',
        'senderType': 'sales_agent',
        'threadId': thread_id
    }
    new_chat = create_chat(new_chat_data)

def createMockBotChat():
    thread_id = '661e4c51-c649-4429-a0fd-9b245c2dc42d'

    new_chat_data = {
        'message': 'AI message',
        'messageType': 'prompt_reply',
        'metaData': {'key': 'value'},
        'senderName': 'Sales Genie',
        'senderType': 'chatbot',
        'threadId': thread_id
    }
    new_chat = create_chat(new_chat_data)    

def createUserChat(thread_id, message, senderName):
    new_chat_data = {
        'message': message,
        'messageType': 'prompt',
        'metaData': {},
        'senderName': senderName,
        'senderType': 'sales_agent',
        'threadId': thread_id
    }
    new_chat = create_chat(new_chat_data)

def createBotChat(thread_id, message, messageType, metaData ):
    thread_id = '661e4c51-c649-4429-a0fd-9b245c2dc42d'

    new_chat_data = {
        'message': 'AI message',
        'messageType': 'prompt_reply',
        'metaData': {'key': 'value'},
        'senderName': 'Sales Genie',
        'senderType': 'chatbot',
        'threadId': thread_id
    }
    new_chat = create_chat(new_chat_data)    