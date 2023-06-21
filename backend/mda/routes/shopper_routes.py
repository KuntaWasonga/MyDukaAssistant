from flask import Blueprint, request, jsonify
from mda import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user

from mda.models import User

shopper_bp = Blueprint('user', __name__)


#This API registers a client to the database
@shopper_bp.route("/user/register", methods=["GET", "POST"])
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
@shopper_bp.route("/user/login", methods=['POST'])
def login():
    data = request.get_json()
    required_fields = ['username', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    
    empty_fields = [field for field in required_fields if not data.get(field)]
    if empty_fields:
        return jsonify({"error": f"Empty fields: {', '.join(empty_fields)}"}), 400

    user = User.query.filter_by(firstname=data['username']).first()
    if user:
        if check_password_hash(user.password, data["password"]):
            login_user(user)
            return jsonify({"message": "Login successful"}), 200

    return jsonify({'message': 'Invalid credentials'}), 401



#This API edits various properties of a client
@shopper_bp.route("/user/edit", methods=["PUT"])
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
@shopper_bp.route('/user/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message' : 'Logout successful'}), 200

#This API deletes a client from the database
@shopper_bp.route("/user/delete", methods =['DELETE'])
@login_required
def delete():
    mtu = User.query.get(current_user.id)
    if mtu:
        db.session.delete(mtu)
        db.session.commit()
        return jsonify({'message': f'{mtu.firstname} successfully deleted'}), 200
    return jsonify({'message': 'Not authorized'}), 409

