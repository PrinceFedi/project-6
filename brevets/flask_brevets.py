"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import logging
import os

import arrow  # Replacement for datetime, based on moment.js
import flask
from flask import request
import requests
import acp_times  # Brevet time calculations

###
# Globals
###
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"


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
    time_and_date = request.args.get("time_and_date", type=str)
    brevet_distance = request.args.get("distance", 998, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    arrow_str = arrow.get(time_and_date, "YYYY-MM-DDTHH:mm")
    open_time = acp_times.open_time(km, brevet_distance, arrow_str).format("YYYY-MM-DDTHH:mm")
    close_time = acp_times.close_time(km, brevet_distance, arrow_str).format("YYYY-MM-DDTHH:mm")
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


###############
#
# Project 6 API Callers
#
#
###############

def brevets_insert(length, start_time, checkpoints):
    _id = requests.post(f"{API_URL}/brevets",
                        json={"length": length, "start_time": start_time, "checkpoints": checkpoints}).json()
    return _id


def brevets_fetch():
    lists = requests.get(f"{API_URL}/brevets").json()
    brevet = lists[-1]
    return brevet["length"], brevet["start_time"], brevet["checkpoints"]


@app.route("/_insert", methods=["POST"])
def _insert():
    """
    /insert : inserts a brevet into the database.
    Accepts POST requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    try:
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!

        # Because input_json is a dictionary, we can now get values of our 3 components that we are inserting:
        start_time = input_json["start_time"]  # Should be a string
        brevet_distance = input_json["brevet_distance"]
        brevet_checkpoint = input_json["brevet_checkpoint"]

        brevet_id = brevets_insert(brevet_distance, start_time, brevet_checkpoint)

        return flask.jsonify(result={},
                             message="Successfully Inserted!",
                             status=1,  # Are user-defined status which determines if successfully inserted our data
                             mongo_id=brevet_id)

    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                             message="Something went wrong... spain without the S",
                             status=0,
                             mongo_id='None')


@app.route("/_fetch")
def _fetch():
    """
    /fetch : fetches the newest to-do list from the database.
    Accepts GET requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    try:
        brevet_distance, start_time, brevet_checkpoint = brevets_fetch()
        return flask.jsonify(
            result={"start_time": start_time, "brevet_distance": brevet_distance,
                    "brevet_checkpoint": brevet_checkpoint},
            status=1,
            message="Successfully fetched our brevet!")
    except:
        return flask.jsonify(
            result={},
            status=0,
            message="Something went wrong... spain without the S")


#############

app.debug = os.environ["DEBUG"]
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run(port=port_num, host="0.0.0.0")
