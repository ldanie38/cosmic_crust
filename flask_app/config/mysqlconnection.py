import os
import pymysql.cursors
from urllib.parse import urlparse

class MySQLConnection:
    def __init__(self, db):
        # Try to get the database URL from JawsDB or ClearDB
        db_url = os.environ.get("JAWSDB_URL") or os.environ.get("CLEARDB_DATABASE_URL")
        if db_url:
            url = urlparse(db_url)
            connection = pymysql.connect(
                host=url.hostname,
                port=url.port or 3306,
                user=url.username,
                password=url.password,
                db=url.path.lstrip('/'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
        else:
            # Use local settings for development
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='Stanislav24',
                db=db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
        self.connection = connection

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
