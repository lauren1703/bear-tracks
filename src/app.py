import json
from flask import Flask, request
from db import db

app = Flask(__name__)
db_filename = "beartracks.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# Get all events
@app.route("/api/events/")
def get_events(): 
    events = [e.serialize() for e in Event.query.all()]
    return success_response({"courses": events})