from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
  
db = SQLAlchemy()
  
def get_uuid():
    return uuid4().hex

#This class defines the client of the supermarket
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(2), primary_key=True, unique=True, default=get_uuid)
    firstname = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    lastname = db.Column(db.String(20), primary_key=True, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    about = db.Column(db.Text)
    cart = db.relationship("Cart", backref="client", lazy=True)
    
    def __repr__(self):
        return f"User('{self.firstname}', '{self.email}')"

#This class defines the employee of the supermarket
class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer(2), primary_key=True, unique=True)
    employee_id = db.Column(db.Integer(5), unique = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean)

#This class defines a client and their items to be put on a cart
class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer(2), primary_key=True, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    product = db.relationship("Product", backref="cart", uselist=False, lazy=True) #OneToOne relationship
    quantity = db.Column(db.Integer(2), nullable = False)
    Total = db.Column(db.Integer(5), nullable = False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#This holds the products added to the database
class Product(db.model):
    __tablename__ = "products"
    id = db.Column(db.Integer(2), primary_key=True, unique=True)
    barcode = db.Column(db.Integer(12), primary_key=True, unique=True, nullable = False)
    name = db.Column(db.String(12), unique = True, nullable=False)
    price = db.Column(db.Integer(5), nullable = False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"
