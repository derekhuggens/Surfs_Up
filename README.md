# Surfs_Up
### Advanced data storage with SQLite, SQLAlchemy, and Flask

## Overview of the Analysis
###
In this repository, SQLite, SQLAlchemy, and Flask were studied and used for gathering and analyzing weather data to justify a business model.

SQLite is a small, fast, relational database management system that can be stored locally for quick testing. SQLAlchemy is a query tool that can query SQLite databases. Flask is a web development framework that uses Python to build websites.

SQLite files are cross-platform, flat files used widely as a reliable, durable storage fornat. SQLAlchemy is built upon two APIs known as the Core and the ORM (Object Relational Mapper) that establish database connectivity and configurable layers for users to define Python classes, respectively.[^1]

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/65d83f91763b4bccd83673c978db17b6543001a5/Readme_Images/sqla_arch_small.png)
[^1]: Reference: https://docs.sqlalchemy.org/en/14/intro.html

Using the SQLAlchemy toolkit and Object Relational Mapper, we used Python to query a SQLite file containing weather station data in Hawaii. 

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


## Results

### 

In this repository...

Three key differences in weather between June and December are:

  * 1
  * 2
  * 3

JUNE  DESCRIPTIVE STATISTICS

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/June_Temperatures.png)

DECEMBER DESCRIPTIVE STATISTICS

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/December_Temperatures.png)

URL ROUTES

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/precipitation_route.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/stations_route.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/temp_observations_route.png)

![This is an image](https://github.com/derekhuggens/Surfs_Up/blob/f8f66c58d51ddbdbfc1d9cf1e06a1cdfbf185962/Readme_Images/min_avg_max_temp_measurements_route.png)

## SUMMARY

### 

Summary of the results and two additional queries to perform to gather more weather data for June and December
