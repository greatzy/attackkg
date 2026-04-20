#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from app import create_app, db

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
