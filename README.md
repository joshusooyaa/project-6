# UOCIS322 - Project 6 #
### Brevet time calculator with MongoDB, and a RESTful API!

# RUSA ACP Control Time Calculator

## **How to run**
Simply run the command `docker-compose up --build -d` or remove `-d` if you wish to look at the logs of the server. You can then connect to your local host via localhost:5002 and you can connect to the page.

To access the database, you can connect in your browser going to http://localhost:5001/api/brevets and this will list all of the brevets in the database. Similarily, you can use curl -X "GET" http://localhost:5001/api/brevets.

POST, DELETE, and PUT requests cannot be done through the webpage, and must be done using curl. You also must have the ID of the brevet object in order to carry out these requests. An ID can be obtained by a GET request to brevets and finding all the objects. There you can choose which object you'd like to send the request to (copy the obj ID). 

After copying the obj ID you'll make requests to http://localhost:5001/api/brevet/<id_here>

`DELETE`: curl -X "DELETE" http://localhost:5001/api/brevet/<id_here>

`PUT`: curl -X "PUT" -H 'Content-Type: application/json' -d '{"brevet_distance":"###","start_date":"YYYY-MM-DDTHH:MM","items":{"location":[""],"ot":["YYYY-MM-DDTHH:MM"],"ct":["YYYY-MM-DDTHH:MM"],"cp_dist":["dist_in_km"]}}' http://localhost:5001/api/brevet/<id_here>

`GET`: curl -X "GET" -H http://localhost:5001/api/brevet<id_here>


# Flask
## `db_access.py`
`db_access.py` contains two main functions, `brevet_insert` and `brevet_find`. These two functions are used to make requests to the API. 

`brevet_find` does the following:
1. Sends a GET request to the specified ULR. This URL is the API_URL/brevets -- brevets is a resource of the flask API.
2. Returns the data in brevets

`brevet_insert` does the following:
1. Sends a POST request to the specified URL. This URL is the API_URL/brevets -- brevets is a resource of the flask API. This resource will then handle the post request (which will be discussed in the API section)
2. Returns the id of the object that was inserted

## `acp_times.py`
`acp_times.py` Contains two main functions, `open_time` and `close_time`. These two functions calculate the open and close time of the distances provided. 

`open_time` has several rules.
1. If the distance is 0km it returns the start time of the race
2. If the distance is greater than the brevet distance, then it'll make sure to only return a time calculated up to the brevet distance (so if the distance is 305 km, it'll only calculate for 300km)
3. Otherwise, the time is calculated using distance intervals with their associated speeds. 

`close_time` follows a similar structure.
1. If the distance is 0km it returns 1 hour after the start time
2. If the distance is greater than the brevet distance then it'll make sure to return a fixed value for that brevet_distance. 
3. If the distance is <= 60 then the time is calculated by distance/20 + 1 and that is used to shift the time. 

All time is in YYYY-MM-DDTHH:MM format and must stay in this format. Both functions ensure that this format is kept by using arrow time and using the shift function the adjust the time. `brevet_start_time` is what gets shifted - as we are calculating the time based off of the beginning of the race each time. 

## `flask_brevets.py`
`flask_brevets.py` is updated to make sure the correct control distance and time is passed in so `acp_times.py` can calculate the correct times. For `flask_brevets.py` to pass a control distance, start time and brevet distance, it needs to get the information from the webpage (specifically from the JSON HTTP request) - so it uses request.args.get(). These arguments are passed in the Javascript from the getJSON request in `calc.html`. Using these arguments, they are then saved as variables in `flask_brevets.py` and are passed to the functions in `acp_times.py` to get the correct time calculations. Once this is done, the open and close times are saved and passed back to the Javascript in `calc.html` as a JSON file.

When `flask_brevets.py` recieves a request from the Javascript (POST or GET request) it'll call either `brevet_find` or `brevet_insert`. If it inserts, it'll return the id of the object inserted along with a message otherwise it'll fail (send failure message). If it successfully fetches, then it'll return the data to the Javascript. 

## `calc.html`
`calc.html` has been updated to make sure that the necesarry information is passed to `flask_brevets.py`. It does this by collecting the brevet distance (km) from the page, as well as the begin_date. The KM was already implemented, but that is also collected. These are then passed as arguments when sending the JSON HTTP request.
 
Once the `flask_brevets.py` sends a response back (sending the JSON back) it unpacks the information (open and close time) and updates the HTML with the open and close time that. 

`calc.html` has also now been updated to send and fetch data to/from the database.

On click of the submit button, the data is packaged up from the HTML file and sent as a POST request to `flask_brevets.py`. `flask_brevets.py` will then send back a result saying whether or not it failed. If it suceeded, all data is wiped from the screen and the user is left with the starting page (but their data has been saved). The user can now, if they wish, click on the Display button where a GET request is sent for a JSON file from `flask_brevets.py`. `flask_brevets.py`, as mentioned before, will get the data from the database and return the documents as a JSON file. The Javascript then unpack this data and updates each field with its respective data.  

# Flask API
This section handles all HTTP requests. It uses mongoengine to handle these requests.

## `flask_api.py` 
`flask_api.py` connects to MongoDB via "connect", then all resoures are added. Once these resources are added, `db_access.py` can send requests to the API_URL/resource_path given how the resource was added to reach that resource. For example, api.add_resource(Brevets, "/api/brevets") can now be reached by API_URL/api/brevets - so when a post or get request is sent to this resource, the appropriate method that was called will be run inside Brevets.  

## `brevets.py` 
`brevets.py` is one of the two resources used by the API. This resource will respond to GET and POST requests from the collection where all the brevets are stored. How it does this is simple - when there is a GET request sent from `db_access.py` the "get" method will be called here. This method uses the method "objects()" from mongoengine to get all the Brevet objects. Keep in mind that 'Brevet' is made into a collection, and it contains 'Brevet' objects as documents. "Brevet.objects()" will return all documents inside of the brevet collection. These are then converted to a json object, and that object is returned to `db_access.py`. 

The post method does a little more work, but essentially all that happens is that the data is separated into four different sections. All the checkpoint information is then stored as Checkpoint subdocuments which will be put into the Brevet document. The ".save()" method is used - this is apart of mongoengine. It saves the object, say Brevet(...).save() -- "..." gets saved to the required fields, and the Brevet object is saved as a document inside the brevet collection.

## `brevet.py`
`brevet.py` is very similar to `brevets.py` except that it deals with single objects inside the brevet database. The object id is used to access the document inside brevet. `brevet.py` handles get (which we already covered, except this time it only gets the document corresponding to the id), put, and delete. Put is very similar to post, except instead of creating a new document it will update the document with the id passed in the request. Delete is also very simple in that it simply deletes the object associated with the id - the document will no longer be able to be accessed once deleted since it's been removed from the collection, and from the database all together. 

## `models.py`
`models.py` is very simple in that it simply defines the structure of the data stored inside of the MongoDB. Brevet tells us how brevet (collection) will store its documents - they will be brevet objects. Checkpoints is a little different in that it's a subdocument, meaning that it exists inside of a document. Well, Checkpoints will be subdocuments of Brevet objects.

-----

## Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.

RESTful API implemented by Josh Sawyer\
jsawyer2@uoregon.com
