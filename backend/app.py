import json
import jwt
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_jwt_extended import (create_access_token,get_jwt,get_jwt_identity,
                                unset_jwt_cookies, jwt_required, JWTManager )
#from flask_cors import CORS

from models import *

# create the app
api = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
api.config['SECRET_KEY'] = 'lhya67'
api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mda.db"
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# initialize the app with the extension
db.init_app(api)

#create all the tables
with api.app_context():
    db.create_all()

#-------------------------------------------------------------------------------------#
#Authentication
def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None

       if 'x-access-token' in request.headers:
           token = request.headers['x-access-token']

       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, api.config['SECRET_KEY'])
           current_user = User.query.filter_by(id=data['user_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})

       return f(current_user, *args, **kwargs)
   return decorator


#-------------------------------------------------------------------------------------#
#This API registers a client to the database
@api.route("/register", methods=["POST"])
def signup():
    data = request.get_json()

    #Check if the user exists
    user_exists = User.query.filter_by(email=data['email']).first()
    if user_exists:
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


#This API is responsible for user login
@api.route("/login")
def create_token():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Could not verify"}), 401

    user = User.query.filter_by(firstname=auth.username).first()

    if not user:
        return jsonify({"message": "User does not exist"}), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes = 45)}, api.config['SECRET_KEY'])

        return jsonify({'token' : token})

    return jsonify({'message': 'Could not verify'}), 401

@api.route('/users')
def users():
    
    item = User.query.all()

    output = []
    for i in item:
        item_data = {}
        item_data['firstname'] = item.firstname
        item_data['lastname'] = item.lastname
        item_data['email'] = item.email
        item_data['password'] = item.password
        output.append(item_data)
        
    return jsonify({
        "users" : output
    })
    

#This API edits various properties of a client
@api.route("/user/edit", methods=["GET", "POST"])
@token_required
def edit(current_user):
    person = User.query.filter_by(email=current_user.email).first()

    if request.method == "POST":
        person.firstname = request.json.get('firstname', person.firstname)
        person.lastname = request.json.get('lastname', person.lastname)
        person.email = request.json.get('email', person.email)
        person.bio = request.json.get('bio', person.bio)
        
        db.session.commit()

    return jsonify({'message': 'Person successfully updated!'})


#This API logs out a user
@api.route('/user/logout', methods=['POST'])
def logout():
    response = jsonify({'message' : 'logout successful'})
    unset_jwt_cookies(response)
    return response, 200

#This API deletes a client from the database
@api.route("/user/delete")
@token_required
def delete(current_user):
    mtu = User.query.filter_by(email=current_user.email).first()

    db.session.delete(mtu)
    db.session.commit()

    return jsonify({'message': 'User successfully deleted'})

#------------------------------------------------------------------#
     
#PRODUCT APIS
#This API adds a new product to the database
@api.route('/product/add', methods=['POST'])
@token_required
def new_product(current_user):
    #checks for user access (meant to be employees only)
#    user = get_jwt_identity()
    user_authorized = Employee.query.filter_by(email=current_user.email).first()
    if not user_authorized:
        return jsonify({'message' : 'Unauthorized access'})

    data = request.get_json()

    #checks if product exists
    product_exists = Product.query.filter_by(barcode=data['barcode']).first()
    if product_exists:
        return jsonify({'message' : 'Product already exists'})

    new_product = Product(
        id = data['id'],
        barcode = data['barcode'], 
        name = data['name'], 
        price = data['price'],
    )

    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({'message' : f'{new_product.name} added'})


#This API reads properties of a product
@api.route('/product/scan/<scan>')
@token_required
def read_product(current_user, scan):
    item = Product.query.filter_by(barcode=scan).first()

    if not item:
        return jsonify({'message':'This item does not exist'})

    output = []
    for i in item:
        item_data = {}
        item_data['id'] = item.id
        item_data['barcode'] = item.barcode
        item_data['name'] = item.name
        item_data['price'] = item.price
        output.append(item_data)

    return jsonify({'item': output})


#This API updates properties of a product
@api.route('/product/update/<product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    #checks for user access (meant to be employees only)
    user_authorized = Employee.query.filter_by(email=current_user.email).first()
    if not user_authorized:
        return jsonify({'message' : 'Unauthorized access'})

    #checks if product exists
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message' : 'Product does not exist'})

    update_product = Product(
        id = product['id'],
        barcode = product['barcode'], 
        name = product['name'], 
        price = product['price'],
    )

    db.session.add(update_product)
    db.session.commit()

    return jsonify({'message' : f'{update_product.name} updated'})


#This API deletes a product
@api.route('/product/delete/<product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    #checks for user access (meant to be employees only)
    user_authorized = Employee.query.filter_by(email=current_user.email).first()
    if not user_authorized or user_authorized.admin:
        return jsonify({'message' : 'Unauthorized access'})

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'product does not exist'})

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message' : 'Product deleted'})


if  __name__ == '__main__': 
    api.run(debug=True)
