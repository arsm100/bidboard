from bidboard import db, S3_LOCATION


class Medium(db.Model):

    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    medium_name = db.Column(db.Text, nullable=False)
    medium_url = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, medium_name, medium_url=None):
        self.user_id = user_id
        self.medium_name = medium_name
        self.medium_url = f'{S3_LOCATION}{self.medium_name}'
