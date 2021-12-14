import datetime as dt
from flask.templating import render_template
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template
from markupsafe import Markup, escape

# app = Flask(__name__)
# @app.route('/')

#def hello_world():
#    return 'Hello world'

# Access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")
# Reflect existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table with variables
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create session link from Python to the ddatabase
session = Session(engine)

# Setup Flask by defining the application
# (__name__) is called a Magic Method. References from where and how it is run
app = Flask(__name__)

# Example: 

#import app

#print("example __name__ = %s", __name__)

#if __name__ == "__main__":
#    print("example is being run directly.")
#else:
#    print("example is being imported")

# Routes must go under app = Flask(__name__)

@app.route("/")

def welcome():
    return render_template('template.html')  

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # create query to get all the stations in the database
    results = session.query(Station.station).all()
    # unravel results into one-dimensional array using function np.ravel() with results as the parameter
    # use list function list() to convert array into a list
    stations = list(np.ravel(results))
    # use jsonify to json the list
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query databases' primary station for all the temp observations from previous year
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    # unravel results into one-dimensional array using function np.ravel() with results as the parameter
    # use list function list() to convert array into a list
    temps = list(np.ravel(results))
    # use jsonify to json the list
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    # create a list to store min, avg, max
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # create an if not conditional to determine starting and ending dates
    if not end:
        # the *sel indicates that there will be multiple results for the query
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    # with dates at hand, this query will gather the statistics data on the data points
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)