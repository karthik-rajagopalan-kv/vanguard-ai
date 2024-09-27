from peewee import PostgresqlDatabase, Model, CharField, IntegerField

# Define the database connection
db = PostgresqlDatabase(
    'your_database_name',  # Replace with your DB name
    user='your_username',  # Replace with your DB user
    password='your_password',  # Replace with your DB password
    host='localhost',  # Replace with your DB host
    port=5432  # Replace with your DB port
)

# Base Model for the existing tables
class BaseModel(Model):
    class Meta:
        database = db  # Use the 'db' connection

# Define the model corresponding to the existing table
class DummyModel(BaseModel):
    username = CharField()  # Ensure these fields match your existing table structure
    age = IntegerField()

# Connect to the database
db.connect()