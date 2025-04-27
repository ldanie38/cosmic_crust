from flask_app.config.mysqlconnection import connectToMySQL

db = "q3ef4i79gf4fl3e7"

class Order:
    def __init__(self, data):
        self.id = data['id']
        self.customer_id = data['customer_id']
        self.pizza_name = data['pizza_name']
        self.size = data['size']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.instructions = data.get("instructions")
        

        
    @classmethod
    def place_order(cls, data):
        print("🔎 Data Being Inserted into Orders:", data)  # ✅ Debugging before insert

        query = '''
            INSERT INTO orders (customer_id, pizza_name, size, quantity, instructions)
            VALUES (%(customer_id)s, %(pizza_name)s, %(size)s, %(quantity)s, %(instructions)s);
        '''
        
        connection = connectToMySQL(db)  # ✅ Ensure correct DB name!
        new_order_id = connection.query_db(query, data)

        print("✅ Inserted Order ID:", new_order_id)  # 🔥 Debugging after insert

        # 🔥 Force retrieval of last inserted order ID if `query_db()` doesn't return it
        if not new_order_id:
            last_id_query = "SELECT LAST_INSERT_ID() AS id;"
            last_id_result = connection.query_db(last_id_query)

            print("🔍 Forced Order ID Retrieval:", last_id_result)  # ✅ Debugging retrieval
            return last_id_result[0]['id'] if last_id_result else None

        return new_order_id










    @classmethod
    def get_orders_by_customer(cls, customer_id):
        query = "SELECT * FROM orders WHERE customer_id = %(customer_id)s;"
        results = connectToMySQL(db).query_db(query, {"customer_id": customer_id})
        
        orders = [cls(order_data) for order_data in results]  # Optimized list creation
        return orders
    
    @classmethod
    def get_by_id(cls, data):
        print("🔎 Fetching Order with Data:", data)  

        query = "SELECT * FROM orders WHERE id = %(order_id)s;"
        print("🚀 Running Query in Flask:", query % data)  # ✅ Debugging query format
        results = connectToMySQL(db).query_db(query, data)

        print("🔍 Query Results:", results)  # ✅ Debugging output

        if results:
            print("✅ Order Found:", results[0])
            return cls(results[0])

        print("⚠️ No Order Found")
        return None



    @classmethod
    def get_last_order_by_customer(cls, customer_id):
        query = """
            SELECT * FROM orders
            WHERE customer_id = %(customer_id)s
            ORDER BY created_at DESC
            LIMIT 1;
        """
        results = connectToMySQL(db).query_db(query, {"customer_id": customer_id})
        return cls(results[0]) if results else None
