import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (create_access_token,get_jwt,get_jwt_identity,
                                unset_jwt_cookies, jwt_required, JWTManager )
#from flask_cors import CORS

from models import *

# create the app
api = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
api.config['SECRET_KEY'] = 'KUNTA'
api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mda.db"

db = SQLAlchemy(api)

api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(api)

bcrypt = Bcrypt(api)

# initialize the app with the extension
db.init_app(api)

#create all the tables
with api.app_context():
    db.create_all()


#This API registers a client to the database
@api.route("/register", methods=('POST'))
def signup():
    data = request.json()

    #Check if the user exists
    user_exists = User.query.filter_by(email=data['email']) is not None
    if user_exists:
        return jsonify({"error": "Email already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(data['password'])

    client = User(
        firstname = data['firstname'],
        lastname = data['lastname'],
        email = data['email'],
        password = hashed_password)
    db.session.add(client)
    db.session.commit()

    return ({
        "id": client.id,
        "email": client.email
    })


#This API is responsible for user login
@api.route("/login", methods=['POST'])
def create_token():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "Wrong email"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    
    return jsonify({
        "email": email,
        "access_token": access_token
    })
    return response


@api.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

#This API edits various properties of a client
@api.route("/<str:person>/edit", methods=('GET', 'PUT'))
@jwt_required
def edit(person):
    person = User.query.get_or_404(person)

    if request.method == "PUT":
        person = User(
            firstname = request.form['firstname'],
            lastname = request.form['lastname'],
            email = request.form['email'],
            bio = request.form['bio']
        )

        db.session.add(person)
        db.session.commit()

    return jsonify({'message': f'{person.firstname} successfully updated!'})

#This API logs out a user
@api.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message' : 'logout successful'})
    unset_jwt_cookies(response)
    return response, 200

#This API deletes a client from the database
@api.route("/<str:user>/delete")
@jwt_required
def delete(user):
    mtu = User.query.get_or_404(user)
    
    db.session.delete(mtu)
    db.session.commit()
    
    return jsonify({'message': f'User successfully deleted'})
    
#------------------------------------------------------------------#
          
#PRODUCT APIS
#This API adds a new product to the database
@api.route('/AddProduct/<product_barcode>', methods=['POST'])
@jwt_required
def add_product(product_barcode):
    #checks for user access (meant to be employees only)
    user = get_jwt_identity()
    user_authorized = Employee.query.filter_by(email=user).first()
    if not user_authorized:
        return jsonify({'message' : 'Unauthorized access'})

    #checks if product exists
    product_exists = Product.query.filter_by(barcode=product_barcode).first()
    if product_exists:
        return jsonify({'message' : 'Product already exists'})

    data = request.get_json()

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
@api.route('/scanItem/<barcode>')
@jwt_required
def readProduct(barcode):
    item = Product.query.filter_by(barcode=barcode).first()
    
    if not item:
        return jsonify({'message':'This item does not exist'})

    return jsonify({
        "id": item.id,
        "barcode": item.barcode,
        "name": item.name,
        "price": item.price,
    })


#This API updates properties of a product
@api.route('/UpdateProduct/<product_id>', methods=['POST'])
@jwt_required
def update_product(product_id):
    user = get_jwt_identity()
    #checks for user access (meant to be employees only)
    user_authorized = Employee.query.filter_by(email=user).first()
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
@api.route('/product/<product_id>', methods=['DELETE'])
@jwt_required
def delete_product(user, product_id):
    user = get_jwt_identity()
    #checks for user access (meant to be employees only)
    user_authorized = Employee.query.filter_by(email=user).first()
    if not user_authorized:
        return jsonify({'message' : 'Unauthorized access'})

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'product does not exist'})

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message' : 'Product deleted'})
