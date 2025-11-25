import sqlite3

DB_NAME = "mercadinho.db"

def get_connection():
    return sqlite3.connect(DB_NAME)
