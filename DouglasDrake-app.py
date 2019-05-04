import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from dateutil.parser import parse
import datetime as dt

# Adding this - DL
from sqlalchemy.orm import scoped_session, sessionmaker

#################################################
# Date parsing using dateutil.parser
#################################################

def try_to_parse_date (a_string):
    """
    Args: a_string is a string representation of a date.  Most
    dateformats are valid.  Since we are parsing with the fuzzy_with_tokens
    argument set to True, a_string may contain additional non-date information.

    Returns:
        a string representation of the parsed date in the format: 'YYYY-MM-DD'.

    Examples:
        try_to_parse_date("Today is Friday, May 3, 2019")
        '2019-05-03'
        try_to_parse_date("2017-01-01")
        '2017-01-01'
        try_to_parse_date("02/03/2019")
        '2019-02-03'
        try_to_parse_date("start=12-25-1990")
        '1990-12-25'
    """
    try:
        parsed = parse(a_string, fuzzy_with_tokens=True)
    except ValueError:
        print(f"Could not parse a date from `{a_string}`")
    else:
        parsed_dt = parsed[0]
        return parsed_dt.strftime("%Y-%m-%d")


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# Adding this - DL
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to both tables
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Welcome to the Hawaii Weather Observations API.<br/>"
        f"<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start=YYYY-MM-DD<br/>"
        f"/api/v1.0/start=YYYY-MM-DD/end=YYYY-MM-DD<br/>"
        f"<br/>"
        f"<br/>"
        f"Example requests with start and end dates are:<br/>"
        f"<blockquote/>"
        f"/api/v1.0/2012-03-01/2013-02-28 <br/>"
        f"/api/v1.0/start=2012-03-01/end=2013-02-28 <br/>"
        f"/api/v1.0/March 3, 2012/Feb. 28, 2013 <br/>"
        f"/api/v1.0/start=2019-05-03/end=Tomorrow%20is%20May%204,%202019 <br/>"
        f"</blockquote/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    results = db_session.query(Measurement.date, Measurement.prcp).all()

    prcp_dict = {}

    for date, prcp in results:
        if date not in prcp_dict:
            # the first time this date is encountered
            prcp_dict[date] = [prcp]
        else:
            # we have already seen this date - append the new prcp amount to the existing list
            prcp_dict[date].append(prcp)
        
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations."""
    # Query all stations - use the station table
    # We could also ask for the list of distinct stations in the measurement table
    results = db_session.query(Station.station, Station.name).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """
    Return the prior 12 months of temperature observations from the last
    available date in the database.
    """
    last_date = db_session.query(func.max(Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)
    one_year_ago_str = one_year_ago.strftime("%Y-%m-%d")

    results = db_session.query(
        Measurement.date,
        Measurement.tobs
        ).filter(Measurement.date >= one_year_ago_str).all()
    
    # Create a dictionary from the row data and append to a list of temperatures
    temperatures = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temperatures.append(temp_dict)

    return jsonify(temperatures)


@app.route("/api/v1.0/<start>")
def temperature_summary_from(start):
    """Return a list of the minimum temperature, the average temperature, and 
    the max temperature for all dates greater than the given start date.
    At the moment it does not raise an error if the date is not in the database."""
    
    # Try to parse the date:
    try:
        parsed = parse(start, fuzzy_with_tokens=True)
    except ValueError:
        return jsonify({"error": f"{start} does not contain a recognized date format."}), 404
    else:
        parsed_start = parsed[0].strftime("%Y-%m-%d")

    results = db_session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
        ).filter(Measurement.date >= parsed_start).all()

    temp_summary = list(np.ravel(results))

    return(jsonify(temp_summary))

@app.route("/api/v1.0/<start>/<end>")
def temperature_summary_from_to(start, end):
    """Return a list of the minimum temperature, the average temperature, and 
    the max temperature for all dates between the given start and end dates, inclusive.
    At the moment it does not raise an error if the dates are not in the database."""
    
    # Check that start, end are valid dates.
    # Try to parse the dates:
    try:
        parsed = parse(start, fuzzy_with_tokens=True)
    except ValueError:
        return jsonify({"error": f"The argument start {start} does not contain a recognized date format."}), 404
    else:
        parsed_start = parsed[0].strftime("%Y-%m-%d")

    try:
        parsed = parse(end, fuzzy_with_tokens=True)
    except ValueError:
        return jsonify({"error": f"The argument end {end} does not contain a recognized date format."}), 404
    else:
        parsed_end = parsed[0].strftime("%Y-%m-%d")

    results = db_session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
        ).filter(Measurement.date >= parsed_start).filter(Measurement.date <= parsed_end).all()

    temp_summary = list(np.ravel(results))

    return(jsonify(temp_summary))

# Adding this - DL
@app.teardown_appcontext
def cleanup(resp_or_exc):
    print('Teardown received')
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
