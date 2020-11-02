import requests

from os import getenv

print ("Updating populations.")
dls = "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv" 
csv = requests.get(dls)

repo_dir = getenv('DABBOTTCOVID')
f = open(repo_dir+"/data/CountryData.csv", 'wb')
f.write(csv.content)
f.close()
print ("Done.")
