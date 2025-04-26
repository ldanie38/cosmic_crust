from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

db = "q3ef4i79gf4fl3e7"


# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        data["password"] = data["password"].decode("utf-8")
        query = '''INSERT INTO customers (first_name, last_name, email, password)
                   VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'''
        print(f"Data being inserted: {data}")
        print("Data structure:", data)
        print("Query:", query)

        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM customers WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {"id": user_id})
        return cls(results[0]) if results else None
    
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM customers WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0]) if results else None



    
 
