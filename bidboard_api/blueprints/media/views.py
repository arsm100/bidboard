from flask import jsonify, Blueprint, request, make_response
from bidboard.media.model import Medium
from bidboard.users.model import User

media_api_blueprint = Blueprint('media_api',
                             __name__,
                             template_folder='templates')


@media_api_blueprint.route('/', methods=['GET'])
def index():
    if request.args.get('userId'):
        media = Medium.query.with_entities(Medium.medium_url).filter_by(user_id = int(request.args['userId'])).all()
    else:
        media = Medium.query.with_entities(Medium.medium_url).all()

    media = [medium[0] for medium in media]

    return jsonify(media)

@media_api_blueprint.route('/me', methods=['GET'])
def show():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        responseObject = {
            'status': 'failed',
            'message': 'No authorization header found'
        }

        return make_response(jsonify(responseObject)), 401

    user_id = User.decode_auth_token(auth_token)

    user = User.query.get(user_id)

    if user:
        media = Medium.query.with_entities(Medium.medium_url).filter_by(user_id = user.id).all()
        media = [medium[0] for medium in media]

        return jsonify(media)
    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401
