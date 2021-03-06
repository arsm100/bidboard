from flask import Blueprint, render_template, request, redirect, url_for, flash
from bidboard.users.forms import SignupForm
from bidboard.users.model import User, db
from flask_login import login_user, logout_user, login_required, login_url, current_user
from bidboard.helpers.sendgrid import send_signup_email

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route("/new", methods=['GET'])
def new():
    if current_user.is_authenticated:
        flash('You are already logged in!!')
        return redirect(url_for('home'))  # change redirect destination later
    else:
        form = SignupForm()
        return render_template('users/new.html', form=form)


@users_blueprint.route("/create", methods=['POST'])
def create():
    form = SignupForm(request.form)

    new_user = User(
        company_name=form.company_name.data,
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        email=form.email.data.lower(),
        password=form.password.data
    )

    if len(new_user.validation_errors) > 0:
        return render_template('users/new.html', validation_errors=new_user.validation_errors, form=form)
    else:
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        send_signup_email(new_user.email, new_user.id)
        flash('User Account created successfully')
        # change redirect destination later
        return redirect(url_for('home', id=current_user.id))


@users_blueprint.route("<id>/dashboard", methods=['GET'])
@login_required
def dashboard(id):
    return render_template("users/dashboard.html")
