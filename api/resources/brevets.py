"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet
from database.models import Checkpoint

class Brevets(Resource):
  def get(self):
    from flask_api import app
    json_object = Brevet.objects().to_json()
    return Response(json_object, mimetype="application/json", status=200)
  
  def post(self):
    try:
      from flask_api import app
      input_json = request.json # Get data sent from JS in HTTP POST request
      
      # We're adding information now - 
      # length, start time, and checkpoint information (dict)
      brev_distance = input_json["brevet_dist"]
      start_time = input_json["start_time"]
      checkpoints = input_json["cp_data"]
      cps = input_json["cps"]
      
      app.logger.debug(f"cps: {cps}")

      # Because checkpoints is a list, we want to loop through and create Checkpoint objects
      checkpointList = []
      length = len(cps)
      
      for i in range(length):
        checkpoint = Checkpoint(
          distance=checkpoints["cp_dist"][i],
          location=checkpoints["location"][i],
          open_time=checkpoints["ot"][i], 
          close_time=checkpoints["ct"][i],
        )
        checkpointList.append(checkpoint)
        app.logger.debug(f"checkpointlist: {checkpointList}")
      
      _object = Brevet(length=brev_distance, start_time=start_time, checkpoints=checkpointList, cps=cps).save()
      
      app.logger.debug(f"id: {_object.id}")
      return {'_id': str(_object.id)}, 200 
    
    except Exception as e:
      app.logger.error(str(e))
      return -1