from flask import Blueprint, Flask, current_app as app, render_template, url_for, redirect, request, flash, session
from flask_wtf import FlaskForm
from wtforms import  PasswordField, SubmitField  
from wtforms.validators import InputRequired, Length,  EqualTo
from sqlalchemy.orm import session
import os
from flask import session, redirect, url_for
from ..models import db, User, Loan, LoginAttempt
from flask import render_template, request, flash, redirect, url_for

from secureApp.utils.utils import custom_password_validator, hash_password, login_required



general_bp = Blueprint('general_bp', __name__)

@general_bp.route('/')
def home():
    return render_template('home.html')

@general_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if user:        
        pending_loans = db.session.query(Loan, User.email).join(User, User.id == Loan.lender_id).filter(Loan.borrower_id == user_id, Loan.is_accepted.is_(None), Loan.is_repaid.is_(None)).all()
      
        taken_loans = db.session.query(Loan, User.email).join(User, User.id == Loan.lender_id).filter(Loan.borrower_id == user_id).all()
        
        given_loans = db.session.query(Loan, User.email).join(User, User.id == Loan.borrower_id).filter(Loan.lender_id == user_id).all()
        

        taken_loan_history = db.session.query(Loan, User.email).join(User, User.id == Loan.lender_id).filter(Loan.borrower_id == user_id, Loan.is_accepted == True, Loan.is_repaid == True).all()        

        given_loan_history = db.session.query(Loan, User.email).join(User, User.id == Loan.borrower_id).filter(Loan.lender_id == user_id, Loan.is_accepted == True, Loan.is_repaid == True).all()
        
        return render_template(
            'dashboard.html',
            user=user, 
            pending_loans=pending_loans,
            taken_loans=taken_loans,
            given_loans=given_loans,
            taken_loan_history=taken_loan_history,
            given_loan_history=given_loan_history
        )
    else:
        flash("User not found", 'error')
        return redirect(url_for('general_bp.home'))



class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired(), Length(min=8, max=80)])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=80), custom_password_validator])
    confirm = PasswordField('Confirm New Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Change Password')

@general_bp.route('/usersettings', methods=['GET', 'POST'])
@login_required
def settings():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():
        old_password = change_password_form.old_password.data
        new_password = change_password_form.new_password.data

        stored_salt, stored_hash = user.password.split(':')
        hashed_old_password = hash_password(old_password, stored_salt)
            
        if hashed_old_password == stored_hash:               
            salt = os.urandom(16).hex()
            hashed_new_password=hash_password(new_password, salt)
            user.password = salt + ':' + hashed_new_password
            db.session.commit()
            flash('Password updated successfully', 'success')
        else:
            flash('Old password is incorrect', 'error')
        

    login_attempts = LoginAttempt.query.filter_by(user_id=user_id).order_by(LoginAttempt.timestamp.desc()).all()

    return render_template('usersettings.html', form=change_password_form, login_attempts=login_attempts)
