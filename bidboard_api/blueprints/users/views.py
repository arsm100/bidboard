from flask import jsonify, Blueprint, request, make_response
from bidboard.users.model import User, db

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.query.all()

    # there is probably a more efficient to do this
    users = [{"id": int(user.id), "company_name": user.company_name, "description": user.description, "email": user.email, "first_name": user.first_name, "last_name": user.last_name} for user in users]

    return jsonify(users)

@users_api_blueprint.route('/create', methods=['POST'])
def create():
    # get the post data
    post_data = request.get_json()

    new_user = User(
        company_name=post_data.get('company_name'),
        first_name=post_data.get('first_name'),
        last_name=post_data.get('last_name'),
        email=post_data.get('email').lower(),
        password=post_data.get('password')
    )

    if len(new_user.validation_errors) > 0:

        responseObject = {
            'status': 'fail',
            'message': new_user.validation_errors
        }

        return make_response(jsonify(responseObject)), 401

    else:
        db.session.add(new_user)
        db.session.commit()
        auth_token = new_user.encode_auth_token(new_user.id)
        
        responseObject = {
            'status': 'success',
            'message': 'Successfully created a user and signed in.',
            'auth_token': auth_token.decode()
        }

        return make_response(jsonify(responseObject)), 201