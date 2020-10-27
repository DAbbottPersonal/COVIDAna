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
    frames["general"] = frames["general"][frames["general"]["Time"] == date_as_date(day).year]
    
    # Get COVID information about the country.
    frames["COVID"] = pd.read_csv(''.join([data_path, date,'.csv']))
    frames["COVID"] = frames["COVID"][frames["COVID"]['Country_Region'] == country]

    # Get economy information about the country.
    frames['economy'] = {}
    frames['economy']['GDP'] = pd.read_csv("../data/GDPData.csv", encoding = "ISO-8859-1")
    frames['economy']['GDP'] = frames['economy']['GDP'][frames['economy']['GDP']['country'] == UN_name]

    frames['economy']['GVA'] = pd.read_csv("../data/GVAData.csv", encoding = "ISO-8859-1")
    frames['economy']['GVA'] = frames['economy']['GVA'][frames['economy']['GVA']['country'] == UN_name]


    if by == "country": 
        frames["COVID"] = frames["COVID"].drop(columns = ["FIPS", "Last_Update", "Admin2", "Province_State", "Combined_Key" ])
        location = frames["COVID"][["Lat", "Long_"]]
        frames["COVID"] = frames["COVID"].drop(columns = ["Lat", "Long_"])
        frames["COVID"] = frames["COVID"].agg("sum")
        location = location.agg("mean")
        frames["COVID"]["Country_Region"] = country
        frames["COVID"] = frames["COVID"].append(location)
        frames["COVID"] = append_populations(frames["COVID"], frames["general"])
        frames["COVID"] = append_date(frames["COVID"],date)
        frames["COVID"] = append_eco(frames["COVID"], frames["economy"])

# State by-state is going to takes some more sensitive care with population. A WIP.
    if by == "state":
        frames["COVID"] = frames["COVID"].drop(columns = ["FIPS", "Last_Update", "Admin2", "Combined_Key" ])
        frames["states"] = {}
        for cur_state in frames["COVID"]["Province_State"]:
            
            frames["states"][cur_state] = frames["COVID"][frames["COVID"]["Province_State"]==cur_state]
            location = frames["states"][cur_state][["Lat", "Long_" ]]
            frames["states"][cur_state] = frames["states"][cur_state].drop(columns = ["Lat", "Long_"])

            frames["states"][cur_state] = frames["states"][cur_state].agg("sum")
            location = location.agg("mean")

            
            frames["states"][cur_state]["Province_State"] = cur_state
            frames["states"][cur_state]["Country_Region"] = country
            frames["states"][cur_state] = frames["states"][cur_state].append(location)
            frames["states"][cur_state] = append_populations(frames["states"][cur_state], frames["general"])
            frames["states"][cur_state] = append_date(frames["states"][cur_state], date)
            frames["states"][cur_state] = append_eco(frames["states"][cur_state], frames["economy"])
            #frames["states"][cur_state] = append_location(frames["states"][cur_state],

        frames["COVID"] = pd.DataFrame(frames["states"])
    else:
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
def date_as_str ( day = "today" ):
    t_date = date.today()-timedelta(days=1)
    if day == "today":
        return t_date.strftime('%m-%d-%Y')    
    elif day < 1:
        print ("Error, minimum day should be 1 or more. Returning None!")
        return None
    t_date = date.today()-timedelta(days=day)
    return t_date.strftime('%m-%d-%Y')

def date_as_date ( day = "today" ):
    t_date = date.today()-timedelta(days=1)
    if day == "today":
        return t_date.strftime('%m-%d-%Y')    
    elif day < 1:
        print ("Error, minimum day should be 1 or more. Returning None!")
        return None
    t_date = date.today()-timedelta(days=day)
    return t_date
 
    
def append_populations( covid_frame, pop_frame ):
    PU = 1E3 # population units are in thousands
    # Append some population information onto the COVID information
    for pop_titles in ["PopTotal", "PopMale", "PopFemale", "PopDensity"]:
        covid_frame[pop_titles] = pop_frame.iloc[0][pop_titles]*PU

    return covid_frame
    
def append_date( frame, date ):
    frame["date"] = date

    return frame

def append_eco( frame, economy ): 
    latest_eco = economy["GDP"][ economy["GDP"]["series"] == "GDP per capita (US dollars)"]
    latest_eco = latest_eco[ latest_eco["year"] == latest_eco["year"].max()]
    frame["GDP"] = latest_eco["value"].iloc[0]

    latest_eco = economy["GVA"][ economy["GVA"]["year"] == economy["GVA"]["year"].max()]
    agriculture = latest_eco[ latest_eco["series"] == "Agriculture, hunting, forestry and fishing (% of gross value added)"]
    frame["argiculture"] = agriculture["value"].iloc[0]
    industry = latest_eco[ latest_eco["series"] == "Industry (% of gross value added)"]
    frame["industry"] = industry["value"].iloc[0]
    services = latest_eco[ latest_eco["series"] == "Services (% of gross value added)"]
    frame["services"] = services["value"].iloc[0]

    return frame
