
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"- Dates and precipitation values from 2016-08 to 2017-08 <br/>"
        f"/api/precipitation<br/>"+

        f"- Most active stations from the data set <br/>"
        f"/api/stations<br/>"+

        f"- Dates and temperature observations  from 2016-08 to 2017-08<br/>"
        f"/api/temperature<br/>"+

        f"- Calculate TMIN, TAVG, and TMAX for all dates greater than and equal to a given start date<br/>"        
        f"/api/<start><br/>"+

        f"- Calculate TMIN, TAVG, and TMAX for  dates between a given  start date and end date inclusive<br/>"        
        f"/api/<start>/<end>"
    )


@app.route("/api/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using `date` as the key and `prcp` as the value."""
    # Query date and prcp
    prcp_query= session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >='2016-08-23', Measurement.date <='2017-08-23').all()

    # # Create a dictionary from the row data and append to a list of all_passengers
    # precipitation_dict = dict(prcp_query)

    all_data = []
    for date,prcp in prcp_query:
       data_dict = {}
       data_dict["date"] = date
       data_dict["prcp"] = prcp
       all_data.append(data_dict)

    return jsonify(all_data)

@app.route("/api/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    # Query most active stations
    active_stations = session.query(Station.station, Station.name)
    # #Convert list of tuples to list
    # active_stations_List = [i[0] for i in active_stations]
    station_data = []
    for station, name in active_stations:
       station_dict = {}
       station_dict["station id"] = station
       station_dict["name"] = name
       station_data.append(station_dict)

    return jsonify(station_data)
    

@app.route("/api/temperature")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the last 12th months."""
    # Query for the dates and temperature observations from a year from the last data point.
    
    initial_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs_query= session.query(Measurement.date, Measurement.tobs).\
        filter (Measurement.date >=initial_date).all()
    
    tobs_data = []
    for date, tobs in tobs_query:
       tobs_dict = {}
       tobs_dict["Date"] = date
       tobs_dict["Temperature"] = tobs
       tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/<start>")
def start_date(start):
    tobs_start = [func.max(Measurement.tobs),
                func.min(Measurement.tobs),
                func.avg(Measurement.tobs)]
    results = session.query(*tobs_start).\
        filter (Measurement.date >= start).all()

    start_temp_data = []
    for Tmax, Tmin, Tavg in results:
        start_dict = {}
        start_dict["Tmax"] = Tmax
        start_dict["Tmin"] = Tmin
        start_dict["Tavg"] = Tavg
        start_temp_data.append(start_dict)

    return jsonify(start_temp_data)
    
@app.route("/api/<start>/<end>")
def start_end_date(start, end):
    tobs_start_end = [func.max(Measurement.tobs),
                func.min(Measurement.tobs),
                func.avg(Measurement.tobs)]
    temps_start_end = session.query(*tobs_start_end).\
        filter (Measurement.date >= start, Measurement.date <= end).all()
    
    start_end_temp_data = []
    for Tmax, Tmin, Tavg in temps_start_end:
        start_end_dict = {}
        start_end_dict["Tmax"] = Tmax
        start_end_dict["Tmin"] = Tmin
        start_end_dict["Tavg"] = Tavg
        start_end_temp_data.append(start_end_dict)

    return jsonify(start_end_temp_data)


if __name__ == '__main__':
    app.run(debug=True)








    



