import requests

dls = "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv" 
csv = requests.get(dls)

f = open("../data/CountryData.csv", 'wb')
f.write(csv.content)
f.close()

