import os
import argparse
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt

def organize_frame ( country='US', day='today', by = "" ):
    data_path = '../data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
    cov_dates = set(os.listdir(data_path))
    latest_date = find_latest_date(cov_dates)
    days_behind = date.today() - latest_date 
    doi = None # Short for date of interest!
    yoi = None
    if days_behind.days >= 7:
        print ("WARNING: COVID data is older than a week. Please update from the repository!")
    if day == "latest":
        doi = date_as_str(days_behind.days)
    else: 
        doi = date_as_str(day)
    yoi = doi.split("-")[2]

    PU = 1E3 # population units are in thousands
    # Get COVID information about the country.
    frames = {}
    frames["COVID"] = pd.read_csv(''.join([data_path, doi,'.csv']))
    frames["COVID"] = frames["COVID"][frames["COVID"]['Country_Region'] == country]
    # Get general information about the country.
    UN_name = convert_UN_name(country)
    frames["general"] = pd.read_csv("../data/CountryData.csv")
    frames["general"] = frames["general"][frames["general"]["Location"] == UN_name]
    if day == "latest":
        frames["general"] = frames["general"][frames["general"]["Time"] == int(yoi)]
    
    # Get economy information about the country.
    frames['economy'] = {}
    frames['economy']['GDP'] = pd.read_csv("../data/GDPData.csv", encoding = "ISO-8859-1")
    frames['economy']['GDP'] = frames['economy']['GDP'][frames['economy']['GDP']['country'] == UN_name]

    frames['economy']['GVA'] = pd.read_csv("../data/GVAData.csv", encoding = "ISO-8859-1")
    frames['economy']['GVA'] = frames['economy']['GVA'][frames['economy']['GVA']['country'] == UN_name]

    # Get Eductation information about the country.
    frames['education'] = pd.read_csv("../data/EducationData.csv", encoding = "ISO-8859-1")
    frames['education'] = frames['education'][frames['education']['country'] == UN_name]

    if by == "country": 
        frames["COVID"] = frames["COVID"].drop(columns = ["FIPS", "Last_Update", "Admin2", "Province_State", "Combined_Key" ])
        location = frames["COVID"][["Lat", "Long_"]]
        frames["COVID"] = frames["COVID"].drop(columns = ["Lat", "Long_"])
        frames["COVID"] = frames["COVID"].agg("sum")
        location = location.agg("mean")
        frames["COVID"]["Country_Region"] = country
        frames["COVID"] = frames["COVID"].append(location)
        frames["COVID"] = append_populations(frames["COVID"], frames["general"])
        frames["COVID"] = append_date(frames["COVID"],doi)
        frames["COVID"] = append_eco(frames["COVID"], frames["economy"])
        frames["COVID"] = append_edu(frames["COVID"], frames["education"])

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
            frames["states"][cur_state] = append_date(frames["states"][cur_state], doi)
            frames["states"][cur_state] = append_eco(frames["states"][cur_state], frames["economy"])
            frames["states"][cur_state] = append_edu(frames["states"][cur_state], frames["education"])
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

def find_latest_date ( dates ):
    max_year  = 1900
    max_day   = -99
    max_month = -99
    for d in dates:
        d = d.strip(".csv")
        d = d.split("-")
        if len(d) < 2: continue
        if int(d[2]) > max_year: max_year = int(d[2])

    for d in dates:
        d = d.strip(".csv")
        d = d.split("-")
        if len(d) < 2: continue
        if int(d[0]) > max_month: max_month = int(d[0])

    for d in dates:
        d = d.strip(".csv")
        d = d.split("-")
        if len(d) < 2: continue
        if int(d[1]) > max_day: max_day = int(d[1])

    return date(max_year, max_month, max_day)

# Handle missing data -- return np.nan 
def check_frame( frame ):
    if frame.empty:
        print ("Frame is empty :: " + frame.name)
        print ("Will be filled with NaN")
        return np.nan
    return frame.iloc[0]
    
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
    frame["GDP"] = check_frame( latest_eco["value"] ).replace(',', '')
    
    latest_eco = economy["GVA"][ economy["GVA"]["year"] == economy["GVA"]["year"].max()]
    agriculture = latest_eco[ latest_eco["series"] == "Agriculture, hunting, forestry and fishing (% of gross value added)"]
    frame["agriculture"] = check_frame( agriculture["value"] )
    industry = latest_eco[ latest_eco["series"] == "Industry (% of gross value added)"]
    frame["industry"] = check_frame( industry["value"] )
    services = latest_eco[ latest_eco["series"] == "Services (% of gross value added)"]
    frame["services"] = check_frame( services["value"] )

    return frame


# NOTE: The male col has a typo of "enrollement" -- perhaps a french typo? :D
def append_edu( frame, education ): 
    latest_edu = education[ education["year"] == education["year"].max()]
    prim_enroll_fem  = latest_edu[ latest_edu["series"] == "Gross enrollment ratio - Primary (female)"]
    frame["prim_edu_fem"] = check_frame( prim_enroll_fem["value"] )
    prim_enroll_male = latest_edu[ latest_edu["series"] == "Gross enrollement ratio - Primary (male)"]
    frame["prim_edu_male"] = check_frame( prim_enroll_male["value"] )

    seco_enroll_fem  = latest_edu[ latest_edu["series"] == "Gross enrollment ratio - Secondary (female)"]
    frame["seco_edu_fem"] = check_frame( seco_enroll_fem["value"] )
    seco_enroll_male = latest_edu[ latest_edu["series"] == "Gross enrollment ratio - Secondary (male)"]
    frame["seco_edu_male"] = check_frame( seco_enroll_male["value"] )
  
    tert_enroll_fem  = latest_edu[ latest_edu["series"] == "Gross enrollment ratio - Tertiary (female)"]
    frame["tert_edu_fem"] = check_frame( tert_enroll_fem["value"] )
    tert_enroll_male = latest_edu[ latest_edu["series"] == "Gross enrollment ratio - Tertiary (male)"]
    frame["tert_edu_male"] = check_frame( tert_enroll_male["value"] )


    return frame












