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

**JUNE AND DECEMBER DESCRIPTIVE STATISTICS

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/2b778317b71460ce57f4498f934cbcf46dc7dd05/Readme_Images/descriptive_stats.png)

In this repository...

Three key differences in weather between June and December are:

  * June's mean temperature is 5.35% higher on average compared to December's mean temperature
  * 
  * 3

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/97e294dc6d8400f231de3b9a215c6ee54ea6b3c3/Readme_Images/temp_plots.png)

**URL ROUTES**

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/precipitation_route.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/stations_route.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/temp_observations_route.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/min_avg_max_temp_measurements_route.png)

## SUMMARY

### 

Summary of the results and two additional queries to perform to gather more weather data for June and December
