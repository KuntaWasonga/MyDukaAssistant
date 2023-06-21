from flask import Blueprint, request, jsonify
from mda import db
from flask_login import current_user, login_required

from mda.models import User, Employee, Product

product_bp = Blueprint('product', __name__)


#This API adds a new product to the database
@product_bp.route('/product/add', methods=['POST'])
@login_required
def new_product():
    # Check if the user is an employee
    user = Employee.query.get(current_user.id)
    if not user:
        return jsonify({'message': 'Unauthorized access'}), 401

    data = request.get_json()

    # Validate required fields in the data
    required_fields = ['id', 'barcode', 'name', 'price']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400
    
    empty_fields = [field for field in required_fields if not data.get(field)]
    if empty_fields:
        return jsonify({"message": f"Empty fields: {', '.join(empty_fields)}"}), 400

    # Check if the product already exists
    product_exists = Product.query.filter_by(barcode=data['barcode']).first()
    if product_exists:
        return jsonify({'message': 'Product already exists'}), 409

    new_product = Product(
        id=data['id'],
        barcode=data['barcode'],
        name=data['name'],
        price=data['price']
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': f'{new_product.name} added'}), 200


@product_bp.route('/product/scan/<scan>')
@login_required
def read_product(scan):
    item = Product.query.filter_by(barcode=scan).first()

    if item:
        output = []
        item_data = {}
        item_data['id'] = item.id
        item_data['barcode'] = item.barcode
        item_data['name'] = item.name
        item_data['price'] = item.price
        output.append(item_data)

        return jsonify({'item': output}), 200

    return jsonify({'message': 'This item does not exist'}), 409



#This API updates properties of a product
@product_bp.route('/product/update/<product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    #checks for User access (meant to be employees only)
    user_authorized = Employee.query.filter_by(email=current_user.email).first()
    if user_authorized:
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
    return jsonify({'message' : 'Unauthorized access'}), 401


#This API deletes a product
@product_bp.route('/product/delete/<product_id>', methods=['DELETE'])
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
