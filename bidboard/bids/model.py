from bidboard import db
from sqlalchemy.ext.hybrid import hybrid_property
import datetime


class Bid(db.Model):

    __tablename__ = 'bids'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #can be ondelete="SET NULL"
    billboard_id = db.Column(db.Integer, db.ForeignKey('billboards.id'), nullable=False)
    medium_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
    created_at = db.Column(db.Numeric(), nullable=False)
    booking_at = db.Column(db.Numeric(), nullable=False)
    amount = db.Column(db.Numeric(), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='MYR')
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, user_id, billboard_id, medium_id, booking_at, amount):
        self.user_id = user_id
        self.billboard_id = billboard_id
        self.medium_id = medium_id
        self.created_at = datetime.datetime.timestamp(datetime.datetime.now())
        self.booking_at = booking_at
        self.amount = amount

    def __repr__(self):
        return f"Bid of {self.amount} MYR has been made for Billboard {self.billboard_id} by user {self.user_id} at {self.booking_at_readable}"

    @hybrid_property
    def created_at_readable(self):
        return datetime.datetime.fromtimestamp(self.created_at).strftime("%Y-%m-%d  %I:%M %p")

    @hybrid_property
    def booking_at_readable(self):
        return datetime.datetime.fromtimestamp(self.booking_at).strftime("%Y-%m-%d  %I%p")
