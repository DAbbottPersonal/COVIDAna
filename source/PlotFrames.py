#######################################
### Common plotting scripts ###########
#######################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def label_points(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.03, point['y'], str(point['val']))

def plot_rates(countries_to_study, time_period, suffix=""):
    day_gap = 7
    time_period = 120
    PU = 1E3 # population units are in thousands
    #country = args.country
    country = "US"
    deaths = {"deaths":{}, "DPC":{}}
    populations = {}
    frame_results = {}
    for country in countries_to_study:
        #deaths[country] = {"deaths":[], "DPC":[]}
        deaths["deaths"][country] = []
        deaths["DPC"][country]    = []
        for day in range(day_gap, day_gap+time_period):
            frame = organize_covid_frame(country, day, by="country")
            if country not in populations:
                populations[country] = frame['PopTotal']
            cur_deaths = frame['Deaths'].sum() 
            deaths["deaths"][country].append( cur_deaths )            
            deaths["DPC"][country].append( cur_deaths/(populations[country]/1000.0) )

    frame_results["DPC"] = pd.DataFrame(data=deaths["DPC"])
    frame_results["DPC"] = frame_results["DPC"].iloc[::-1]
    print (frame_results["DPC"].head())

    frame_results["deaths"] = pd.DataFrame(data=deaths["deaths"])
    frame_results["deaths"] = frame_results["deaths"].iloc[::-1]
    print (frame_results["deaths"].head())

    #print (populations)
    #print (deaths)



    # Append on deaths per capita
    #frames["DeathsPerCapita"] = frames.apply(lambda row: row.Deaths/row.PopTotal, axis=1)
    #average_DeathsPerCapita   = frames["DeathsPerCapita"].agg("mean")

    if suffix == "":
        suffix = ".png"
    else:
        suffix = ''.join(["_",suffix,".png"])
    plots = {}
    plots["DPC"] = sns.lineplot(data=frame_results["DPC"])
    plots["DPC"].set_xlim(time_period, 0)
    plots["DPC"].grid(True)
    plots["DPC"].set(title='Deaths Per Capita', xlabel="Time [days]", ylabel="Deaths/Capita x1E3")
    #plots["DPC"].plot()
    plots["DPC"].figure.savefig("deaths_per_capita"+suffix)
    plt.close()

    plots["deaths"] = sns.lineplot(data=frame_results["deaths"])
    plots["deaths"].set_xlim(time_period, 0)
    plots["deaths"].grid(True)
    plots["deaths"].set(title='Total Deaths', xlabel="Time [days]", ylabel="Deaths")
    #plots["deaths"].plot()
    plots["deaths"].figure.savefig("deaths"+suffix)
    plt.close()

def plot_rates_by_gdp(countries_to_study, days_ago=7, suffix=""):
    PU = 1E3 # population units are in thousands
    today = date_as_str(day="today", style="EU" )
    #country = args.country
    country = "US"
    stats = {"GDP":[], "deaths":[], "DPC":[]}
    populations = {}
    frame_results = {}
    if suffix != "":
        suffix = "_"+suffix
    for country in countries_to_study:
        print ("Now Running Country: " + country)
        frame = organize_frame(country, days_ago, by="country")
        if country not in populations:
            populations[country] = frame['PopTotal']
        cur_deaths = frame['Deaths'].sum() 
        stats["GDP"].append( frame["GDP"] )
        # GDP already in per capita! May add more metrics in the future
        # stats["GDPPC"].append( frame["GDP"]/(populations[country]/1000.0) )
        stats["deaths"].append( cur_deaths )            
        stats["DPC"].append( cur_deaths/(populations[country]/1000.0) )

    frame_results = pd.DataFrame(data=stats, index=countries_to_study)
    #frame_results = frame_results["DPC"].iloc[::-1]
    print (frame_results)

    plots = {}
    plots["per_capita"] = sns.lmplot(x="GDP", y="DPC", data=frame_results)
    #plots["per_capita"].set_xlim(time_period, 0)
    #plots["per_capita"].grid(True)
    plots["per_capita"].set(title=today, xlabel="GDP/population [USD]", ylabel="total COVID deaths/population")
    #plots["deaths"].plot()
    label_points( frame_results["GDP"], frame_results["DPC"], frame_results.index.to_series(), plt.gca()) 
    plots["per_capita"].savefig("GDP_vs_deaths_percapita"+suffix)
    plt.close()
   

    plots["total"] = sns.lmplot(x="GDP", y="deaths", data=frame_results)
    #plots["per_capita"].set_xlim(time_period, 0)
    #plots["total"].grid(True)
    plots["total"].set(title=today, xlabel="GDP [USD]", ylabel="deaths")
    #plots["deaths"].plot()
    label_points( frame_results["GDP"], frame_results["deaths"], frame_results.index.to_series(), plt.gca()) 
    plots["total"].savefig("GDP_vs_deaths"+suffix)
    plt.close()

