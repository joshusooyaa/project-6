from mongoengine import *
from datetime import datetime

class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
      distance: MongoEngine float field, required, (checkpoint distance in kilometers),
      location: MongoEngine string field, optional, (checkpoint location name),
      open_time: MongoEngine datetime field, required, (checkpoint opening time),
      close_time: MongoEngine datetime field, required, (checkpoint closing time).
    """
    distance = FloatField(required=True)
    location = StringField(required=False)
    open_time = DateTimeField(required=True, format="%Y-%m-%dT%H:%M")
    close_time = DateTimeField(required=True, format="%Y-%m-%dT%H:%M")     
   
     
class Brevet(Document):
    """
    A MongoEngine document containing:
      length: MongoEngine float field, required
      start_time: MongoEngine datetime field, required
      checkpoints: MongoEngine list field of Checkpoints, required
    """
    length = FloatField(required=True)
    start_time = DateTimeField(required=True, format="%Y-%m-%dT%H:%M")
    checkpoints = EmbeddedDocumentListField(Checkpoint, required=True)
    
# Used to convert times into datetime objects
# It's in "models" because Brevet and Checkpoint require DateTimeFields and both 
# resources will send "string" times that should be converted to datetime objects
def convert_to_datetime(input_json):
    # Need to turn the times into datetime objects
    if "start_time" in input_json:
      input_json["start_time"] = datetime.strptime(input_json["start_time"], "%Y-%m-%dT%H:%M")
    
    # Need to check because this could be a put request
    if "checkpoints" in input_json:
      for checkpoint in input_json["checkpoints"]: # Go through and change all string dates to datetime objects
        # Now check if open time is in checkpoint
        # If it isn't, then mongoengine will throw an error anyways - the error shown should not be here
        # No need to check if it's a string because how the javascript is set up, it's always sent as a string
        if "open_time" in checkpoint: 
          checkpoint["open_time"] = datetime.strptime(checkpoint["open_time"], "%Y-%m-%dT%H:%M")
        if "close_time" in checkpoint:
          checkpoint["close_time"] = datetime.strptime(checkpoint["close_time"], "%Y-%m-%dT%H:%M")
    
    return input_json
