# hawaii

# Description
Query weather observatory database via SQLAlchemy in Python.  Using the query results, we analyze weather data over for a time period in the past.

A Flask app is also provided to query the database.

# Methods
1.  SQLALchemy is used to query the SQLite database of observations.  
2.  Plots are constructed with `matplotlib`.
3.  A Flask app is provided to query the database.   We utilize the fuzzy date parsing option of the 
`dateutil.parser.parse` function.  This allows us to avoid checking input dates for valid entries.

# Results
* The Jupyter notebook `hawaii.ipynb` contains the results of querying the database.  [View the notebook via nbviewer](https://github.com/douglasdrake/hawaii/blob/master/hawaii.ipynb)
* The Jupyter notebook `dateparsing.ipynb` gives examples of using the `dateutil.parser.parse` 
function to produce ISO 8601 dates YYYY-MM-DD.  [View the notebook via nbviewer](https://github.com/douglasdrake/hawaii/blob/master/dateparsing.ipynb). 
* `stations.ipynb` explores the range of available dates in the database 
for the various stations and the effect of querying for dates with different formats (`datetime` objects versus dates as
strings).  [View the notebook via nbviewer](https://github.com/douglasdrake/hawaii/blob/master/stations.ipynb)
* `app.py` is the code for the Flask app to query the database.  We have incorporated the `dateutil.parser.parse` function 
to allow for flexible entry of dates.   Queries using dates outside the range of the datebase do not produce errors at this time.
If a queried date falls outside of the datebase range, the query returns `null` if appropriate.