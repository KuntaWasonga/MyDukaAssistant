import uuid
from flask import Blueprint, request, jsonify
from mda import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user

from mda.models import User, Employee


employee_bp = Blueprint('employee', __name__)


def get_uuid_from_integer(integer_value):
    # Convert the integer to a bytes representation
    bytes_value = integer_value.to_bytes((integer_value.bit_length() + 7) // 8, 'big')

    # Generate a UUID from the bytes value
    uuid_value = uuid.UUID(bytes=bytes_value)

    return uuid_value


#This API registers an Employee to the database
@employee_bp.route("/employee/register", methods=["GET", "POST"])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    #Check for missing fields
    required_fields = ['employee_id', 'email', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    #Check if the employee already exists
    user = Employee.query.filter_by(employee_id=data['employee_id']).first()
    if user:
        return jsonify({"error": "Employee already exists"}), 409

    #Ensures employee credentials are well protected
    hashed_password = generate_password_hash(data['password'])
    #id_uuid = get_uuid_from_integer(data['employee_id'])

    new_employee = Employee(
        id = data['id'],
        employee_id = data['employee_id'],
        email = data['email'],
        password = hashed_password,
        admin = data['admin'])

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"messsage": "Registration successful"})


#This API is responsible for Employee login
@employee_bp.route("/employee/login", methods=['POST'])
def login():
    data = request.get_json()
    required_fields = ['employee_id', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    user = Employee.query.filter_by(employee_id=data["employee_id"]).first()
    if user:
        if check_password_hash(user.password, data["password"]):
            login_user(user)
            return jsonify({"message": "Login successful"}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

#This API logs out a User
@employee_bp.route('/employee/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message' : 'Logout successful'}), 200


#---------------------------------ADMIN ROUTES------#
#This API lets the admin check all the users in the users database
@employee_bp.route('/employee/users')
@login_required
def users():
    adm = Employee.query.get(current_user.id)
    if adm.admin:
        users = User.query.all()

        output = []
        for u in users:
            item_data = {}
            item_data['firstname'] = User.firstname
            item_data['lastname'] = User.lastname
            item_data['email'] = User.email
            #item_data['password'] = User.password

            output.append(item_data)
            
        return jsonify({"users" : output})
    return jsonify({"message": "unauthorized access"})


#This API lets only an admin delete an employee from the database
@employee_bp.route("/employee/delete/<id>", methods =['DELETE'])
@login_required
def delete(id):
    mtu = Employee.query.get(current_user.id)
    if mtu.admin:
        e_id = get_uuid_from_integer(id)
        user = Employee.query.filter_by(employee_id=e_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()

            return jsonify({'message': f'{user.employee_id} terminated'}), 200
        return jsonify({'message': "Employee not found"})
    return jsonify({'message': 'Not authorized'}), 409
