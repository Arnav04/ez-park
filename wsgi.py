from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

from app import app

print(__name__)

if __name__ == "__main__":
	app.run(host='0.0.0.0')
