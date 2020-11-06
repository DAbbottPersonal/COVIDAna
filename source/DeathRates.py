import argparse
import pandas as pd
import matplotlib.pyplot as plt

from OrganizeFrames import organize_frame
from datetime import date, datetime, timedelta
from scipy.interpolate import BSpline

def rebin( graph, scale ):
    if not isinstance(scale, int):
        print ("WARNING you can only rebin with integers. Exiting.")
        return 0
    if scale < 1:
        print ("WARNING you must rescale by a number >=1. Exiting.")
        return 0
    x, y = [], []
    for cur_bin in range(0,len(graph)-scale+1, scale):
        #print (cur_bin)
        ave_x = cur_bin+scale/2
        x.append(ave_x)
        print (ave_x)
        ave_y = 0
        for y_iter in range(cur_bin, cur_bin+scale+1):
            ave_y += graph[y_iter]
        ave_y /= scale
        y.append( graph[cur_bin])

    return [x,y]
do_smooth=False

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

print (deaths)
death_types_dict = {"Cumulative":[],
                     "PerCapita":[],
                     "Daily":[],
                     "Daily_PerCapita":[]}
death_types = ["Cumulative", "PerCapita", "Daily", "Daily_PerCapita"]
for index in range( 0, len(deaths)-1):
    death_types_dict["Cumulative"].append(deaths[index]-deaths[-1])
    death_types_dict["PerCapita"].append((deaths[index]-deaths[-1]) / populations[index])
    death_types_dict["Daily"].append(deaths[index]-deaths[index+1])
    death_types_dict["Daily_PerCapita"].append((deaths[index]-deaths[index+1]) / populations[index])

frame_result = pd.DataFrame(data=death_types_dict)
frame_result_oriented = frame_result.iloc[::-1]
print (frame_result.head())

if not args.skipPlots:
    print ("Done.")
    exit()
else: 
    print ("Beginning Plotting.")

# Get "calendar" style days for labels on plots
#l_days = []
#l_ticks = []
#for day in range(0,frame_result.shape[0], 4):# int(frame_result.shape[0]/7)+1 ):
#    print (day)
#    l_days.append( (today-timedelta(days=day)).strftime('%a %m/%d') )
#print (l_days)

for cur_type in death_types:
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    reb_result = rebin(frame_result_oriented[cur_type], 7)
    #ax.plot(frame_result_oriented[cur_type])
    ax.plot(reb_result[0], reb_result[1])
    ax.set_xlim(frame_result.shape[0], 0)
    ax.grid(True)
    ax.set(title=' '.join([country, cur_type]), xlabel="Time [days]", ylabel="Deaths")
   
    if do_smooth:
        smooth = BSpline( range(len(frame_result_oriented[cur_type])), list(frame_result_oriented[cur_type]), 1)
        smooth_x = range(len(frame_result_oriented[cur_type]))
        smooth_y = []
        for x in range(len(frame_result_oriented[cur_type])-1, -1, -1):
            smooth_y.append( int(smooth(x)) )

        ax.plot(smooth_x, smooth_y)

    plt.savefig( '_'.join([country,cur_type,"Deaths.png"]) )



print ("Done.")
