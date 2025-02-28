import json
import uuid
import urllib
import numpy as np
import pandas as pd
import pymysql
from models import db, Users, Order, OrderItem
from flask import Flask, render_template, request, redirect, url_for, session
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

@app.route('/', methods=['GET', 'POST'])
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

        # Store order information in database
        user = Users(username=name, email=email)
        db.session.add(user)
        db.session.commit()
        
        order = Order(user_id=user.user_id, total_price=total_amount, shipping_address=address)
        db.session.add(order)
        db.session.commit()
        
        for item in session['cart']:
            order_item = OrderItem(order_id=order.order_id, quantity=item['quantity'], price_at_purchase=item['price'])
            db.session.add(order_item)
        db.session.commit()        
        
        session['cart'] = []
        session.modified = True
        
        return render_template('result.html', name=name, email=email, address=address, 
                               cart=session['cart'], delivery_date=delivery_date, total_amount=total_amount)
    return render_template('checkout.html')


if __name__ == '__main__':
    app.run(debug=True)
