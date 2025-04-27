

from flask import Flask, render_template, request, session, redirect, flash
from flask_app.config.mysqlconnection import connectToMySQL   

from flask_app import app
from flask_app.models.user import User
from flask_app.models.order import Order  
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    existing_customer = User.get_by_email(request.form["email"])
    if existing_customer:
        flash("Email already in use. Try logging in instead.", "register_error")
        return redirect('/')

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }

    customer_id = User.save(data)
    session["user_id"] = customer_id  # Store user session after registration
    return redirect('/dashboard')



@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/')

    user = User.get_by_id(session["user_id"])

    current_order = None
    order_id = session.get("current_order")  # ✅ Retrieve stored order ID
    if order_id:
        data = {"order_id": order_id}
        current_order = Order.get_by_id(data)
        session.pop("current_order", None)  # Remove after retrieving

    return render_template("dashboard.html", user=user, current_order=current_order, order_id=order_id)


@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/login_user', methods=['POST'])
def login_user():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db or not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid email or password.", "error")
        return redirect('/login')

    session["user_id"] = user_in_db.id  # ✅ Store correct customer ID
    print("✅ Session User ID After Login:", session["user_id"])  # 🔥 Debugging output

    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/order_pizza', methods=['POST'])
def order_pizza():
    if "user_id" not in session:
        flash("Please log in before placing an order.", "error")
        return redirect('/')

    print("✅ Confirming Session User ID Before Order:", session["user_id"])  

    # Validate form data before accessing
    required_fields = ["pizza_name", "size", "quantity"]
    if not all(field in request.form for field in required_fields):
        flash("Incomplete order details.", "error")
        return redirect('/dashboard')

    data = {
        "customer_id": session["user_id"],
        "pizza_name": request.form["pizza_name"],
        "size": request.form["size"],
        "quantity": request.form["quantity"],
        "instructions": request.form.get("instructions", "")  
    }

    print("🔎 Data Sent to `place_order()`: ", data)  

    new_order_id = Order.place_order(data)  # ✅ Get correct order ID
    session["current_order"] = new_order_id  # ✅ Store the ID properly

    if not new_order_id:
        flash("Failed to place order.", "error")
        return redirect('/dashboard')

    print("✅ New Order ID:", new_order_id)  
    return redirect('/dashboard')

@app.route('/order/<int:order_id>')
def order_details(order_id):
    if "user_id" not in session:
        return redirect('/')
    
    data = { "order_id": order_id }  
    order = Order.get_by_id(data)     
    
    if not order:
        flash("Order not found.", "order_error")
        return redirect('/dashboard')
    
    return render_template("order.html", order=order)



@app.route('/debug_db')
def debug_db():
    connection = connectToMySQL("db")  # ✅ Ensure correct DB name!
    db_name = connection.query_db("SELECT DATABASE();")
    print("🔥 Connected to Database:", db_name)  # Debugging output
    
    tables = connection.query_db("SHOW TABLES;")
    print("🛠 Tables in Current Database:", tables)  
    
    return f"Database: {db_name}, Tables: {tables}"





