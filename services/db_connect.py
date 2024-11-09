import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_postgres():
    try:
        connection = psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"), 
            password=os.getenv("password"),
            port = os.getenv("port")
        )
        return connection
    except Exception as error:
        print("Error connecting to PostgreSQL database:", error)
        return None