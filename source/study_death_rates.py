'''
Script to steer advanced plotting of death rates for countries.
'''

from json import load
from plot_frames import label_points, plot_rates, plot_rates_by_gdp, plot_latest_trend


#######################################
### Main code starts here #############
#######################################

random_mix = ["US", "Germany", "France", "Italy", "India", "Brazil", "Japan", "Canada", "Mexico", "Thailand"]
top_gdppc = ["Switzerland", "Ireland", "Norway", "US", "Singapore", "Denmark", "Australia", "Netherlands", "Sweden", "Austria", "Finland", "Germany"]
with open("../data/CountryLists.json") as f:
    countries = load(f)

time_period = 180 #days 

# Deaths over time line plots
#plot_rates(random_mix, time_period, suffix="")
#plot_rates(top_gdppc, time_period, suffix="topgdp")
#plot_rates(countries["eu_countries"], time_period, suffix="eu")

# GDP scatterplots
#plot_rates_by_gdp(random_mix)
#plot_rates_by_gdp(countries["all_countries"])
#plot_rates_by_gdp(countries["eu_countries"], suffix="eu")

plot_latest_trend(random_mix, suffix="test")
plot_latest_trend(top_gdppc, suffix="topgdppc")
