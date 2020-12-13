import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from OrganizeFrames import organize_covid_frame

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

    plots["deaths"] = sns.lineplot(data=frame_results["deaths"])
    plots["deaths"].set_xlim(time_period, 0)
    plots["deaths"].grid(True)
    plots["deaths"].set(title='Total Deaths', xlabel="Time [days]", ylabel="Deaths")
    #plots["deaths"].plot()
    plots["deaths"].figure.savefig("deaths"+suffix)


#######################################
### Main code starts here #############
#######################################

random_mix = ["US", "Germany", "France", "Italy", "India", "Brazil", "Japan", "Canada", "Mexico", "Thailand"]
top_gdppc = ["Switzerland", "Ireland", "Norway", "US", "Singapore", "Denmark", "Australia", "Netherlands", "Sweden", "Austria", "Finland", "Germany"]
friends = ["Finland", "Georgia", "Italy", "US", "Switzerland"]

#plot_rates(random_mix, 180, suffix="")
#plot_rates(top_gdppc, 180, suffix="topgdp")
plot_rates(friends, 180, suffix="friends")

