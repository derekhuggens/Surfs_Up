# Surfs_Up
### Advanced data storage with SQLite, SQLAlchemy, and Flask

## Overview of the Analysis
###
In this repository, SQLite, SQLAlchemy, and Flask were studied and used for gathering and analyzing weather data (in June and December months) to justify a business model.

SQLite is a small, fast, relational database management system that can be stored locally for quick testing. SQLAlchemy is a query tool that can query SQLite databases. Flask is a web development framework that uses Python to build websites.

SQLite files are cross-platform, flat files used widely as a reliable, durable storage fornat. SQLAlchemy is built upon two APIs known as the Core and the ORM (Object Relational Mapper) that establish database connectivity and configurable layers for users to define Python classes, respectively.[^1]

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/65d83f91763b4bccd83673c978db17b6543001a5/Readme_Images/sqla_arch_small.png)
[^1]: Reference: https://docs.sqlalchemy.org/en/14/intro.html

Using the SQLAlchemy toolkit and Object Relational Mapper, we used Python to query a SQLite file containing weather station data in Hawaii. The following dependencies were used.

``` Jupyter Notebook
# Dependencies
import numpy as np
import pandas as pd
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
```

In short, an object known as `Engine` was declared to connect our SQLite database for querying as such: `engine = create_engine("sqlite:///hawaii.sqlite")`.  The SQLite file `hawaii.sqlite` database was automapped into a new model using `automap_base()` as `Base = automap_base()` and then the base class schema was reflected with mappings with `Base.prepare(engine, reflect=True)`. The classes that were mapped for our interest were saved in variables with logically matching table names for reference: `Measurement = Base.classes.measurement` `Station = Base.classes.station`. Finally, `session = Session(engine)` creates the link from Python to the database. Below, our hawaii.sqlite database can be seen with two tables, measurement and station.

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/6cb427b7faaf1d983a3a4aa0ed31716195bbaffa/Readme_Images/sqlite_file.png)


In order to pull the requested weather data from the database the `sqlalchemy` module `extract` was imported: `from sqlalchemy import extract`.

`session.query` and `.filter` were used as well as `.all()` to pull appropriate temperatures from June and December, respectively, from the Measurement table:

`june_results = session.query(Measurement.tobs).filter(extract('month', Measurement.date)==6).all()`

`dec_results = session.query(Measurement.tobs).filter(extract('month', Measurement.date)==12).all()`

The resulting objects were converted to a list using `list()` and the numpy function `np.ravel`:

`june_temps = list(np.ravel(june_results))`

`dec_temps = list(np.ravel(dec_results))`

To view the lists in a table we converted the lists to DataFrames with new column names using `pd.Dataframe` and `columns=[]`:

`june_df = pd.DataFrame(june_temps, columns=['June Temperatures'])`

`dec_df = pd.DataFrame(dec_temps, columns=['December Temperatures'])`

Finally, descriptive statistics were requested from the dataframes as seen in the Results section of this `README`.

## Results

Three key differences in weather observations between June and December are:

  * June's mean temperature is 5.35% higher on average compared to December's mean temperature
  * There is no skew in the data as the mean temperatures sit with the 50% percentile or median.
  * December's minimum temperature measures 8 degrees Fahrenheit colder than June's minimum.

**JUNE AND DECEMBER DESCRIPTIVE STATISTICS**

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/2b778317b71460ce57f4498f934cbcf46dc7dd05/Readme_Images/descriptive_stats.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/97e294dc6d8400f231de3b9a215c6ee54ea6b3c3/Readme_Images/temp_plots.png)

**FLASK**

Flask was used to present the Hawaii data within four different webpages. Within Flask, `@app.route("/")` was used as the welcome/home page to then create four different `@app.route()` paths that someone could click on to view various Hawaii database data.

```python
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
```

