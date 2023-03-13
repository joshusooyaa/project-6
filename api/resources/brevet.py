"""
Resource: Brevet

Used for getting, posting, deleting, and putting a single brevet
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet
from database.models import Checkpoint

from datetime import datetime

class Brev(Resource):
  def get(self, _id):
    json_object = Brevet.objects.get(id=_id).to_json()
    return Response(json_object, mimetype="application/json", status=200)

  def delete(self, _id):
    Brevet.objects.get(id=_id).delete()

  def put(self, _id):
    from flask_api import app
    
    input_json = request.json
    
    update_dict = {} # This will contain what gets updated
    
    # get is used to store "None" if field is empty/ or rather, doesn't exist
    # a put request could end up wanting to just update brevet_distance, or checkpoints
    # and doesn't need to have all the other information
    brev_distance = input_json.get("length")
    checkpoints = input_json.get("checkpoints")
    start_time = input_json.get("start_time")
    
    if brev_distance:
      update_dict["length"] = brev_distance
    
    if start_time:
      start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
      update_dict["start_time"] = start_time
    
    checkpointList = None
    
    if checkpoints is not None:
      # Because checkpoints is a list, we want to loop through and create Checkpoint objects
      checkpointList = []
      length = len(checkpoints["distance"]) # Get length of the array holding the distances
      
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
      
      update_dict["checkpoints"] = checkpointList
    
    app.logger.debug(f"Dict: {update_dict}\n\n")
    
    Brevet.objects.get(id=_id).update(**update_dict)
  
  
# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200
#
# Why would you need both?
# Flask-RESTful's default behavior:
# Return python dictionary and status code,
# it will serialize the dictionary as a JSON.
#
# MongoEngine's objects() has a .to_json() but not a .to_dict(),
# So when you're returning a brevet / brevets, you need to convert
# it from a MongoEngine query object to a JSON and send back the JSON
# directly instead of letting Flask-RESTful attempt to convert it to a
# JSON for you.
