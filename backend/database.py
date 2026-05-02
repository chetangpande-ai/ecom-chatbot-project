"""
Database configuration

"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os 

#load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

#get mongodb connection string from environment variable
MONGO_URI = os.getenv('MONGO_URI')

#initialize MongoDB client
client = MongoClient(MONGO_URI)
db=client['ecom'] #replace 'mydatabase' with your database name

#Collections    
users_collection = db['users'] #replace 'users' with your collection name   
products_collection = db['products'] #replace 'products' with your collection name
orders_collection = db['orders'] #replace 'orders' with your collection name
carts_collection = db['carts'] #replace 'carts' with your collection name
