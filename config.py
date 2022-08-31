import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

username = os.environ.get("MONGODB_USER")

password = os.environ.get("MONGODB_PWD")

mdb_connection_string = F"mongodb+srv://{username}:{password}@firstmongo.oday65l.mongodb.net/?retryWrites=true&w=majority"

redis_url = 'redis://localhost:6379'
