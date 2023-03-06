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
    
    # Convert open time and close time to datetime objects if they are strings
    def __init__(self, *args, **kwargs):
      if ("open_time" in kwargs and "close_time" in kwargs):
        if (type(kwargs["open_time"]) == str):
          kwargs["open_time"] = datetime.strptime(kwargs["open_time"], "%Y-%m-%dT%H:%M")
        if (type(kwargs["close_time"]) == str):
          kwargs["close_time"] = datetime.strptime(kwargs["close_time"], "%Y-%m-%dT%H:%M")
      
      super(Checkpoint, self).__init__(*args, **kwargs)
        
        
class Brevet(Document):
    """
    A MongoEngine document containing:
      length: MongoEngine float field, required
      start_time: MongoEngine datetime field, required
      checkpoints: MongoEngine list field of Checkpoints, required
    """
    length = FloatField(required=True)
    start_time = DateTimeField(default=datetime.utcnow, required=True, format="%Y-%m-%dT%H:%M")
    checkpoints = EmbeddedDocumentListField(Checkpoint, required=True)
    cps = ListField(field=IntField(), required=True) # Used to save what cp the data is saved in
    
    # Convert start_time to datetime object if it's a string
    def __init__(self, *args, **kwargs):
      if ("start_time" in kwargs):
        if (type(kwargs["start_time"]) == str):
          kwargs["start_time"] = datetime.strptime(kwargs["start_time"], "%Y-%m-%dT%H:%M")
      
      super(Brevet, self).__init__(*args, **kwargs)
