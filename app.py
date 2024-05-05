# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
# Declare a Base using `automap_base()`
Base = automap_base()


# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

print

#Measurement class assigned to variable called Measurement
Measurement = Base.classes.measurement

#Station class assigned to a variable called Station
Station = Base.classes.station
# Create a session
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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipiation():
    """Returning the json representation of the dictionary, date and precipitation"""
    #Query for the precipition and dates from the last year (dates found in climate_starter.ipynb section)
    results = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= '2016-08-23').all()

    #Converting the results from the query into the dictionary
    precipiation_data = []
    for date, prcp in results:
        precipiation_dict = {}
        precipiation_dict[date] = prcp
        precipiation_data.append(precipiation_dict)
    return jsonify(precipiation_data)
    
@app.route("/api/v1.0/stations")
def stations():
    """Returning the json representation of the dictionary, list of each station"""
    #Query for all stations
    results = session.query(Station.station).all()

    #Convert the list of tuples into a normal list
    station_lists = list(np.ravel(results))

    return jsonify(station_lists)

@app.route("/api/v1.0/tobs")
def tobs():
    """return a json list of temperture data for the last year"""
    #Query the dataset for dates and temperatures for the last year for the most active station
    results = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= '2016-08-23').all()

    #Convert query into the dictionary
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start(start):
    """return a list of the minimum, maximum and average temperatures for a given start date"""
    #Query to retrieve the min, max and average temps 
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start).all()

    #Convert query into a dictionary
    temp_stats = []
    for min_temp, max_temp, avg_temp in results:
        temp_dict = {}
        temp_dict["Minimum Temperature"] = min_temp
        temp_dict["Maximum Temperature"] = max_temp
        temp_dict["Average Temperature"] = avg_temp
        temp_stats.append(temp_dict)
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """return a list of the minimum, maximum and average temperatures for a given start and end date range"""
    #Query to retrieve the min, max and average temps 
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end).all()
    
     #Convert query into a dictionary
    temp_stats = []
    for min_temp, max_temp, avg_temp in results:
        temp_dict = {}
        temp_dict["Minimum Temperature"] = min_temp
        temp_dict["Maximum Temperature"] = max_temp
        temp_dict["Average Temperature"] = avg_temp
        temp_stats.append(temp_dict)
    return jsonify(temp_stats)
    
if __name__ == '__main__':
    app.run(debug=True)
