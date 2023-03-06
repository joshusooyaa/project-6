"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
import os
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import logging
from db_access import brevet_find, brevet_insert
import json
import requests

from datetime import timedelta

###
# Globals
###
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brev = request.args.get('brev', type=float) # No need for a fallback since there's always a value for brev
    start_time = request.args.get('bd', type=str)
    
    
    time = timedelta(hours=1.5)
    time2 = arrow.now()
    time2 = time + time2
    
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    open_time = acp_times.open_time(km, brev, arrow.get(start_time)).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brev, arrow.get(start_time)).format('YYYY-MM-DDTHH:mm')
    app.logger.debug("open_time={}".format(open_time))
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/_fetch")
def _fetch_data():
    brev, start, cp_dict = brevet_find()
    
    app.logger.debug(f"brev: {brev}")
    app.logger.debug(f"start: {start}")
    app.logger.debug(f"cp_dict: {cp_dict}")
    

    result = {"brevet": brev, "start_time": start, "cp_data": cp_dict}
    return flask.jsonify(result=result)



@app.route("/_insert", methods=["POST"])
def _insert_data():
    try:
        input_json = request.json

        start_date = input_json["start_date"]
        brevet_distance = input_json["brevet_distance"]
        cp_data = input_json["items"]

        _id = brevet_insert(brevet_distance, start_date, cp_data)
        
        app.logger.debug(f"\n\nid is: {_id}\n\n")
        
        return flask.jsonify(result={}, message="Inserted!", status=1, mongo_id=_id)

    except:
        return flask.jsonify(result={}, message="Server error!", status=0, mongo_id="None")

#############

if __name__ == "__main__":
    app.run(port=port_num, host="0.0.0.0")
