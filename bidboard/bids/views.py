from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bidboard import generate_client_token, gateway, db, Bid, Medium, Billboard
from bidboard.helpers.sendgrid import send_bid_email
import datetime


bids_blueprint = Blueprint(
    'bids', __name__, template_folder='templates')


@bids_blueprint.route("/<medium_id>/new", methods=["GET"])
@login_required
def create(medium_id):
    client_token = generate_client_token()
    return render_template('bids/new.html', medium_id=medium_id, client_token=client_token)


@bids_blueprint.route("<medium_id>/<billboard_id>/checkout", methods=["POST"])
def checkout(medium_id, billboard_id):
    amount = request.form["amount"]
    nonce_from_the_client = request.form["payment_method_nonce"]
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        new_bid = Bid(
            user_id=current_user.id,
            billboard_id=billboard_id,
            medium_id=medium_id,
            booking_at=datetime.datetime.timestamp(datetime.datetime.now()),
            amount=amount
        )
        db.session.add(new_bid)
        db.session.commit()
        send_bid_email(current_user.email, new_bid.id)
        flash('Bid placed successfully.')
        return redirect(url_for('home'))
    else:
        flash(result.transaction.status)
        flash(f'{result.transaction.processor_response_code} : {result.transaction.processor_response_text}')
        return redirect(url_for('home'))


@bids_blueprint.route("/", methods=["GET"])
@login_required
def index():
    bids = Bid.query.all()
    return render_template('bids/index.html', Medium=Medium, bids=bids)
