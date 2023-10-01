from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv()

class MongoConnection:
    def __init__(self):    
        user = os.getenv("MONGO_USER")
        password = os.getenv("MONGO_PASSWORD")
        db_hostname = os.getenv("MONGO_HOST")
        uri = f"mongodb+srv://{user}:{password}@{db_hostname}/?retryWrites=true&w=majority"
        self.client = MongoClient(uri, server_api=ServerApi('1'))

    def test_connection(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)


MongoConnection().test_connection()