from flask import jsonify, Blueprint, request, make_response
from bidboard.billboards.model import Billboard
import simplejson as json

billboards_api_blueprint = Blueprint('billboards_api',
                                __name__,
                                template_folder='templates')


@billboards_api_blueprint.route('/', methods=['GET'])
def index():
    billboards = Billboard.query.all()

    all_billboards = []
    for billboard in billboards:
        billboard.get_bid_times()
        del billboard.__dict__['_sa_instance_state']
        all_billboards.append(billboard.__dict__)

    responseObject = {
        'status': 'success',
        'message': 'All billboards returned',
        'all_billboards': all_billboards
    }

    return make_response(json.dumps(responseObject)), 201


@billboards_api_blueprint.route('/schedule', methods=['GET'])
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
        media = user.media
        all_ads = []
        for medium in media:
            del medium.__dict__['_sa_instance_state']
            all_ads.append(medium.__dict__)
        
        responseObject = {
            'status': 'success',
            'message': 'All ads media for user returned',
            'all_ads': all_ads
        }

        return make_response(jsonify(responseObject)), 201

    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401
