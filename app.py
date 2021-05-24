
# Import Modules
from datetime import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station 

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Create Home
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of climate data with date and prcp values"""
    # Query all dates and prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_dates
    all_dates = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        
        all_dates.append(precipitation_dict)

    return jsonify(all_dates)

#stations
@app.route("/api/v1.0/stations")
def stations():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations from the dataset"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    return jsonify(results)

#tobs
@app.route("/api/v1.0/tobs")
def tobs():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs for the most active station"""
    # Query all tobs
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23')
    session.close()

    # Create a dictionary from the row data and append to a list of all_dates
    active_dates = []
    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        active_dates.append(tobs_dict)

    return jsonify(active_dates)
#start only
@app.route("/api/v1.0/tobs/<start>")
def tobs_by_date(start):
    """Fetch the mintemp, maxtemp, avgtemp for a specific date, if date is non existent create a 404 error"""
     # Create our session (link) from Python to the DB
    session = Session(engine)
        # Query all tobs
    results = session.query(Measurement.date, Measurement.tobs).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_dates
    for date, tobs in results:
        query_dict = {}
        query_dict["date"] = date
        query_dict["tobs"] = tobs

    for date in range(query_dict['date']):

        if start == query_dict['date']:
            return jsonify([query_dict['date'],
            max(query_dict['tobs']), 
            min(query_dict['tobs']), 
            np.mean(query_dict['tobs'])]
            )

    return jsonify({"error": "date not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)



