"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet
from database.models import Checkpoint, convert_to_datetime

from datetime import datetime

class Brevets(Resource):
  def get(self):
    json_object = Brevet.objects().to_json()
    return Response(json_object, mimetype="application/json", status=200)
  
  def post(self):
    input_json = request.json # Get data sent from JS in HTTP POST request
    input_json = convert_to_datetime(input_json)
    _object = Brevet(**input_json).save()
    return {'_id': str(_object.id)}, 200 