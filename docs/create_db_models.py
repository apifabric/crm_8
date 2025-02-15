# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Define the base class for ORM models
Base = declarative_base()

# Define the CRM data model with descriptions


class Customer(Base):
    """description: Represents customers in the CRM system."""
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    membership_since = Column(DateTime, nullable=False, default=datetime.datetime.now)


class Account(Base):
    """description: Represents financial accounts associated with customers."""
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    balance = Column(Float, nullable=False)


class Contact(Base):
    """description: Represents contacts associated with customers."""
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    contact_type = Column(String(50), nullable=False)  # e.g., phone, email
    value = Column(String(100), nullable=False)


class Order(Base):
    """description: Represents orders made by customers."""
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.now)
    total_amount = Column(Float, nullable=False, default=0.0)


class Product(Base):
    """description: Represents products available for purchase."""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)


class OrderDetail(Base):
    """description: Represents the details of each product within an order."""
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)


class Employee(Base):
    """description: Represents employees who manage customer interactions."""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)


class CustomerInteraction(Base):
    """description: Represents interactions between employees and customers."""
    __tablename__ = 'customer_interactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    interaction_date = Column(DateTime, default=datetime.datetime.now)
    notes = Column(Text, nullable=True)


class Payment(Base):
    """description: Represents customer payments for orders."""
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.now)


class Subscription(Base):
    """description: Represents subscription plans customers can enroll in."""
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    plan_name = Column(String(100), nullable=False)
    monthly_fee = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)


class Vendor(Base):
    """description: Represents suppliers or vendors providing products."""
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact_name = Column(String(100), nullable=True)
    contact_email = Column(String(100), nullable=True)


class ProductVendor(Base):
    """description: Represents the association between products and vendors."""
    __tablename__ = 'product_vendors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)


# Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample data
# Adding Customers
session.add_all([
    Customer(name="John Doe", email="johndoe@example.com", phone="123-456-7890", address="123 Elm St"),
    Customer(name="Jane Smith", email="janesmith@example.com", phone="987-654-3210", address="456 Oak St")
])

# Adding Accounts
session.add_all([
    Account(customer_id=1, balance=2500.0),
    Account(customer_id=2, balance=1500.0)
])

# Adding Contacts
session.add_all([
    Contact(customer_id=1, contact_type="email", value="johndoe@example.com"),
    Contact(customer_id=2, contact_type="phone", value="987-654-3210")
])

# Adding Products
session.add_all([
    Product(name="Laptop", price=1200.0, stock_quantity=30),
    Product(name="Smartphone", price=800.0, stock_quantity=50)
])

# Adding Orders
session.add_all([
    Order(customer_id=1, total_amount=2000.0),
    Order(customer_id=2, total_amount=1600.0)
])

# Adding Order Details
session.add_all([
    OrderDetail(order_id=1, product_id=1, quantity=1, price_per_unit=1200.0),
    OrderDetail(order_id=1, product_id=2, quantity=1, price_per_unit=800.0),
    OrderDetail(order_id=2, product_id=2, quantity=2, price_per_unit=800.0)
])

# Adding Employees
session.add_all([
    Employee(name="Alice Johnson", role="Sales Representative"),
    Employee(name="Bob Williams", role="Customer Service")
])

# Adding Customer Interactions
session.add_all([
    CustomerInteraction(employee_id=1, customer_id=1, notes="Discussed product options."),
    CustomerInteraction(employee_id=2, customer_id=2, notes="Assisted with order tracking.")
])

# Adding Payments
session.add_all([
    Payment(order_id=1, amount=2000.0),
    Payment(order_id=2, amount=1600.0)
])

# Adding Subscriptions
session.add_all([
    Subscription(customer_id=1, plan_name="Premium", monthly_fee=50.0, start_date=datetime.datetime.now()),
    Subscription(customer_id=2, plan_name="Basic", monthly_fee=20.0, start_date=datetime.datetime.now())
])

# Adding Vendors
session.add_all([
    Vendor(name="Tech Supplier", contact_name="Tom Vendor", contact_email="tom@techsupplier.com"),
    Vendor(name="Gadget Warehouse", contact_name="Gina Vendor", contact_email="gina@gadgetwarehouse.com")
])

# Adding Product Vendors
session.add_all([
    ProductVendor(product_id=1, vendor_id=1),
    ProductVendor(product_id=2, vendor_id=2)
])

# Commit the session
session.commit()

# Close the session
session.close()
