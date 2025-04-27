
       
import os
import pymysql.cursors
from urllib.parse import urlparse

class MySQLConnection:
    def __init__(self, db):
        # Check for Heroku environment variables first, fallback to JawsDB_CYAN or JawsDB_PINK
        #db_url = os.environ.get("JAWSDB_CYAN_URL") or os.environ.get("JAWSDB_PINK_URL")
        db_url = os.environ.get("JAWSDB_URL") or os.environ.get("DATABASE_URL") or \
                 "mysql://x01qsgk792vgfrtd:bn9f9ptf7o18t3lj@d6vscs19jtah8iwb.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/q3ef4i79gf4fl3e7"
       

        if not db_url:
            raise ValueError("Database URL not found in environment variables.")
            test_query = "SELECT @@hostname AS db_host;"


        url = urlparse(db_url)
        self.connection = pymysql.connect(
            host=url.hostname,
            port=url.port or 3306,
            user=url.username,
            password=url.password,
            db=url.path.lstrip('/'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                # Ensure data exists before using mogrify
                if data:
                    query = cursor.mogrify(query, data)

                print("Running Query:", query)
                
                cursor.execute(query, data if data else ())

                # Commit changes for insert, update, or delete queries
                if query.lower().startswith(("insert", "update", "delete")):
                    self.connection.commit()
                    return cursor.lastrowid if query.lower().startswith("insert") else True

                # Fetch results for select queries
                elif query.lower().startswith("select"):
                    return cursor.fetchall()
                
            except Exception as e:
                print("Something went wrong:", e)
                return False
            
            finally:
                cursor.close()  # Close cursor, but keep connection open

    def close_connection(self):
        """Manually close the database connection."""
        self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
