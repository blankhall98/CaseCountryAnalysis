# https://github.com/blankhall98/CaseCountryAnalysis

from scripts.country import Country, Region
from case import Case
from scripts.analysis import Analyst

routes = {
    'qog_db': './data/QOG-BD.csv'
}

analyst = Analyst(routes)
analyst.load_data()

# Countries
chl = analyst.extract_country_data('CHL','Chile')
arg = analyst.extract_country_data('ARG','Argentina')
mex = analyst.extract_country_data('MEX','Mexico')
usa = analyst.extract_country_data('USA','United States')
bra = analyst.extract_country_data('BRA','Brazil')
col = analyst.extract_country_data('COL','Colombia')
bol = analyst.extract_country_data('BOL','Bolivia')
per = analyst.extract_country_data('PER','Peru')

#Region
LA = Region([chl, arg, mex, bra, col, bol, per],'Latin America', weight='Real GDP (2005)')

##### CASE #####
indicator = "Foreign direct investment, net inflows (% of GDP)"
countries = [chl, arg, LA]
period = (1960,2020)
periods = [(1970,1973),(1973, 1990), (1990, 2010)]
periods_titles = ['Allende Nationalization','Pinochet Dictatorship', 'Democracy']
###########

##### ACTIONS #####

#analyst.plot_time_series(countries, 'Oil production value in 2014 dollars')
analyst.plot_time_series(countries, indicator, 
                        period=period, periods=periods,
                        periods_titles=periods_titles
                        )

# table statistics
table , table_data = analyst.calculate_period_stats(countries,
                                                     indicator,
                                                     periods=periods,
                                                     periods_titles=periods_titles
                                                     )

print(table)
analyst.plot_trend_comparison(table, table_data)

# Indicator vs Indicator
indicators = ['Trade (% of GDP)', 'Foreign direct investment, net inflows (% of GDP)']
table = analyst.indicator_relationship_stats(chl, indicators[0], indicators[1])
print(table)

##########
