from bidboard import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from bidboard_api.blueprints.media.views import media_api_blueprint
from bidboard_api.blueprints.users.views import users_api_blueprint
from bidboard_api.blueprints.sessions.views import sessions_api_blueprint
from bidboard_api.blueprints.billboards.views import billboards_api_blueprint
from bidboard_api.blueprints.bids.views import bids_api_blueprint

app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/')
app.register_blueprint(media_api_blueprint, url_prefix='/api/v1/media')
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(billboards_api_blueprint, url_prefix='/api/v1/billboards')
app.register_blueprint(bids_api_blueprint, url_prefix='/api/v1/bids')
