import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_, desc
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Define connection to hawaii.sqlite file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the existing database into a new model
Base = automap_base()

# Reflect Database and generate ORM classes based on the SQLite tables
Base.prepare(autoload_with = engine)

# Save reference for the ORM classes
measurement = Base.classes.measurement
station = Base.classes.station


#################################################
# Flask Setup
#################################################
# Create new Flask Application object
app = Flask(__name__)

# From the Flask library, configure to not sort the keys when serializing JSON responses
app.json.sort_keys = False


#################################################
# Flask Routes
#################################################

############# Route #1 (Homepage) ###############
@app.route("/")
def homepage():
    # Welcome the user to the API and list all available routes
    return (
        f"Welcome to the Climate Data Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"<br/>"
        f"Replace 'start_date' and 'end_date' with actual date in the following format: YYYYMMDD"
    )


########## Route #2 (Precipitation) #############
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Establish session (link) from Python to the SQLite DB
    session = Session(engine)

    # Using 'func', query the maximum date from 'measurement' and return the first result (using scalar()); Convert the date string to datetime object
    recent_date = session.query(func.max(measurement.date)).scalar()
    recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')

    # Using 'timedelta' from the DateTime Library, calculate the difference between the recent date and 365 days
    start_date = recent_date - dt.timedelta(days = 365)

    # Convert the Start & Recent dates back into string in YYYY-MM-DD format
    start_date = dt.datetime.strftime(start_date, '%Y-%m-%d')
    recent_date = dt.datetime.strftime(recent_date, '%Y-%m-%d')

    # Pre-define the columns from 'measurement' used for the upcoming query...
    date_prcp_columns = [func.date(measurement.date), measurement.prcp]

    # Query all date and prcp elements from 'measurement' where...
    # The date is greater than or equal to 2016-08-23 AND the date is less than or equal to 2017-08-23 
    # '_and' function used to combine multiple conditionals within a single filter in the same query
    # *date_prcp_columns is to unpack the columns from the list in sequence using the '*' operator
    prcp_12_months = session.query(*date_prcp_columns).filter(
        and_(
            func.date(measurement.date) >= start_date,
            func.date(measurement.date) <= recent_date
        )
    ).order_by(measurement.date).all()

    # Terminate the SQLAlchemy session; no additional queries to be conducted for this route
    session.close()


    # Create an empty list to store dictionaries of precipitation data
    precipitation_data = []

    # For every date and prcp value in the queried data...
    # Store date and prcp in a dict where the former is a key, and the latter is the value.
    # append the list with the dict
    for date, prcp in prcp_12_months:
        temp_dict = {date : prcp}
        precipitation_data.append(temp_dict)


    # Message to inform the user of the data analysis conducted in this route
    message = f"[JSON Dictionary Representation] Precipitation Data for the previous 12 months in the database (sorted by date)."

    # Store key information (message, start date, recent date, queried data) in a dictionary
    results = {
        "Data Analysis": message,
        "Start Date": start_date,
        "End Date": recent_date,
        "Final Query Result": precipitation_data
    }

    # Return the JSON 'results' dictionary that includes key information as well as the JSON representation of the Precipitation dictionary
    return jsonify(results)


############# Route #3 (Stations) ###############
@app.route("/api/v1.0/stations")
def list_stations():
    # Establish session (link) from Python to the SQLite DB
    session = Session(engine)

    # Query the count of all rows in the 'station' table (Total Number of Stations)
    total_stations = session.query(station).count()

    # Query all stations from 'station' and...
    # the result count of observations a station has been listed where...
    # the 'station' column from both the 'measurement' & 'station' tables match i.e. common link between 2 tables
    # In addition, group the queried data by 'station' from the 'station' table and...
    # Sort the queried data in descending order of the result count of observations (using the 'desc' function)
    get_stations = session.query(station.station, func.count().label('count')).join(
        measurement,
        station.station == measurement.station
    ).group_by(measurement.station).order_by(desc('count')).all()

    # Terminate the SQLAlchemy session; no additional queries to be conducted for this route
    session.close()


    # Create an empty list to store lists of station w/ observation count
    stations_list = []

    # For every station and total observation count value in the queried data...
    # Store station and count in a temporary list
    # append the main list with the temporary list    
    for name, count in get_stations:
        temp_list = [name, count]
        stations_list.append(temp_list)


    # Message to inform the user of the data analysis conducted in this route
    message = f"[JSON List] ALL Stations with observation counts (descending order) in the database."

    # Store key information (message, total stations count, queried data) in a dictionary
    results = {
        "Data Analysis": message,
        "Total No. Stations": total_stations,
        "Final Query Result": stations_list
    }

    # Return the JSON 'results' dictionary that includes key information as well as the JSON list of all stations
    return jsonify(results)


