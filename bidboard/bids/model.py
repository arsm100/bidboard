from bidboard import db
import datetime
import time


class Bid(db.Model):

    __tablename__ = 'bids'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    billboard_id = db.Column(db.Integer, db.ForeignKey('billboards.id'), nullable=False)
    medium_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    booking_at = db.Column(db.TIMESTAMP, nullable=False)
    amount = db.Column(db.Numeric(), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='MYR')
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, user_id, billboard_id, medium_id, booking_at, amount):
        self.user_id = user_id
        self.billboard_id = billboard_id
        self.medium_id = medium_id
        self.created_at = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        self.booking_at = booking_at
        self.amount = amount

    def __repr__(self):
        return f"Bid of {self.amount} has been made for {self.billboard_id} by {self.user_id} for {self.booking_at}"
