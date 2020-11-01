import pandas as pd

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from OrganizeFrames import organize_frame

days_back = 3

#countries_to_study = ["Austria", "Belgium", "Bulgaria", "Croatia", "Republic of Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]

countries_to_study = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]

# Get all the dataframes
frames = []
for country in countries_to_study:
    frames.append(organize_frame(country, days_back, by="country"))

frames = pd.DataFrame(frames)

# Append on deaths per capita
frames["DeathsPerCapita"] = frames.apply(lambda row: row.Deaths/row.PopTotal, axis=1)
average_DeathsPerCapita   = frames["DeathsPerCapita"].agg("mean")

target = frames.DeathsPerCapita

features = ["Incidence_Rate", "Case-Fatality_Ratio", 
            "PopDensity", 
            "GDP", "agriculture", "industry", "services",
            "prim_edu_fem", "prim_edu_male", "seco_edu_fem", "seco_edu_male", "tert_edu_fem", "tert_edu_male"]

data = frames[ features ] 

train_data, validation_data, train_target, validation_target  = train_test_split(data, target, random_state=0)

covid_model = DecisionTreeRegressor(splitter="best")
covid_model.fit(train_data, train_target)

prediction = covid_model.predict(validation_data)

print("Predicted absolute errors on the deaths per capita are: ")
print(mean_absolute_error(validation_target, prediction))
print("Compared to the average deaths per capita: ")
print(average_DeathsPerCapita)