############ Route #4 (Temperature) #############
@app.route("/api/v1.0/tobs")
def list_tobs():
    # Establish session (link) from Python to the SQLite DB
    session = Session(engine)

    # Query all stations from 'station' and...
    # the result count of observations a station has been listed where...
    # the 'station' column from both the 'measurement' & 'station' tables match i.e. common link between 2 tables
    # In addition, group the queried data by 'station' from the 'station' table and...
    # Sort the queried data in descending order of the result count of observations (using the 'desc' function)
    get_stations = session.query(station.station, func.count().label('observation_count')).join(
        measurement,
        station.station == measurement.station
    ).group_by(measurement.station).order_by(desc('observation_count')).all()


    # Using 'func', query the maximum date from 'measurement' and return the first result (using scalar()); Convert the date string to datetime object
    recent_date = session.query(func.max(measurement.date)).scalar()
    recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')

    # Calculate the start date 12 months from the recent date
    start_date = recent_date - dt.timedelta(days = 365)

    # Convert the Start & Recent dates back into string in YYYY-MM-DD format
    start_date = dt.datetime.strftime(start_date, '%Y-%m-%d')
    recent_date = dt.datetime.strftime(recent_date, '%Y-%m-%d')

    # Get the 'Most Active' Station from the previous queried data (first listed since it is already sorted in desc)
    most_active_station = get_stations[0].station

    # Pre-define the columns to use for the upcoming query
    date_tobs_columns = [func.date(measurement.date), measurement.tobs]

    # Query all dates and tobs values from 'measurement' where...
    # station is the most active station and where...
    # The date is greater than or equal to 2016-08-23 AND the date is less than or equal to 2017-08-23 
    # '_and' function used to combine multiple conditionals within a single filter in the same query
    # *date_tobs_columns is to unpack the columns from the list in sequence using the '*' operator
    tobs_12_months = session.query(*date_tobs_columns).filter(measurement.station == most_active_station).filter(
        and_(
            func.date(measurement.date) >= start_date,
            func.date(measurement.date) <= recent_date
        )
    ).all()

    # Terminate the SQLAlchemy session; no additional queries to be conducted for this route
    session.close()


    # Create an empty list to store lists of date w/ tobs data
    tobs_list = []

    # For every date and tobs in the queried data...
    # Store date and tobs in a temporary list
    # append the main list with the temporary list    
    for date, tobs in tobs_12_months:
        temp_list = [date, tobs]
        tobs_list.append(temp_list)

    # Message to inform the user of the data analysis conducted in this route
    message = f"[JSON List] Date & Temperature Observation (TOBS) Data for the 'Most Active Station' for the previous 12 months in the database."

    # Store key information (message, most active station, start date, recent date, queried data) in a dictionary
    results = {
        "Data Analysis": message,
        "Most Active Station" : most_active_station,
        "Start Date": start_date,
        "End Date": recent_date,
        "Final Query Result": tobs_list
    }

    # Return the JSON 'results' dictionary that includes key information as well as the JSON list of temperature observations for the previous year for the most active station.
    return jsonify(results)


