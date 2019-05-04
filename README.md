# hawaii
Query weather observatory database via SQLAlchemy in Python.  A Flask app is also provided to query the database.


* The Jupyter notebook `dateparsing.ipynb` gives examples of using the `dateutil.parser.parse` 
function to produce ISO 8601 dates YYYY-MM-DD.  
* `stations.ipynb` explores the range of available dates in the database 
for the various stations and the effect of querying for dates with different formats (`datetime` objects versus dates as
strings).
* `app.py` is the code for the Flask app to query the database.  We have incorporated the `dateutil.parser.parse` function 
to allow for flexible entry of dates.   Queries using dates outside the range of the datebase do not produce errors at this time.
If a queried date falls outside of the datebase range, the queries return `null` if appropriate.



