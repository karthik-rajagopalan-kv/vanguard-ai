from typing import List
from peewee import DoesNotExist
import uuid
import json
from src.db.models import Chat, ChatThread  # Assuming your models are defined in a file named models.py

# Method to fetch a Chat record by its ID
def get_chat_by_id(chat_id: str):
    try:
        chat = Chat.get(Chat.id == uuid.UUID(chat_id))
        return chat
    except DoesNotExist:
        return None  # Handle if no record is found

# Method to fetch all Chats by Thread ID
def get_chats_by_thread_id(thread_id: str)-> List[Chat]: 
    try:
        chats = Chat.select().where(Chat.thread_id == uuid.UUID(thread_id))
        return list(chats)  # Return as list
    except DoesNotExist:
        return []  # Return an empty list if no records found

# Method to insert a new Chat record
def create_chat(data: dict):
    chat = Chat.create(
        message=data.get('message'),
        message_type=data.get('messageType'),
        meta_data=json.dumps(data.get('metaData', {})),  # Store JSON as text
        sender_name=data.get('senderName'),
        sender_type=data.get('senderType'),
        thread_id=uuid.UUID(data.get('threadId')) if data.get('threadId') else None
    )
    return chat

# # Method to update an existing Chat record
# def update_chat(chat_id: str, data: dict):
#     try:
#         chat = Chat.get(Chat.id == uuid.UUID(chat_id))
        
#         chat.message = data.get('message', chat.message)
#         chat.message_type = data.get('messageType', chat.message_type)
#         chat.meta_data = json.dumps(data.get('metaData', json.loads(chat.meta_data)))
#         chat.sender_name = data.get('senderName', chat.sender_name)
#         chat.sender_type = data.get('senderType', chat.sender_type)
#         chat.thread_id = uuid.UUID(data.get('threadId')) if data.get('threadId') else chat.thread_id
        
#         chat.save()  # Save changes
#         return chat
#     except DoesNotExist:
#         return None  # Handle if no record is found
