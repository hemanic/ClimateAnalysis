import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to the DB
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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )

###Precipitation
@app.route("/api/v1.0/precipitation")
def prcp(input_date):
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    """Return a list of precipitation data with date as the key and prcp as the value"""
    # Query data
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all() 

    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

###Station Data
@app.route("/api/v1.0/stations")
def stations():
    station=session.query(Station.station)
    stationresults=list(np.ravel(results))
    return jsonify(stationresults)

###Temperature Data

#previous year temp
@app.route("/api/v1.0/tobs/<start_date>")
def temp():
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
#     year_temp = session.query(Measurement.tobs).\
#       filter(Measurement.date >= previous_year, Measurement.station == 'USC00519281').\
#       order_by(Measurement.tobs).all()

#     year_temp = []
#     for y_t in year_temp:
#         yrtemp = {}
#         yrtemp["tobs"] = y_t.tobs
#         year_temp.append(yrtemp)

#     return jsonify(year_temp)    

    station_temp = session.query(Measurement.tobs).\
      filter(Measurement.date >= previous_year, Measurement.station == 'USC00519281').\
      order_by(Measurement.tobs).all()

    year_temp = list(np.ravel(station_temp))
    return jsonify(year_temp)

#temp mins, maxs, and avgs for given start date
def temp_start(start_date):
    temp_dict = {}
    start_query = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                 filter(Measurement.date >= func.strftime("%Y-%m-%d",start_date)).all()
    temp_dict["Min_temp"] = start_query[0]
    temp_dict["Avg_temp"] = start_query[1]
    temp_dict["Max_temp"] = start_query[2]
    return jsonify(temp_dict)


#temp mins, maxs, and avgs for given start+end date
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start_date2,end_date):
    temp_dict_2 = {}
    start_end_query = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                   filter(Measurement.date >= func.strftime("%Y-%m-%d",start_date2)).\
                   filter(Measurement.date <= func.strftime("%Y-%m-%d",end_date)).all()
    temp_dict_2["Temp_min"] = start_end_query[0]
    temp_dict_2["Temp_avg"] = start_end_query[1]
    temp_dict_2["Temp_max"] = start_end_query[2]
    return jsonify(temp_dict_2)


if __name__ == '__main__':
    app.run(debug=True)
