from bidboard import db


class Billboard(db.Model):

    __tablename__ = 'billboards'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    size = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text)
    successful_bookings = db.Column(db.ARRAY(db.Integer), nullable=True)
    bids = db.relationship("Bid", backref="billboards", lazy=False,
                             order_by="desc(Bid.id)", cascade="delete, delete-orphan")

    def __init__(self, owner, location, size, description=None):
        self.owner = owner
        self.location = location
        self.size = size
        self.description = description
        self.successful_bookings = []

    def __repr__(self):
        return f"Billboard at {self.location} with size {self.size} owned by {self.owner}"

    def get_successful_bookings(self):
        bids = self.bids
        successful_bookings = []
        for bid in bids:
            if bid.is_confirmed:
                successful_bookings.append(bid.id)
        self.successful_bookings = successful_bookings
        return successful_bookings
