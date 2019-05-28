import os

class Config:
    MONGO_DBNAME = "m4recipesCollection"
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")