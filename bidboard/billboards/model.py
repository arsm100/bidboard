from bidboard import db


class Billboard(db.Model):

    __tablename__ = 'billboards'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    size = db.Column(db.String(), nullable=False)
    base_price = db.Column(db.Numeric(), nullable=False)
    description = db.Column(db.Text)
    bid_times = db.Column(db.ARRAY(db.Numeric()), nullable=True)
    bids = db.relationship("Bid", backref="billboards", lazy=False,
                             order_by="desc(Bid.id)", cascade="delete, delete-orphan")

    def __init__(self, owner, location, size, base_price, description=None):
        self.owner = owner
        self.location = location
        self.size = size
        self.base_price = base_price
        self.description = description
        self.successful_bookings = []

    def __repr__(self):
        return f"Billboard at {self.location} with size {self.size} owned by {self.owner}"

    def get_bid_times(self):
        bid_times = []
        for bid in self.bids:
            bid_times.append(bid.booking_at)
        self.bid_times = bid_times
        return self.bid_times

    def get_bids(self):
        jsonfiable_bids = []
        for bid in self.bids:
            del bid.__dict__['_sa_instance_state']
            jsonfiable_bids.append(bid.__dict__)
        return jsonfiable_bids
