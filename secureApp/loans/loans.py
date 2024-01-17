from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SubmitField
from wtforms.validators import InputRequired, Length, Email
from flask import session
from ..models import db, User, Loan
from decimal import Decimal
from secureApp.utils.utils import custom_amount_validator, login_required 


loans_bp = Blueprint('loans_bp', __name__)

class LoanForm(FlaskForm):
    borrower_email = StringField('Borrower Email', validators=[InputRequired(), Length(min=4, max=40), Email()])
    amount = DecimalField('Amount', validators=[InputRequired(),Length(min=1), custom_amount_validator])
    due_date = DateField('Due Date', validators=[InputRequired()], format='%Y-%m-%d')
    submit = SubmitField('Create Loan')

@loans_bp.route('/accept_loan/<int:loan_id>', methods=['POST'])
@login_required
def accept_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    borrower = User.query.get(loan.borrower_id)
    lender = User.query.get(loan.lender_id)

    if loan.borrower_id != session.get('user_id'):
        flash('Unauthorized action.', 'error')
        return redirect(url_for('general_bp.dashboard'))   

    lender.balance += Decimal(loan.amount)
    borrower.balance -= Decimal(loan.amount)
    loan.is_accepted = True
    db.session.commit()
    flash('Loan offer accepted.', 'success')
    return redirect(url_for('general_bp.dashboard'))
 
@loans_bp.route('/repay/<int:loan_id>', methods=['POST'])
@login_required
def repay_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    borrower = User.query.get(loan.borrower_id)
    lender = User.query.get(loan.lender_id)

    if loan.borrower_id != session.get('user_id'):
        flash('Unauthorized action.', 'error')
        return redirect(url_for('general_bp.dashboard'))   

    lender.balance -= Decimal(loan.amount)
    borrower.balance += Decimal(loan.amount)
    loan.is_repaid = True
    db.session.commit()
    flash('Loan repaid.', 'success')
    return redirect(url_for('general_bp.dashboard'))
 


@loans_bp.route('/add_loan', methods=['GET', 'POST'])
@login_required
def add_loan():
    form = LoanForm()
    if form.validate_on_submit():
        borrower = User.query.filter_by(email=form.borrower_email.data).first()
        if not borrower:
            flash('Borrower email not found.', 'error')
            return render_template('add_loan.html', form=form)

        lender_id = session.get('user_id')
        new_loan = Loan(
            amount=form.amount.data,
            lender_id=lender_id,
            borrower_id=borrower.id,
            due_date=form.due_date.data
        )
        db.session.add(new_loan)
        db.session.commit()
        flash('Loan successfully created.', 'success')        
        return redirect(url_for('general_bp.dashboard'))

    return render_template('add_loan.html', form=form)

