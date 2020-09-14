import os
import argparse
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt

# Take in your desired input directory and output name
parser = argparse.ArgumentParser(description='Read out death rates due to covid19.')
parser.add_argument('-c','--country',type=str, default='US', help='Country for which you want the death rate and trends for.')
parser.add_argument('-t','--time',type=int, default=14, help='How far back do you want to examine?')
parser.add_argument('-p','--skipPlots',action='store_false', default=True, help='This flag will skip plotting.')
parser.add_argument('-o','--outfile',type=str, default='deathrates', help='Outfile name.')
args = parser.parse_args()
print ("###############################################")
print (args)
print ("###############################################")


data_path = '../data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
country = args.country
PU = 1E3 # population units are in thousands

# The most recent data is really yesterday, so subtract a day from today
today = date.today()-timedelta(days=1)
end_date   = today-timedelta(days=args.time)
# Start cur_date a day back further to get the beggining amount deaths
cur_date = today-timedelta(days=1)

# Get country data
d_pop = {}
frame = pd.read_csv("../data/CountryData.csv")
d_un_names = {"US":"United States of America",
        "Palestine":"State of Palestine",
        "Iran":"Iran (Islamic Republic of)"}
country_data = True
if country in d_un_names:
    print ("Using modified UN style name for country, ", country)
    frame = frame[frame['Location'] == d_un_names[country]]
else:
    frame = frame[frame['Location'] == country]

if frame.empty:
    print ("No country data found, proceeding without country data.")
    country_data = False

frame = frame[frame['Time'] == today.year]
d_pop["total"] = None 
if country_data == True:
    d_pop["total"] = frame.iloc[0]["PopTotal"]*PU
else:
    d_pop["total"] = 1
print (d_pop["total"])

l_deaths = []
while cur_date >= end_date:
    date_file = cur_date.strftime('%m-%d-%Y')
    csv_frame = pd.read_csv(''.join([data_path, date_file,'.csv']))
    frame = csv_frame[csv_frame['Country_Region'] == country]
    # Assume if this frame is empty that the country is actually a county or state!
    if frame.empty:
        frame = csv_frame[csv_frame['Province_State'] == country]
    deaths = frame['Deaths']
    l_deaths.append(deaths.sum())
    cur_date = cur_date - timedelta(days=1)
    
d_deaths = {"Cumulative":[],
        "PerCapita":[],
        "Daily":[],
        "Daily_PerCapita":[]}
l_death_types = ["Cumulative", "PerCapita", "Daily", "Daily_PerCapita"]
for index in range( 0, len(l_deaths)-1):
    d_deaths["Cumulative"].append(l_deaths[index]-l_deaths[-1])
    d_deaths["PerCapita"].append((l_deaths[index]-l_deaths[-1]) / d_pop["total"])
    d_deaths["Daily"].append(l_deaths[index]-l_deaths[index+1])
    d_deaths["Daily_PerCapita"].append((l_deaths[index]-l_deaths[index+1]) / d_pop["total"])

df_result = pd.DataFrame(data=d_deaths)
df_result_oriented = df_result.iloc[::-1]
print (df_result.head())

if not args.skipPlots:
    print ("Done.")
    exit()
else: 
    print ("Beginning Plotting.")

# Get "calendar" style days for labels on plots
#l_days = []
#l_ticks = []
#for day in range(0,df_result.shape[0], 4):# int(df_result.shape[0]/7)+1 ):
#    print (day)
#    l_days.append( (today-timedelta(days=day)).strftime('%a %m/%d') )
#print (l_days)

for cur_type in l_death_types:
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.plot(df_result_oriented[cur_type])
    ax.set_xlim(df_result.shape[0], 0)
    ax.grid(True)
    ax.set(title=' '.join([country, cur_type]), xlabel="Time [days]", ylabel="Deaths")
#    ax.set_xticklabels(l_days)
    plt.savefig( '_'.join([country,cur_type,"Deaths.png"]) )







print ("Done.")