############ Route #5 (Dynamic Route w/ Specified Start Date) #############
@app.route("/api/v1.0/<start_date>")
def stats_tobs_start_only(start_date):
    # Exception Handling: Attempt to...
    try:
        # Convert user-specified date (YYYYMMDD) into YYYY-MM-DD format
        start_date = dt.datetime.strptime(start_date, '%Y%m%d')
        start_date = start_date.strftime('%Y-%m-%d')
        
        # Establish session (link) from Python to the SQLite DB
        session = Session(engine)

        # Query the min, max and mean of the temperature (tobs) from 'measurement' where...
        # date is greater than or equal to the user-specified start date
        tob_stats = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(
            func.date(measurement.date) >= start_date
        ).all()

        # Terminate the SQLAlchemy session; no additional queries to be conducted for this route
        session.close()


        # Convert list of tuples into normal list
        stats_list = list(np.ravel(tob_stats))

        # Message to inform the user of the data analysis conducted in this route
        message = f"[JSON List] Minimum/Maximum/Average Temperature from the database from the given start date."

        # Store key information (message, user-specified start date, queried data) in a dictionary
        results = {
            "Data Analysis": message,
            "Given Start Date": start_date,
            "Final Query Result": stats_list
        }

        # Return JSON 'results' dictionary that includes key information as well as the JSON list of min, max, and average temperatures calculated from the given start date
        return jsonify(results)
    
    # Exception Handling: In the event an error occurs...
    except ValueError:

        # Messages to inform the user of the error and the correct date format to use
        error_message = f"Invalid Date Format! Please use the following format: 'YYYYMMDD'"
        example_message = f"/api/v1.0/20100101"

        # Store messages in a dictionry
        results = {
            "Error": error_message,
            "Correct Example": example_message,
        }

        # Return JSON 'results' dictionary of those messages
        return jsonify(results)
    


############ Route #6 (Dynamic Route w/ Specified Start & End Dates) #############
@app.route("/api/v1.0/<start_date>/<end_date>")
def stats_tobs_start_end(start_date, end_date):
    # Exception Handling: Attempt to...
    try:
        # Convert user-specified start date (YYYYMMDD) into YYYY-MM-DD format
        start_date = dt.datetime.strptime(start_date, '%Y%m%d')
        start_date = start_date.strftime('%Y-%m-%d')

        # Convert user-specified end date (YYYYMMDD) into YYYY-MM-DD format
        end_date = dt.datetime.strptime(end_date, '%Y%m%d')
        end_date = end_date.strftime('%Y-%m-%d')
        
        # Establish session (link) from Python to the SQLite DB
        session = Session(engine)

        # Query the min, max and mean of the temperature (tobs) from 'measurement' where...
        # date is greater than or equal to the user-specified start date AND...
        # date is less than or equal to the user-specified end date
        tob_stats = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(
            and_(
                func.date(measurement.date) >= start_date,
                func.date(measurement.date) <= end_date
            )
        ).all()

        # Terminate the SQLAlchemy session; no additional queries to be conducted for this route
        session.close()


        # Convert list of tuples into normal list
        stats_list = list(np.ravel(tob_stats))

        # Message to inform the user of the data analysis conducted in this route
        message = f"[JSON List] Minimum/Maximum/Average Temperature from the database from the given start date to the given end date."

        # Store key information (message, given start date, given end date, queried data) in a dictionary
        results = {
            "Data Analysis": message,
            "Given Start Date": start_date,
            "Given End Date": end_date,
            "Final Query Result": stats_list
        }

        # Return JSON 'results' dictionary that includes key information as well as the JSON list of min, max, and average temperatures calculated from the given start date to given end date
        return jsonify(results)
    
    # Exception Handling: In the event an error occurs...
    except ValueError:
        # Messages to inform the user of the error and the correct date format to use
        error_message = f"Invalid Date Format(s)! Please use the following format: 'YYYYMMDD'"
        example_message = f"/api/v1.0/20100101/20170823"

        # Store messages in a dictionary
        results = {
            "Error": error_message,
            "Correct Example": example_message,
        }

        # Return JSON 'results' dictionary of those messages
        return jsonify(results)


# Check if python script is the main program that is executed
# If so, run the app in debugging mode
if __name__ == "__main__":
    app.run(debug = True)