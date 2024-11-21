from flask import Flask
from database.mongodb import init_db
from routes.crud import bp as crud_bp
from routes.predict import bp as predict_bp

def create_app():
    app = Flask(__name__)

    # Initialize the database
    init_db()

    # Register routes
    app.register_blueprint(crud_bp)
    app.register_blueprint(predict_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
