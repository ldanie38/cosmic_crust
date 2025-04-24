

from flask import Flask, render_template, request, session, redirect, flash
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
    if "current_order" in session:
        data = {"order_id": session["current_order"]}
        current_order = Order.get_by_id(data)
        # Optionally, remove the session variable after retrieving
        session.pop("current_order", None)
    
    return render_template("dashboard.html", user=user, current_order=current_order)



@app.route('/order_pizza', methods=['POST'])
def order_pizza():
    if "user_id" not in session:
        flash("Please log in before placing an order.", "error")
        return redirect('/')

    data = {
        "customer_id": session["user_id"],  # Ensure correct user session
        "pizza_name": request.form["pizza_name"],
        "size": request.form["size"],
        "quantity": request.form["quantity"],
        "instructions": request.form.get("instructions", "") 
    }
    
    # Store this order id in the session
    new_order_id = Order.place_order(data)
    session["current_order"] = new_order_id
    flash("Order placed successfully!", "order_success")
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


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_user', methods=['GET', 'POST'],endpoint='process_login')
def login_user():
    if request.method == 'POST':
        data = {"email": request.form["email"]}
        user_in_db = User.get_by_email(data)

        if not user_in_db:
            flash("Invalid email or password.", "error")
            return redirect('/login')

        if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
            flash("Invalid email or password.", "error")
            return redirect('/login')

        session["user_id"] = user_in_db.id
        flash("Login successful!", "success")
        return redirect('/dashboard')

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


