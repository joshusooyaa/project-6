"""
Brevets RESTful API
"""
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect
import logging

# You need to implement two resources: Brevet and Brevets.
# Uncomment when done:
# from resources.brevet import Brevet
from resources.brevets import Brevets

# Connect MongoEngine to mongodb
connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017/brevetsdb")

# Start Flask app and Api here:
app = Flask(__name__) 
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)

api = Api(app)

# Bind resources to paths here:
api.add_resource(Brevets, "/api/brevets")
# api.add_resource(Brevet, "/brevet/<_id>")

if __name__ == "__main__":
    app.run(port=port_num, host="0.0.0.0")
