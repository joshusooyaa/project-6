"""
Resource: Brevet

Used for getting, posting, deleting, and putting a single brevet
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet
from database.models import Checkpoint, convert_to_datetime

from datetime import datetime

class Brev(Resource):
  def get(self, _id):
    json_object = Brevet.objects.get(id=_id).to_json()
    return Response(json_object, mimetype="application/json", status=200)

  def delete(self, _id):
    Brevet.objects.get(id=_id).delete()

  def put(self, _id):
    input_json = request.json
    input_json = convert_to_datetime(input_json)
    Brevet.objects.get(id=_id).update(**input_json)


