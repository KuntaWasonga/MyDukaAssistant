from flask import Blueprint, request, jsonify
from mda import db
from flask_login import current_user, login_required

from mda.models import User, Employee, Product, Cart, cart_product

cart_bp = Blueprint('cart', __name__)


#This adds additional items to a user's cart.
@cart_bp.route('/updateCart/<scan>', methods=["PUT"])
@login_required
def add_to_cart(scan):
    user = User.query.get(current_user.id)
    if user:
        product = Product.query.filter_by(barcode=scan).first()

        if product:
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
        return jsonify({"message": "Product not found"}), 404
    return jsonify({"message": "Unauthorized access"}), 401


@cart_bp.route('/removeFromCart/<product_id>', methods=['DELETE'])
@login_required
def removeFromCart(product_id):
    cart = Cart.query.filter_by(client_id=current_user.id).first()
    item = Product.query.filter_by(product_id=product_id).first
    item_cart = cart_product.query.filter_by(cart_id=cart.id, product_id=item.id)

    if item_cart:
        db.session.delete(item_cart)
        db.session.commit()

        return jsonify({"message": "Product deleted successfully"}), 200


@cart_bp.route('/viewcart')
@login_required
def viewCart():
    cart = Cart.query.filter_by(client_id=current_user.id).first()
    cart_items = db.session.query(cart_product, Product).join(Product).filter(cart_product.c.cart_id == cart.id).all()

    output = []
    total = 0

    for item, product in cart_items:
        item_data = {}

        item_data['product'] = product.name
        item_data['quantity'] = item.quantity
        item_data['price'] = product.price
        item_data['Total'] = item.quantity * product.price
        total += item_data['Total']

        output.append(item_data)

    output.append({'TOTAL': total})

    return jsonify({"Items": output, "TOTAL": total})



@cart_bp.route('/checkout')
@login_required
def checkOut():
    remove = 1

@cart_bp.route('/clearCart')
@login_required
def clearCart():
    remove = 1