import os 
import requests
from datetime import datetime

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"

def brevet_insert(brevet_dist, start_time, cp_data, cps):
  from flask_brevets import app
  _id = requests.post(f"{API_URL}/brevets", json={"brevet_distance": brevet_dist, "start_date": start_time, "items": cp_data, "cps": cps}).json()
  return _id
  
def brevet_find():
  from flask_brevets import app
  races = requests.get(f"{API_URL}/brevets").json()
  # races contains a list of dictionaries containing all saved brevet information
  # only need to get the last saved race data
  # also check if races actually has something in it, if it's empty we'll get indexerror
  if races:
    race = races[-1]
  else:
    return -1

  
  # All datetime objects were converted to BSON format (ms since Jan 1, 1970) - need to change back
  # To change back, divide by 1000 since fromtimestamp wants it in seconds
  # Then format the time back to how it was originally inputted (strftime)
  time = race["start_time"]
  app.logger.debug(f"start time is: {time}")
  race["start_time"] = datetime.fromtimestamp(int(race["start_time"]["$date"]) / 1000).strftime("%Y-%m-%dT%H:%M")
  time = race["start_time"]
  app.logger.debug(f"start time is now: {time}")
  for i in range(len(race["cps"])):
    race["checkpoints"][i]["open_time"] = datetime.fromtimestamp(int(race["checkpoints"][i]["open_time"]["$date"]) / 1000).strftime("%Y-%m-%dT%H:%M")
    race["checkpoints"][i]["close_time"] = datetime.fromtimestamp(int(race["checkpoints"][i]["close_time"]["$date"]) / 1000).strftime("%Y-%m-%dT%H:%M")
  
  app.logger.debug(f"Race: {race}")
  
  # race is a dictionary: {"length": length, "start_time": start_time, "checkpoints": list, len 0, containing a dict of cp data}
  # Return all entries (except for id)
  return race["length"], race["start_time"], race["checkpoints"], race["cps"]