I was not happy with the original f-string Python text used to create the landing page, so I imported `from flask import render_template` and created an HTML file titled `template.html` in a folder titled "templates" within the same directory as the Flask python file `app.py`. Below is the HTML code for the new landing page with the more interactive HTML links using `<a href="url">link text</a>`.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Flask Template Example</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <style type="text/css">
      .container {
        max-width: 500px;
        padding-top: 100px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <p>Welcome to the Hawaii Climate Analysis API!</p>
      <p>Available Routes</p>
      <p> <a href="http://127.0.0.1:5000/api/v1.0/precipitation">/api/v1.0/precipitation</a></p>
      <p> <a href="http://127.0.0.1:5000/api/v1.0/stations">/api/v1.0/stations</a></p>
      <p> <a href="http://127.0.0.1:5000/api/v1.0/tobs">/api/v1.0/tobs</a></p>
      <p> <a href="http://127.0.0.1:5000/api/v1.0/temp/start/end">/api/v1.0/temp/start/end</a></p>
    </div>
    <script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
  </body>
</html>
```

**URL ROUTES**

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/precipitation_route.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/stations_route.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/temp_observations_route.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/min_avg_max_temp_measurements_route.png)

## SUMMARY

### 

From a business perspective, in this case, opening an ice-cream/surfing store, it would be imperative to open up a store during times of an average or higher temperature with a lower than average amount of precipitation. The image below shows the precipitation in Hawaii for the past 12 months. I would 

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/a535ab99a84fc843dc7c339635883640f57b7c3b/Readme_Images/prcp.png)

* Query 1

Of the 1700 measurements taken in June by the weather stations (See "Count" from June descriptive statistics), 565 of the measurements were below the year round average temperature for all stations.

Query for all temperature measurements: 
`session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).all()`

Output: `[(53.0, 87.0, 73.09795396419437)]`

The year round average temperature is 73.1 degrees Fahrenheit.

Query for  June temperature measurements and their dates that are below the year round average: 
`june_below_avg_temps = session.query(Measurement.tobs, Measurement.date).filter(extract('month', Measurement.date)==6).filter(Measurement.tobs <= 73.10).all()`

Turning this query into a DataFrame:
`
june_below_avg_temps_df = pd.DataFrame(june_below_avg_temps, columns=['temps','date'])
june_below_avg_temps_df.set_index(june_below_avg_temps_df['date'], inplace=True)
print(june_below_avg_temps_df.drop(['date'], axis=1))`

A count of measurements: `june_below_avg_temps_df.count()`

Output:

`temps 565`

`date 565`

 This can be interpreted that 33.23% of all temperature observations in June are below the year round average temperature in Hawaii, and so 66.77% of all June temperature observations are above the year round average temperature in Hawaii. June is a good month temperature wise!
 
 * Query 2

Of the 1517 measurements taken in December by the weather stations (See "Count" from December descriptive statistics), 565 of the measurements were below the year round average temperature for all stations.

Query for all temperature measurements: 
`session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).all()`

Output: `[(53.0, 87.0, 73.09795396419437)]`

The year round average temperature is 73.1 degrees Fahrenheit.

Query for  June temperature measurements and their dates that are below the year round average: 
`dec_below_avg_temps = session.query(Measurement.tobs, Measurement.date).filter(extract('month', Measurement.date)==12).filter(Measurement.tobs <= 73.10).all()`

Turning this query into a DataFrame:
`
dec_below_avg_temps_df = pd.DataFrame(dec_below_avg_temps, columns=['temps','date'])
dec_below_avg_temps_df.set_index(dec_below_avg_temps_df['date'], inplace=True)
print(dec_below_avg_temps_df.drop(['date'], axis=1))`

A count of measurements: `dec_below_avg_temps_df.count()`

Output:

`temps 1118`

`date 1118`

This can be interpreted that 73.7% of all temperature observations in December are below the year round average temperature in Hawaii, and so only 26.3% of all December temperature observations are above the year round average temperature in Hawaii. December is not a good month temperature wise!
