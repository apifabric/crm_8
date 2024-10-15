# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 15, 2024 15:37:54
# Database: sqlite:////tmp/tmp.O6fVt7rb9G/crm_8/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Customer(SAFRSBaseX, Base):
    """
    description: Represents customers in the CRM system.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(50))
    address = Column(Text)
    membership_since = Column(DateTime, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    AccountList : Mapped[List["Account"]] = relationship(back_populates="customer")
    ContactList : Mapped[List["Contact"]] = relationship(back_populates="customer")
    CustomerInteractionList : Mapped[List["CustomerInteraction"]] = relationship(back_populates="customer")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")
    SubscriptionList : Mapped[List["Subscription"]] = relationship(back_populates="customer")



class Employee(SAFRSBaseX, Base):
    """
    description: Represents employees who manage customer interactions.
    """
    __tablename__ = 'employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    CustomerInteractionList : Mapped[List["CustomerInteraction"]] = relationship(back_populates="employee")



class Product(SAFRSBaseX, Base):
    """
    description: Represents products available for purchase.
    """
    __tablename__ = 'products'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductVendorList : Mapped[List["ProductVendor"]] = relationship(back_populates="product")
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="product")



class Vendor(SAFRSBaseX, Base):
    """
    description: Represents suppliers or vendors providing products.
    """
    __tablename__ = 'vendors'
    _s_collection_name = 'Vendor'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_name = Column(String(100))
    contact_email = Column(String(100))

    # parent relationships (access parent)

    # child relationships (access children)
    ProductVendorList : Mapped[List["ProductVendor"]] = relationship(back_populates="vendor")



class Account(SAFRSBaseX, Base):
    """
    description: Represents financial accounts associated with customers.
    """
    __tablename__ = 'accounts'
    _s_collection_name = 'Account'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    balance = Column(Float, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("AccountList"))

    # child relationships (access children)



class Contact(SAFRSBaseX, Base):
    """
    description: Represents contacts associated with customers.
    """
    __tablename__ = 'contacts'
    _s_collection_name = 'Contact'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    contact_type = Column(String(50), nullable=False)
    value = Column(String(100), nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("ContactList"))

    # child relationships (access children)



class CustomerInteraction(SAFRSBaseX, Base):
    """
    description: Represents interactions between employees and customers.
    """
    __tablename__ = 'customer_interactions'
    _s_collection_name = 'CustomerInteraction'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    employee_id = Column(ForeignKey('employees.id'), nullable=False)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    interaction_date = Column(DateTime)
    notes = Column(Text)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("CustomerInteractionList"))
    employee : Mapped["Employee"] = relationship(back_populates=("CustomerInteractionList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Represents orders made by customers.
    """
    __tablename__ = 'orders'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime)
    total_amount = Column(Float, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="order")
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="order")



class ProductVendor(SAFRSBaseX, Base):
    """
    description: Represents the association between products and vendors.
    """
    __tablename__ = 'product_vendors'
    _s_collection_name = 'ProductVendor'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    vendor_id = Column(ForeignKey('vendors.id'), nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("ProductVendorList"))
    vendor : Mapped["Vendor"] = relationship(back_populates=("ProductVendorList"))

    # child relationships (access children)



class Subscription(SAFRSBaseX, Base):
    """
    description: Represents subscription plans customers can enroll in.
    """
    __tablename__ = 'subscriptions'
    _s_collection_name = 'Subscription'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    plan_name = Column(String(100), nullable=False)
    monthly_fee = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("SubscriptionList"))

    # child relationships (access children)



class OrderDetail(SAFRSBaseX, Base):
    """
    description: Represents the details of each product within an order.
    """
    __tablename__ = 'order_details'
    _s_collection_name = 'OrderDetail'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderDetailList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderDetailList"))

    # child relationships (access children)



class Payment(SAFRSBaseX, Base):
    """
    description: Represents customer payments for orders.
    """
    __tablename__ = 'payments'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)
