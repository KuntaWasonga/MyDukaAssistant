import json
from flask import Flask, request, jsonify
#from datetime import datetime, timedelta, timezone
from mda import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
#from functools import wraps
#from flask_jwt_extended import (create_access_token,get_jwt,get_jwt_identity,
                                #unset_jwt_cookies, jwt_required, JWTManager )
#from flask_cors import CORS

from mda.models import User, Employee, Product, Cart, cart_product


#-------------------------------------------------------------------------------------#
#This API registers a client to the database
@app.route("/register", methods=["GET", "POST"])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    #Check for missing fields
    required_fields = ['firstname', 'lastname', 'email', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    #Check if the user already exists
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({"error": "Email already exists"}), 409

    hashed_password = generate_password_hash(data['password'])

    new_client = User(
        firstname = data['firstname'],
        lastname = data['lastname'],
        email = data['email'],
        password = hashed_password)
    
    db.session.add(new_client)
    db.session.commit()

    return jsonify({"messsage": "Registration successful"})


#This API is responsible for User login
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    required_fields = ['username', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    user = User.query.filter_by(firstname=data['username']).first()
    if user:
        if check_password_hash(user.password, data["password"]):
            login_user(user)
            return jsonify({"message": "Login successful"}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/users')
def users():
    users = User.query.all()

    output = []
    for User in users:
        item_data = {}
        item_data['firstname'] = User.firstname
        item_data['lastname'] = User.lastname
        item_data['email'] = User.email
        item_data['password'] = User.password

        output.append(item_data)
        
    return jsonify({"users" : output})


#This API edits various properties of a client
@app.route("/user/edit", methods=["PUT"])
@login_required
def edit():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    required_fields = ['firstname', 'lastname', 'email', 'bio']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    user = User.query.get(current_user.id)
    if user:
        user.firstname = data['firstname']
        user.lastname = data['lastname']
        user.email = data['email']
        user.bio = data["bio"]

        db.session.commit()

        return jsonify({"message": f"{(user.firstname)} successfully updated"}), 200

    return jsonify({'message': 'Not authorized'}), 401


#This API logs out a User
@app.route('/user/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message' : 'Logout successful'}), 200

#This API deletes a client from the database
@app.route("/user/delete", methods =['DELETE'])
@login_required
def delete():
    mtu = User.query.get(current_user.id)
    if mtu:
        db.session.delete(mtu)
        db.session.commit()
        return jsonify({'message': f'{mtu.firstname} successfully deleted'}), 200
    return jsonify({'message': 'Not authorized'}), 409

#------------------------------------------------------------------#
#----------------------PRODUCT APIS--------------------------------#

#This API adds a new product to the database
@app.route('/product/add', methods=['POST'])
@login_required
def new_product():
    # Check if the user is an employee
    user = Employee.query.get(current_user.id)
    if not user:
        return jsonify({'message': 'Unauthorized access'}), 401

    # Retrieve JSON data from the request
    data = request.get_json()

    # Validate required fields in the data
    required_fields = ['id', 'barcode', 'name', 'price']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

    # Check if the product already exists
    product_exists = Product.query.filter_by(barcode=data['barcode']).first()
    if product_exists:
        return jsonify({'message': 'Product already exists'}), 409

    # Create a new product object
    new_product = Product(
        id=data['id'],
        barcode=data['barcode'],
        name=data['name'],
        price=data['price']
    )

    # Add the new product to the database
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': f'{new_product.name} added'}), 200


#This API reads properties of a product
@app.route('/product/scan/<scan>')
@login_required
def read_product(scan):
    item = Product.query.filter_by(barcode=scan).first()

    if not item:
        return jsonify({'message':'This item does not exist'}), 409

    output = []
    for i in item:
        item_data = {}
        item_data['id'] = item.id
        item_data['barcode'] = item.barcode
        item_data['name'] = item.name
        item_data['price'] = item.price
        output.append(item_data)

    return jsonify({'item': output}), 200


#This API updates properties of a product
@app.route('/product/update/<product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    #checks for User access (meant to be employees only)
    user_authorized = Employee.query.filter_by(email=current_user.email).first()
    if not user_authorized:
        return jsonify({'message' : 'Unauthorized access'}), 401

    data = request.get_json()
    #checks if product exists
    product = Product.query.filter_by(id=product_id).first()
    if product:
        product.id = data['id'],
        product.barcode = data['barcode']
        product.name = data['name']
        product.price = data['price']

        db.session.commit()

        return jsonify({'message' : f'{product.name} updated successfully'}), 200
    return jsonify({'message' : 'Product does not exist'}), 404


#This API deletes a product
@app.route('/product/delete/<product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    #checks for User access (meant to be employees only)
    user_authorized = Employee.query.filter_by(email=current_user.email).first()
    if not user_authorized or user_authorized.admin:
        return jsonify({'message' : 'Unauthorized access'}), 401

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'product does not exist'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message' : 'Product deleted'}), 200


#-----------------------------------------------------------------------------------#
#-------------------------------------CART APIS-------------------------------------#
#This adds additional items to a user's cart.
@app.route('/updateCart/<scan>', methods=["PUT"])
@login_required
def add_to_cart(scan):
    user = User.query.get(current_user.id)
    if user:
        product = Product.query.filter_by(barcode=scan).first()

        if not product:
            return jsonify({"message": "Product not found"}), 404

        cart = Cart.query.filter_by(client_id=current_user.id).first()

        if not cart:
            # If the user doesn't have a cart yet, create a new cart
            cart = Cart(client_id=current_user.id)
            db.session.add(cart)
            db.session.commit()

        # Add the product to the cart or update the quantity if it already exists
        cart_product = cart_product.query.filter_by(cart_id=cart.id, product_id=product.id).first()
        if cart_product:
            cart_product.quantity += 1
        else:
            cart_product = cart_product(cart_id=cart.id, product_id=product.id, quantity=1)
            db.session.add(cart_product)

        db.session.commit()
 
        return jsonify({"message": f"{product.name} added to cart successfully"}), 200
    return jsonify({"message": "Unauthorized access"}), 401


@app.route('/removeFromCart/<product_id>', methods=['DELETE'])
@login_required
def removeFromCart(product_id):
    cart = Cart.query.filter_by(client_id=current_user.id).first()
    item = Product.query.filter_by(product_id=product_id).first
    item_cart = cart_product.query.filter_by(cart_id=cart.id, product_id=item.id)

    if item_cart:
        db.session.delete(item_cart)
        db.session.commit()

        return jsonify({"message": "Product deleted successfully"}), 200

@app.route('/viewcart')
@login_required
def viewCart():
    cart = Cart.query.filter_by(client_id=current_user.id).first()
    item_cart = cart_product.query.filter_by(cart_id=cart.id)
    product = cart_product.query.filter_by()
    
    output = []
    for i in item_cart:
        item_data = {}
        prod = cart_product.product_id
        item_data['product'] = prod.name
        item_data['quantity'] = item_cart.quantity
        item_data['price'] = prod.price
        item_data['Total'] = item_cart.quantity * item_cart.price
        output.append(item_data)
    
    sum = []
    for o in output:
        add = {}
        add['TOTAL'] += output.Total
    output.append(add)
    
    return jsonify({"Items": output, "TOTAL": add})

@app.route('/checkout')
@login_required
def checkOut():
    remove = 1


@app.route('/clearCart')
@login_required
def clearCart():
    remove = 1