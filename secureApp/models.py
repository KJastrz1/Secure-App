from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from decimal import Decimal

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    emailConfirmed = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(80), nullable=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime, nullable=True)
    balance = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=Decimal('0.00'))
    
    
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=Decimal('0.00'))
    lender_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    borrower_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    is_accepted = db.Column(db.Boolean, nullable=True)
    is_repaid = db.Column(db.Boolean, nullable=True)
    
    lender = relationship("User", foreign_keys=[lender_id])
    borrower = relationship("User", foreign_keys=[borrower_id])
 
   
class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(15))  
    success = db.Column(db.Boolean, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    country = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    
    user = relationship("User", backref="login_attempts")
 
