import os
import pymysql

# Retrieve environment variable
db_url = os.environ.get("JAWSDB_URL") or os.environ.get("DATABASE_URL") or \
                 "mysql://x01qsgk792vgfrtd:bn9f9ptf7o18t3lj@d6vscs19jtah8iwb.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/q3ef4i79gf4fl3e7"
       


print("🔍 Checking environment variable...")
print("JAWSDB_CYAN_URL:", db_url)  # This MUST print a valid connection string

# If the database URL is missing, exit early
if not db_url:
    print("❌ ERROR: Database URL not found.")
    exit()

# Extract credentials manually for clarity
host = "d6vscs19jtah8iwb.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
user = 'x01qsgk792vgfrtd'
password = "bn9f9ptf7o18t3lj"
database = "q3ef4i79gf4fl3e7"

try:
    print("🔗 Attempting to connect to the database...")
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("✅ Database connection successful!")

    # Test query to check tables
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("📌 Existing tables:", tables)

    connection.close()

except Exception as e:
    print("❌ Connection failed:", e)
