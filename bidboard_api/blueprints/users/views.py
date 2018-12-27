from flask import jsonify, Blueprint, request
from bidboard.users.model import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.query.all()

    # there is probably a more efficient to do this
    users = [{"id": int(user.id), "company_name": user.company_name, "description": user.description, "email": user.email, "first_name": user.first_name} for user in users]

    return jsonify(users)
