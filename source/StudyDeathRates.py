from OrganizeFrames import date_as_str, organize_covid_frame, organize_frame, get_countries
from PlotFrames import label_points, plot_rates_by_gdp


#######################################
### Main code starts here #############
#######################################

random_mix = ["US", "Germany", "France", "Italy", "India", "Brazil", "Japan", "Canada", "Mexico", "Thailand"]
top_gdppc = ["Switzerland", "Ireland", "Norway", "US", "Singapore", "Denmark", "Australia", "Netherlands", "Sweden", "Austria", "Finland", "Germany"]
time_period = 180 #days 

#plot_rates(random_mix, time_period, suffix="")
#plot_rates(top_gdppc, time_period, suffix="topgdp")
#plot_rates(friends, time_period, suffix="friends")

countries = get_countries( population = 1E4, c_type = "countries" )
countries = '''["'''+'''", "'''.join(countries)+'''"]'''

almost_all_countries = ["Afghanistan", "Algeria", "Angola", "Argentina",  "Australia", "New Zealand", "Austria", "Azerbaijan", "Bangladesh", "Belarus", "Belgium", "Benin", "Brazil", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Chad", "Chile", "China", "Taiwan*", "Colombia", "Cuba", "Czechia", "Cote d'Ivoire", "Dominican Republic", "Ecuador", "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia", "France", "Gabon", "Gambia", "Germany", "Ghana", "Greece", "Guatemala", "Guinea", "Guinea-Bissau", "Haiti", "Honduras", "Hungary", "India", "Indonesia", "Iraq", "Israel", "Italy", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kyrgyzstan", "Liberia", "Libya", "Madagascar", "Malawi", "Malaysia", "Mali", "Mauritania", "Mexico", "Morocco", "Mozambique", "Namibia", "Nepal", "Netherlands", "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Korea, South", "Romania", "Rwanda", "Saudi Arabia", "Senegal", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Sweden", "Switzerland", "Syria", "Tajikistan", "Thailand", "Togo", "Tunisia", "Turkey", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "Tanzania", "US", "Uzbekistan", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

eu_countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]


#plot_rates_by_gdp(random_mix)

plot_rates_by_gdp(almost_all_countries)

plot_rates_by_gdp(eu_countries, suffix="eu")

