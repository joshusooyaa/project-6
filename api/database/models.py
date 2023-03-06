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
    open_time = DateTimeField(required=True)
    close_time = DateTimeField(required=True)
    cp = IntField(required=True)
    
    # Convert open time and close time to datetime objects
    def __init__(self, *args, **kwargs):
      if ("open_time" in kwargs and "close_time" in kwargs):
        kwargs["open_time"] = datetime.strptime(kwargs["open_time"], "%Y-%m-%dT%H:%M")
        kwargs["close_time"] = datetime.strptime(kwargs["close_time"], "%Y-%m-%dT%H:%M")
      
      super().__init__(*args, **kwargs)
        
        
      

class Brevet(Document):
    """
    A MongoEngine document containing:
      length: MongoEngine float field, required
      start_time: MongoEngine datetime field, required
      checkpoints: MongoEngine list field of Checkpoints, required
    """
    length = FloatField(required=True)
    start_time = DateTimeField(required=True)
    checkpoints = EmbeddedDocumentListField(Checkpoint, required=True)
    # cp = ListField(required=True)
    
    # Convert start_time to datetime object
    def __init__(self, *args, **kwargs):
      if ("start_time" in kwargs):
        kwargs["start_time"] = datetime.strptime(kwargs["start_time"], "%Y-%m-%dT%H:%M")
      
      super().__init__(*args, **kwargs)
