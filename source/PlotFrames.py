#######################################
### Common plotting scripts ###########
#######################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from datetime import date, datetime, timedelta
from itertools import cycle
from OrganizeFrames import date_as_str, organize_covid_frame, organize_frame, get_countries, find_latest_date
from os import listdir
from scipy import optimize as opt

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

def plot_latest_trend(countries_to_study, suffix=""):
    def func(x, a, b, c, d, e):
        #return (a + b*x + c*np.exp(d*x)) 
        return (a + b*x + c*x*x + d*np.exp(e*x))
    colors = color_dict(countries_to_study)
    data_path = '../data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
    cov_dates = set(listdir(data_path))
    latest_date = find_latest_date(cov_dates) 
    day_gap = (date.today() - latest_date).days
    # Typically, COVID is a 2 week period so use that trend window.
    time_period = 14
    extrap_days = 10
    PU = 1E3 # population units are in thousands
    #country = args.country
    country = "US"
    deaths = {"deaths":{}, "DPC":{}}
    populations = {}
    frame_results = {}
    if suffix != "":
        suffix = "_"+suffix
    for country in countries_to_study:
        #deaths[country] = {"deaths":[], "DPC":[]}
        deaths["deaths"][country] = []
        deaths["DPC"][country]    = []
        for day in range(day_gap+time_period, day_gap, -1):
            frame = organize_covid_frame(country, day, by="country")
            if country not in populations:
                populations[country] = frame['PopTotal']
            cur_deaths = frame['Deaths'].sum() 
            deaths["deaths"][country].append( cur_deaths )            
            deaths["DPC"][country].append( cur_deaths/(populations[country]/1000.0) )
    
        time_period_x = range(-1*time_period, 0, 1)
        print ("Fitting country " + country)
        try:
            # Try with an exponential first
            popt, pcov = opt.curve_fit(func, time_period_x, deaths["DPC"][country], bounds=([-10,-10,-10,-10,-10],[10,10,10,10,10]))
            print (popt)
        except RuntimeError:
            # Drop the exponential, virtually to zero and refit the curve
            popt, pcov = opt.curve_fit(func, time_period_x, deaths["DPC"][country], bounds=([-10,-1,-0.001,-0.001,-0.001],[10,1,0.001,0.001,0.001]))
            print ("Exception in fitting...")
            print (popt)

        plot_period_x = range(-1*time_period, extrap_days, 1)
        plt.plot(plot_period_x, func(plot_period_x, *popt), color=colors[country]['nom'], linestyle='--')
        plt.plot(time_period_x, deaths["DPC"][country], color=colors[country]['nom'], linestyle='-', label=(country))
    plt.legend()
    plt.xlim([-1*time_period, extrap_days+7])
    plt.savefig("week_projection"+suffix)
    plt.close() 

    #frame_results["DPC"] = pd.DataFrame(data=deaths["DPC"])
    #frame_results["DPC"] = frame_results["DPC"].iloc[::-1]

    #frame_results["deaths"] = pd.DataFrame(data=deaths["deaths"])
    #frame_results["deaths"] = frame_results["deaths"].iloc[::-1]



    # Append on deaths per capita
    #frames["DeathsPerCapita"] = frames.apply(lambda row: row.Deaths/row.PopTotal, axis=1)
    #average_DeathsPerCapita   = frames["DeathsPerCapita"].agg("mean")

    #if suffix == "":
    #    suffix = ".png"
    #else:
    #    suffix = ''.join(["_",suffix,".png"])
    #plots = {}
    #plots["DPC"] = sns.regplot(data=frame_results["DPC"])
    #plots["DPC"].set_xlim(time_period, 0)
    #plots["DPC"].grid(True)
    #plots["DPC"].set(title='Deaths Per Capita', xlabel="Time [days]", ylabel="Deaths/Capita x1E3")
    #plots["DPC"].figure.savefig("deaths_per_capita"+suffix)
    #plt.close()

    #plots["deaths"] = sns.regplot(data=frame_results["deaths"])
    #plots["deaths"].set_xlim(time_period, 0)
    #plots["deaths"].grid(True)
    #plots["deaths"].set(title='Total Deaths', xlabel="Time [days]", ylabel="Deaths")
    #plots["deaths"].figure.savefig("deaths"+suffix)
    #plt.close()

   
def color_dict(countries):
    colors = []
    colors.append({'nom':'black','var':'dimgray'})
    colors.append({'nom':'darkred','var':'brown'})
    colors.append({'nom':'red','var':'lightcoral'})
    colors.append({'nom':'darkorange','var':'orange'}) 
    colors.append({'nom':'goldenrod','var':'gold'}) 
    colors.append({'nom':'olive','var':'yellowgreen'}) 
    colors.append({'nom':'limegreen','var':'lime'}) 
    colors.append({'nom':'turquoise','var':'aquamarine'}) 
    colors.append({'nom':'steelblue','var':'lightslateblue'}) 
    colors.append({'nom':'navy','var':'blue'}) 
    colors.append({'nom':'rebeccapurple','var':'mediumpurple'}) 
    colors.append({'nom':'darkviolet','var':'mediumorchid'}) 
    colors.append({'nom':'indigo','var':'purple'}) 
    colors.append({'nom':'deeppink','var':'hotpink'}) 
    colors.append({'nom':'saddlebrown','var':'sandybrown'}) 
    colors.append({'nom':'darkgrey','var':'lightgrey'})
    colors.append({'nom':'black','var':'dimgray'}) 
    # Use a cycle in case we run out of colors, loop back around.
    colors = cycle(colors)

    country_colors = {}
    c_iter = 0
    for color in colors:
        country_colors[countries[c_iter]] = color
        if (countries[c_iter] == countries[len(countries)-1]):
            break
        c_iter+=1
    return country_colors


