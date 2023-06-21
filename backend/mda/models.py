from datetime import datetime
from mda import db, login_manager
from uuid import uuid4
from mda import db
from flask_login import UserMixin  

def get_uuid():
    return uuid4().hex

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user

    employee = Employee.query.get(user_id)
    if employee:
        return employee

    return None


#This class defines the client of the supermarket
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, default=get_uuid)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    about = db.Column(db.Text)
    cart = db.relationship("Cart", backref="client", lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.email}')"


#This class defines the employee of the supermarket
class Employee(db.Model, UserMixin):
    __tablename__ = "employees"
    id = db.Column(db.String(2), primary_key=True, unique=True)
    employee_id = db.Column(db.Integer, unique = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean, default=False)


#This class defines a client and their items to be put on a cart
class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, unique=True, default=get_uuid)
    client_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    product = db.relationship("Product", secondary="cart_product", backref="carts", uselist=False, lazy=True) #OneToOne relationship
    quantity = db.Column(db.Integer)
    Total = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


#This holds the products added to the database
class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    barcode = db.Column(db.Integer, primary_key=True, unique=True, nullable = False)
    name = db.Column(db.String(50), unique = True, nullable=False)
    price = db.Column(db.Integer, nullable = False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"


# Intermediate table for the many-to-many relationship between Cart and Product
cart_product = db.Table(
    "cart_product",
    db.Column("cart_id", db.Integer, db.ForeignKey("cart.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column("quantity", db.Integer, nullable=False),
    db.Column("total", db.Integer)
)
