import os
import argparse
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt

def organize_frame ( country='US', day='today', by = "" ):
    data_path = '../data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
    PU = 1E3 # population units are in thousands
    date = date_as_str(day)

    # Get general information about the country.
    UN_name = convert_UN_name(country)
    frames = {}
    frames["general"] = pd.read_csv("../data/CountryData.csv")
    frames["general"] = frames["general"][frames["general"]["Location"] == UN_name]
        # Get COVID information about the country.
    frames["COVID"] = pd.read_csv(''.join([data_path, date,'.csv']))
    frames["COVID"] = frames["COVID"][frames["COVID"]['Country_Region'] == country]

    if by == "country": 
        frames["COVID"] = frames["COVID"].drop(columns = ["FIPS", "Admin2", "Province_State", "Lat", "Long_", "Combined_Key" ]).agg("sum")
        #frames["COVID"].agg("sum")
    if by == "state":
        frames["COVID"] = frames["COVID"].drop(columns = ["FIPS", "Admin2", "Lat", "Long_", "Combined_Key" ])
        frames["COVID"].sum(level="Province_State")

    # Append some population information onto the COVID information
    for pop_titles in ["PopTotal", "PopMale", "PopFemale", "PopDensity"]:
        frames["COVID"][pop_titles] = frames["general"].iloc[0][pop_titles]*PU
    frames["COVID"]["date"] = date    

    # Some cleanup then ready to return.
    frames["COVID"].rename(index={0:country})

    return frames["COVID"]

# To handle country names that are spelled unique.
def convert_UN_name( country ):
    d_un_names = {"US":"United States of America",
                  "Palestine":"State of Palestine",
                  "Iran":"Iran (Islamic Republic of)"}

    if country not in d_un_names:
        return country

    return d_un_names[country]


# Default is "today", which is really yesterday as the data collection lags a day.
# Otherwise, it is how many days ago.
def date_as_str (day = "today"):
    t_date = date.today()-timedelta(days=1)
    if day == "today":
        return t_date.strftime('%m-%d-%Y')    
    elif day < 1:
        print ("Error, minimum day should be 1 or more. Returning None!")
        return None
    t_date = date.today()-timedelta(days=day)
    return t_date.strftime('%m-%d-%Y')
    
