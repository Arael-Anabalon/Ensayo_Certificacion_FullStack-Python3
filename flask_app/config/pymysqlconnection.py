import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()

class MySQLConnection:
    def __init__(self):
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),  
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data)
                tipo_consulta = query.strip().lower()
                if tipo_consulta.startswith("select"):
                    return cursor.fetchall()
                if tipo_consulta.startswith("insert"):
                    return cursor.lastrowid
                return cursor.rowcount
            except Exception as e:
                print("Something went wrong:", e)
                raise e 

def connectToMySQL(db=None):
    return MySQLConnection()