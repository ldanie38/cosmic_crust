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
            VALUES (%(customer_id)s, %(pizza_name)s, %(size)s, %(quantity)s);
        '''
        connection = connectToMySQL("q3ef4i79gf4fl3e7")

        # 🔥 Print the formatted query for debugging
        formatted_query = query % data
        print("🔍 Running Query in Flask:", formatted_query)

        new_order_id = connection.query_db(query, data)
        print("✅ Inserted Order ID:", new_order_id)  # 🔥 Debugging after insert

        return new_order_id







    @classmethod
    def get_orders_by_customer(cls, customer_id):
        query = "SELECT * FROM orders WHERE customer_id = %(customer_id)s;"
        results = connectToMySQL(db).query_db(query, {"customer_id": customer_id})
        
        orders = [cls(order_data) for order_data in results]  # Optimized list creation
        return orders
    
    @classmethod
    def get_by_id(cls, data):
        print("Fetching Order with Data:", data)  # ✅ Debugging output

        # 🔥 Fix: Ensure `data` is a dictionary with a single key-value pair
        if isinstance(data, dict) and "order_id" in data:
            query = "SELECT * FROM orders WHERE id = %(order_id)s;"
            results = connectToMySQL(db).query_db(query, data)
            
            if results:
                print("Order Found:", results[0])
                return cls(results[0])
            
            print("⚠️ No Order Found")
            return None
        else:
            print("❌ Incorrect Data Format:", data)
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
