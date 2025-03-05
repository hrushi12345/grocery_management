import json
import uuid
import urllib
import pandas as pd
import pymysql
from models import db, Users, Order, OrderItem, UserProfile
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta


pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = "!@#$%QWER^&*()POIYTREWQ"

# Load config
with open('config.json', 'r') as file:
    data = json.load(file)

dbUserName = urllib.parse.quote_plus(data['username'])
dbPassword = urllib.parse.quote_plus(data['password'])
dbHost = data['host']
dbName = data['database']
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{dbUserName}:{dbPassword}@{dbHost}/{dbName}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Load dataset
DATASET_PATH = "dataset_grocery_items/grocery_list.csv"
data = pd.read_csv(DATASET_PATH)
categories = data['Category'].unique()

def get_items_by_category(category):
    return data[data['Category'] == category]['Product Name'].tolist()

@app.route('/')
def home():
    return render_template('home.html')

### 🔹 User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')        
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        # Check if user already exists
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))

        # Create user account
        user_id = str(uuid.uuid4())
        user = Users(user_id=user_id, email=email, passwordHash=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        profile = UserProfile(
            profileId=str(uuid.uuid4()),
            userId=user_id,
            name=name,
            address = address,
            phoneNumber=phone_number,
            updatedAt=datetime.utcnow()
        )
        db.session.add(profile)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

### 🔹 User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.passwordHash, password):
            session['user_id'] = user.user_id
            session['email'] = user.email
            userProfileObj = UserProfile.query.filter_by(userId=user.user_id).first()
            session['name'] = userProfileObj.name
            session['address'] = userProfileObj.address
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')

### 🔹 Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'cart' not in session:
        session['cart'] = []
    
    if request.method == 'POST':
        category = request.form['category']
        item = request.form['item']
        quantity = int(request.form['quantity'])
        price = float(data[data['Product Name'] == item]['Average Price (₹)'].values[0])
        
        session['cart'].append({'item': item, 'quantity': quantity, 'price': price})
        session.modified = True

    # Convert NumPy types to Python types
    items_by_category = {
        category: [str(item) for item in data[data['Category'] == category]['Product Name'].tolist()]
        for category in categories
    }
    
    total_amount = sum(item['quantity'] * item['price'] for item in session['cart'])
    
    return render_template('index.html', categories=categories, items_by_category=items_by_category, cart=session['cart'], total_amount=total_amount)


@app.route('/remove_item/<int:index>')
def remove_item(index):
    if 'cart' in session and 0 <= index < len(session['cart']):
        session['cart'].pop(index)
        session.modified = True
    return redirect(url_for('index'))

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    session.modified = True
    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        delivery_date = (datetime.utcnow() + timedelta(days=1)).strftime('%d-%m-%Y')
        total_amount = sum(item['quantity'] * item['price'] for item in session['cart'])

        user_id = session['user_id']
        # user = Users.query.filter_by(user_id=user_id).first()
        
        order = Order(user_id=user_id, total_price=total_amount, shipping_address=address, delivery_date=delivery_date)
        db.session.add(order)
        db.session.commit()
        
        for item in session['cart']:
            order_item = OrderItem(order_id=order.order_id, item = item['item'], quantity=item['quantity'], price_at_purchase=item['price'])
            db.session.add(order_item)
        db.session.commit()
        
        session['cart'] = []
        session.modified = True
        return render_template('result.html', name=name, email=email, address=address, 
                               cart=session['cart'], delivery_date=delivery_date, total_amount=total_amount)
        
    email = session['email']
    name = session['name']
    address = session['address']
    return render_template('checkout.html', name=name, email=email, address=address)

@app.route('/order_details', methods=['GET'])
def order_details():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect if no hotel selected
    email = session['email']
    name = session['name']
    address = session['address']
    orderObj = Order.query.filter_by(user_id=session['user_id']).first()
    if orderObj:
        delivery_date = orderObj.delivery_date
        total_amount = orderObj.total_price
        itemList = [
            {
                "item": item.item,
                "quantity": item.quantity,
                "price": item.price_at_purchase
            }
            for item in OrderItem.query.filter_by(order_id=orderObj.order_id).all()
        ]
        return render_template('result.html', name=name, email=email, address=address, 
                        cart=itemList, delivery_date=delivery_date, total_amount=total_amount)
    else:
        return render_template('result.html', name="")

@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # Redirect if no hotel selected
    orderObj = Order.query.filter_by(user_id=session['user_id']).first()

    if orderObj:  # Check if orderObj exists
        Order.query.filter_by(order_id=orderObj.order_id).delete()
        db.session.delete(orderObj)  # Correct way to delete an instance
        db.session.commit()  # Commit the changes
        flash("Order cancelled successfully!", "success")    
    else:
        flash("No order found for the given user.", "success")
    
    return render_template('result.html', name="")


if __name__ == '__main__':
    app.run(debug=True)
