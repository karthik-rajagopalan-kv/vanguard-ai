from peewee import PostgresqlDatabase, Model, CharField, IntegerField, DateTimeField, UUIDField, TextField, ForeignKeyField
import uuid
import json
import datetime

# Define the database connection
db = PostgresqlDatabase(
    'projectdb',  # Replace with your DB name
    user='postgres',  # Replace with your DB user
    password='password',  # Replace with your DB password
    host='localhost',  # Replace with your DB host
    port=5432  # Replace with your DB port
)

# Base Model for the existing tables
class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    # created_at = DateTimeField(default=datetime.datetime.now)  # Use DateTimeField for PostgreSQL timestamp
    # updated_at = DateTimeField(default=datetime.datetime.now)  # Use DateTimeField for PostgreSQL timestamp
    deleted_at = DateTimeField(null=True)  # Use DateTimeField for nullable timestamp
    version = IntegerField(default=1)
    created_by = CharField(max_length=300, null=True)
    updated_by = CharField(max_length=300, null=True)

    class Meta:
        database = db  # Use the 'db' connection

    # Hook to update the `updated_at` field
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()  # Automatically update the timestamp
        return super(BaseModel, self).save(*args, **kwargs)

class ChatThread(BaseModel):
    subject_type = CharField(max_length=255)
    subject_id = UUIDField()

    class Meta:
        db_table = 'chat_thread'

class Chat(BaseModel):
    message = TextField()
    message_type = CharField(max_length=255)
    meta_data = TextField()  # Handle JSONB serialization
    sender_name = CharField(max_length=255, null=True)
    sender_type = CharField(max_length=255, null=True)
    thread_id = UUIDField(null=True)
    thread = ForeignKeyField(ChatThread, backref='chats', null=True, field='id')

    class Meta:
        db_table = 'chat'

    # Optional: to handle JSON serialization
    def set_meta_data(self, data):
        self.meta_data = json.dumps(data)

    def get_meta_data(self):
        return json.loads(self.meta_data)

# Define the model corresponding to the existing table
class DummyModel(BaseModel):
    username = CharField()  # Ensure these fields match your existing table structure
    age = IntegerField()

# Connect to the database
db.connect()
