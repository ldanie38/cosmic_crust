from flask_app.config.mysqlconnection import connectToMySQL

db = "pizza_system"

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
        query = '''
            INSERT INTO orders (customer_id, pizza_name, size, quantity, instructions)
            VALUES (%(customer_id)s, %(pizza_name)s, %(size)s, %(quantity)s, %(instructions)s);
        '''
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_orders_by_customer(cls, customer_id):
        query = "SELECT * FROM orders WHERE customer_id = %(customer_id)s;"
        results = connectToMySQL(db).query_db(query, {"customer_id": customer_id})
        
        orders = []
        for order_data in results:
            orders.append(cls(order_data))
        return orders
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM orders WHERE id = %(order_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0]) if results else None
    
    
    @classmethod
    def get_last_order_by_customer(cls, customer_id):
        query = """
            SELECT * FROM orders
            WHERE customer_id = %(customer_id)s
            ORDER BY created_at DESC
            LIMIT 1;
        """
        data = {"customer_id": customer_id}
        results = connectToMySQL(db).query_db(query, data)
        if results:
            return cls(results[0])
        return None




