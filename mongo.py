from config import MONGO_URI
import time
import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class UserCredential:
    def __init__(self):
        self.uri = MONGO_URI
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client["techwizard"]  # Replace with your database name
        self.collection = self.db["credentials"]  # Replace with your collection name

    def save_credential(self, username, password):
      # we can update this function as per our need i just added this may be we will use only retrive function
        try:
          user = {"username": username, "password": password}
          result = self.collection.insert_one(user)
          print(f"Successfully saved user credential with id: {result.inserted_id}")
        except Exception as e:
          print(f"Error saving credential: {e}")

    def get_credential_by_username(self, username):
        try:
            user = self.collection.find_one({"username": username})
            if user:
                user['_id'] = str(user['_id'])
                return user['password']
            else:
                print("User not found.")
                return None
        except Exception as e:
            print(f"Error retrieving credential: {e}")
            return None   


class MongoMailManager:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_email_data(self, mail_data):
        try:
            # Add timestamp to the mail data
            mail_data["timestamp"] = datetime.datetime.utcnow()
            result = self.collection.insert_one(mail_data)
            print(f"Email data saved successfully. Inserted ID: {result.inserted_id}")
            return result.inserted_id  # Return inserted ID for potential use
        except Exception as e:
            print(f"Error saving email data: {e}")
            return None

    def retrieve_email_data(self, query=None): # Added query parameter
        try:
            if query:
              results = list(self.collection.find(query)) # Use query if given
            else:
              results = list(self.collection.find()) # Fetch all if query is None
            return results
        except Exception as e:
            print(f"Error retrieving email data: {e}")
            return None