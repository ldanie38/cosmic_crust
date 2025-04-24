import os
import pymysql.cursors
from urllib.parse import urlparse

class MySQLConnection:
    def __init__(self, db):
        # Try to get your remote database URL from the environment.
        # On Heroku, you can set DATABASE_URL or JAWSDB_URL.
        # Otherwise, it will fall back to the hard-coded AWS RDS connection string.
        db_url = os.environ.get("JAWSDB_URL") or os.environ.get("DATABASE_URL") or \
                 "mysql://x01qsgk792vgfrtd:bn9f9ptf7o18t3lj@d6vscs19jtah8iwb.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/q3ef4i79gf4fl3e7"
        
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
        self.connection = connection

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                # Prepare the query with provided data, if any.
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query)
                # For insert queries, commit and return the lastrow id.
                if "insert" in query.lower():
                    self.connection.commit()
                    return cursor.lastrowid
                # For select queries, fetch and return all results.
                elif "select" in query.lower():
                    result = cursor.fetchall()
                    return result
                # For update or delete queries, commit changes.
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
