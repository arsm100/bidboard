from bidboard import db, S3_LOCATION


class Medium(db.Model):

    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    medium_name = db.Column(db.Text, nullable=False)
    medium_url = db.Column(db.Text, nullable=False)
    campaign_name = db.Column(db.Text, nullable=False, server_default="")
    description = db.Column(db.Text, nullable=False, server_default="")
    is_approved = db.Column(db.Boolean, nullable=False, server_default="False")
    concepts = db.Column(db.JSON, nullable=True)


    def __init__(self, user_id, medium_name, campaign_name, description):
        self.user_id = user_id
        self.medium_name = medium_name
        self.medium_url = f'{S3_LOCATION}{self.medium_name}'
        self.campaign_name = campaign_name
        self.description = description
        self.is_approved = False
        self.concepts = {}
