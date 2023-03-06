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
    input_json = request.json
    
    brev_distance = input_json["brevet_distance"]
    start_time = datetime.strptime(input_json["start_date"], "%Y-%m-%dT%H:%M")
    checkpoints = input_json["items"]
    cps = input_json["cps"]
    
    checkpointList = []
    length = len(cps)
      
    for i in range(length):
      checkpoint = Checkpoint(
        distance=checkpoints["cp_dist"][i],
        location=checkpoints["location"][i],
        open_time=datetime.strptime(checkpoints["ot"][i], "%Y-%m-%dT%H:%M"),
        close_time=datetime.strptime(checkpoints["ct"][i], "%Y-%m-%dT%H:%M")
      )
      checkpointList.append(checkpoint)
    
    Brevet.objects(id=_id).update(length=brev_distance, set__start_time=start_time, checkpoints=checkpointList, cps=cps)
  
  
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
