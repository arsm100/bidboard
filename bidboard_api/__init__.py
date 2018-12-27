from bidboard import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from bidboard_api.blueprints.media.views import media_api_blueprint
from bidboard_api.blueprints.users.views import users_api_blueprint
from bidboard_api.blueprints.sessions.views import sessions_api_blueprint

app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/')
app.register_blueprint(media_api_blueprint, url_prefix='/api/v1/media')
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')

print("testing")
print(app.url_map)
