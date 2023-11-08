# sqlalchemy-challenge
Module 10 Challenge (SQLAlchemy) - Wassim Deen

# Summary of Challenge
- Analyse and Explore Climate Data (Jupyter Notebook / SQLAlchemy)
    1. Jupyter Notebook Database Connection
        - Use the SQLAlchemy `create_engine()` function to connect to my SQLite database
        - Use the SQLAlchemy `automap_base()` function to reflect my tables into ORM classes
        - Save references to the classes named `station` and `measurement`
        - Link Python to the SQLite database by creating an SQLAlchemy session
        - Close your session at the end of my notebook

    2. Precipitation Analysis
        - Create a query that finds the most recent `date` in the dataset
        - Create a query that collects only the `date` and `precipitation` for the last year of data
        - Save the query results to a Pandas DataFrame to create `date` and `precipitation` columns (`prcp_df`)
        - Sort the DataFrame by `date`
        - Plot the results by using Matplotlib with `date` as the x and `precipitation` as the y variables
        - Use Pandas to print the summary statistics for the precipitation data

    3. Station Analysis
        - Design a query that correctly finds the number of stations in the dataset
        - Design a query that correctly lists the stations and observation counts in descending order and finds the most active station
        - Design a query that correctly finds the min, max, and average temperatures for the most active station
        - Design a query to get the previous 12 months of temperature observation (`tobs`) data that filters by the station that has the greatest number of observations
        - Save the query results to a Pandas DataFrame (`tobs_df`)
        - Plot a Matplotlib histogram with `bins=12` for the last year of data using `tobs` as the column to count.

- Design Climate App (Flask API / SQLAlchemy)
    1. API SQLite Connection & Landing Page
        - Correctly generate the engine to the correct sqlite file
        - Use `automap_base()` function to reflect my tables into ORM classes
        - Save references to the classes named `station` and `measurement`
        - Correctly create & bind the session between the Python app and the SQLite database
        - Display all available routes on the landing (home) page

    2. API Static Routes
        - Precipitation Route (`"/api/v1.0/precipitation"`)
            1. Returns json with the date as the key and the value as the precipitation
            2. Only returns the jsonified precipitation data for the last year in the database

        - Stations Route (`"/api/v1.0/stations"`)
            1. Returns jsonified data of all of the stations in the database

        - Temperature (tobs) Route (`"/api/v1.0/tobs"`)
            1. Returns jsonified data for the most active station (USC00519281)
            2. Only returns the jsonified data for the last year of data 

    3. API Dynamic Routes
        - Start Route (`"/api/v1.0/<start_date>"`)
            1. Accepts the start date as a parameter from the URL
            2. Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset

        - Start/End Route (`"/api/v1.0/<start_date>/<end_date>"`)
            1. Accepts the start and end dates as parameters from the URL
            2. Returns the min, max, and average temperatures calculated from the given start date to the given end date


# Notes
1. CSV files used only as reference to look at the data stored in the SQLite Database (date format not 1:1)


# Final Repository Structure
```
├── README.md
└── SurfsUp
    ├── climate_analysis.ipynb
    ├── app.py
    └── Resources
        ├── hawaii.sqlite
        ├── hawaii_measurements.csv
        ├── hawaii_stations.csv

```
