"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet
from database.models import Checkpoint

from datetime import datetime

class Brevets(Resource):
  def get(self):
    from flask_api import app
    json_object = Brevet.objects().to_json()
    app.logger.debug(f"object: {json_object}")
    return Response(json_object, mimetype="application/json", status=200)
  
  def post(self):
    from flask_api import app
    
    input_json = request.json # Get data sent from JS in HTTP POST request
    
    # We're adding information now - 
    # length, start time, and checkpoint information (dict)
    brev_distance = input_json["length"]
    start_time = input_json["start_time"]
    checkpoints = input_json["checkpoints"]  
    
    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")

    # Because checkpoints is a list, we want to loop through and create Checkpoint objects
    length = len(checkpoints["distance"]) # Get length of the array holding the distances

    checkpointList = []
    for i in range(length):
      open_t = datetime.strptime(checkpoints["open_time"][i], "%Y-%m-%dT%H:%M")
      close_t = datetime.strptime(checkpoints["close_time"][i], "%Y-%m-%dT%H:%M")
      checkpoint = Checkpoint(
        distance=checkpoints["distance"][i],
        location=checkpoints["location"][i],
        open_time=open_t,
        close_time=close_t
      )
      checkpointList.append(checkpoint)
    
    _object = Brevet(length=brev_distance, start_time=start_time, checkpoints=checkpointList).save()
    
    return {'_id': str(_object.id)}, 200 