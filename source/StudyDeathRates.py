import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from OrganizeFrames import organize_covid_frame

days_back = 3

countries_to_study = ["US", "Germany", "France", "Italy", "India", "Brazil", "Japan", "Canada"]

# Get all the dataframes
frames = []
for country in countries_to_study:
    frames.append(organize_covid_frame(country, days_back, by="country"))

frames = pd.DataFrame(frames)


day_gap = 7
PU = 1E3 # population units are in thousands
country = args.country

frames = []
deaths = []
populations = []
for day in range(day_gap, day_gap+args.time):
    frame = organize_frame(country, day, by="country")
    deaths.append( frame['Deaths'].sum() )
    populations.append( frame['PopTotal'] )




# Append on deaths per capita
frames["DeathsPerCapita"] = frames.apply(lambda row: row.Deaths/row.PopTotal, axis=1)
average_DeathsPerCapita   = frames["DeathsPerCapita"].agg("mean")

print(frames.head())

sns.

