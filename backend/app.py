import os
import logging

from flask import Flask, jsonify # type: ignore #
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_cors import CORS # type: ignore
from dotenv import load_dotenv # type: ignore
import pymysql # type: ignore
from sqlalchemy import text # type: ignore

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Database configuration
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# 1. Home route
@app.route('/')
def home():
    return jsonify({"message": "EduSphere API is running!"})

# 2. Check DB with SQLAlchemy
@app.route('/check-db')
def check_db():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return jsonify({"message": "Database connection successful!"})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Database connection failed"}), 500

# 3. Check DB with PyMySQL directly
@app.route('/check-db-direct')
def check_db_direct():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        conn.close()
        return jsonify({"message": "Direct MySQL connection successful!"})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Direct MySQL connection failed"}), 500

# Example “Hello, World!” route
@app.route('/hello')
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
    # Create tables at startup (replaces the removed @app.before_first_request)
    try:
        with app.app_context():
            db.create_all()
            logging.info("Database tables created or verified.")
    except Exception as e:
        logging.error(f"Error creating tables: {str(e)}")

    # Run the Flask app
    app.run(host="0.0.0.0", port=5001, debug=True)
