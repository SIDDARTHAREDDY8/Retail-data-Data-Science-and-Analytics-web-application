# backend/app/__init__.py
import os
from flask import Flask
from flask_cors import CORS
import pyodbc

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to handle cross-origin requests
CORS(app)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# Database connection variables (hard-coded for simplicity)
DB_SERVER = 'siddureddy.database.windows.net'  # Your server name
DB_DATABASE = 'retail-db'  # Your database name
DB_USERNAME = 'sidduch'  # Your username
DB_PASSWORD = 'Siddu@1139'