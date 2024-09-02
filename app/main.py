# app/main.py

from flask import Flask, render_template
from redis import Redis
from app.routes.document_routes import document_blueprint
# from app.routes.auth_routes import auth_blueprint
# from app.routes.frontend_routes import frontend_blueprint
from app.config.config import Config
# from flask_cors import CORS


def create_app():
    # Create a Flask application instance
    app = Flask(__name__)
    # , template_folder='C:\\Users\\novneet.patnaik\\Documents\\GitHub\\music-app\\app\\templates',
    #             static_folder='C:\\Users\\novneet.patnaik\\Documents\\GitHub\\music-app\\app\\static'
    # CORS(app)
    redis = Redis(host='localhost', port=6379, db=0)

    # Load configuration from the Config class
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(document_blueprint, url_prefix='/documents')
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # app.register_blueprint(frontend_blueprint, url_prefix='/ui')

    # You can add more setup here if needed (e.g., database initialization, login manager setup)
    # Landing page route
    # @app.route('/')
    # def landing_page():
    #     return render_template('landing.html')

    return app


# Create an instance of the Flask application
app = create_app()
#
# if __name__ == '__main__':
#     # Run the Flask app
#     # You can specify the host and port number inside app.run()
#     # For example, app.run(host='0.0.0.0', port=5000)
#     app.run(host='0.0.0.0', port=5000, debug=True)  # Set debug=False in a production environment
