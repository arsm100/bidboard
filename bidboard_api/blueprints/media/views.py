from flask import jsonify, Blueprint, request, make_response
from bidboard.media.model import Medium, db
from bidboard.users.model import User
import random
from werkzeug.utils import secure_filename
from bidboard.helpers.helpers import allowed_file, upload_file
from bidboard.helpers.content_review import review_media


media_api_blueprint = Blueprint('media_api',
                                __name__,
                                template_folder='templates')


@media_api_blueprint.route('/', methods=['GET'])
def index():
    if request.args.get('userId'):
        media = Medium.query.with_entities(Medium.medium_url).filter_by(
            user_id=int(request.args['userId'])).all()
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


@media_api_blueprint.route("/upload", methods=['POST'])
def upload():
        # check there is a file, campaign_name and description
    form = request.form

    if "user_media" not in request.files or not form.get('campaign_name') or not form.get('description'):

        responseObject = {
            'status': 'fail',
            'message': "All fields are required"
        }

        return make_response(jsonify(responseObject)), 401

    # grab the file, campaign_name and description
    file = request.files["user_media"]
    user_id = form['user_id']
    campaign_name = form['campaign_name']
    description = form['description']

    # check there is a name
    if file.filename == "":

        responseObject = {
            'status': 'fail',
            'message': "Invalid file name"
        }

        return make_response(jsonify(responseObject)), 401

    # check file size
    if len(file.read()) > (20 * 1024 * 1024):

        responseObject = {
            'status': 'fail',
            'message': "Max size allowed is 20 MB"
        }

        return make_response(jsonify(responseObject)), 401

    # check correct extension and upload if valid
    if file and allowed_file(file.filename):
        file.seek(0)
        serial_filename = f'{user_id}.{random.randint(1,100000)}.{file.filename}'
        file.filename = secure_filename(serial_filename)
        upload_file(file)

        new_medium = Medium(
            user_id=user_id,
            medium_name=str(file.filename),
            campaign_name=campaign_name,
            description=description
        )

        db.session.add(new_medium)
        db.session.commit()
        
        review_media(new_medium)
        del new_medium.__dict__['_sa_instance_state']

        responseObject = {
            'status': 'success',
            'message': 'Media uploaded successfully. Check approval status in the dashboard',
            'medium': new_medium.__dict__
        }

        return make_response(jsonify(responseObject)), 201

    else:

        responseObject = {
            'status': 'fail',
            'message': "Media format not supported"
        }

        return make_response(jsonify(responseObject)), 401
