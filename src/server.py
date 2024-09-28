import falcon
import json

from src.db.repository import get_chats_by_thread_id
from src.rag.rag import RAGProcessor
from src.db.mock import createBotChat, createMockBotChat, createMockUserChat, createUserChat
from src.api.resource import MailResource

from langchain_core.messages import HumanMessage, AIMessage

class HelloWorldResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # HTTP status code
        resp.media = {"message": "Hello, World!"}

class TestResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        createMockUserChat()
        createMockBotChat()
        resp.status = falcon.HTTP_200  # HTTP status code
        resp.media = {"message": "MOCK DATA"}

class ChatResource:
    def on_post(self, req, resp):
        """Handles POST requests to create a chat message"""
        # Parse the JSON body
        raw_json = req.stream.read().decode('utf-8')
        data = json.loads(raw_json)

        # Extract fields from the JSON data
        thread_id = data.get('thread_id')
        message = data.get('message')
        sender_name = data.get('senderName')
        subject_type = data.get('subjectType')

        chat = createUserChat(thread_id=thread_id, message=message,senderName=sender_name)


        if(subject_type=='learning'):
            print('here',message )
            ragp =  RAGProcessor()
            chatList = get_chats_by_thread_id(thread_id)
            # history = 
            chatHist: 
            res = ragp.chat(message,[])
            print('res', res)
            botChat = createBotChat(thread_id=thread_id, message=res,metaData={})



        resp.status = falcon.HTTP_201  # HTTP status code for resource created
        resp.media = chat


# Create Falcon API instance
app = falcon.App(middleware=[falcon.CORSMiddleware(allow_origins="*", allow_credentials="*")])

# Add route to HelloWorldResource
hello_world = HelloWorldResource()
test = TestResource()
chatRes = ChatResource()


app.add_route("/hello", hello_world)
app.add_route("/test", test)
app.add_route("/chat", chatRes)

app.add_route("/email/action", MailResource())
