'''
import uuid
from flask import Flask, request, jsonify
from mda import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
#from flask_cors import CORS

from mda.models import User, Employee, Product, Cart, cart_product

def get_uuid_from_integer(integer_value):
    # Convert the integer to a bytes representation
    bytes_value = integer_value.to_bytes((integer_value.bit_length() + 7) // 8, 'big')

    # Generate a UUID from the bytes value
    uuid_value = uuid.UUID(bytes=bytes_value)

    return uuid_value
#------------------------------------------------------------------#
#----------------------PRODUCT APIS--------------------------------#
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
    # product = cart_product.query.filter_by()
    
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
'''