import pandas as pd
import eli5

from eli5.sklearn import PermutationImportance
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

# Append any other fields that may be predictive here
frames["GDPPerCapita"] = frames.apply(lambda row: row.GDP/row.PopTotal, axis=1)

# Append on deaths per capita
frames["DeathsPerCapita"] = frames.apply(lambda row: row.Deaths/row.PopTotal, axis=1)
average_DeathsPerCapita   = frames["DeathsPerCapita"].agg("mean")

target = frames.DeathsPerCapita

print (frames.columns)

# Remove "services" as I suspect it is too correlated to agriculture and industry
features = ["Incident_Rate", "Case_Fatality_Ratio", 
            "PopDensity", 
            "GDPPerCapita", "agriculture", "industry"]

# First pass shows education data has little to no ability to predict death rate!
#           "prim_edu_fem", "prim_edu_male", "seco_edu_fem", "seco_edu_male", "tert_edu_fem", "tert_edu_male"]

data = frames[ features ] 

print (data)

train_data, validation_data, train_target, validation_target  = train_test_split(data, target, random_state=0)

covid_model = DecisionTreeRegressor(splitter="best")
covid_model.fit(train_data, train_target)

prediction = covid_model.predict(validation_data)

print("Predicted absolute errors on the deaths per capita are: ")
print(mean_absolute_error(validation_target, prediction))
print("Compared to the average deaths per capita: ")
print(average_DeathsPerCapita)


print("Testing permutation importance on the features")
perm = PermutationImportance(covid_model, random_state=1).fit(validation_data, validation_target)
print(eli5.format_as_text(eli5.explain_weights(perm, feature_names=features)))

