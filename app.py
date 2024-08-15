from scripts.country import Country
from case import Case
from scripts.analysis import Analyst

routes = {
    'qog_db': './data/QOG-BD.csv'
}

analyst = Analyst(routes)
analyst.load_data()

chl = analyst.extract_country_data('CHL','Chile')
arg = analyst.extract_country_data('ARG','Argentina')
usa = analyst.extract_country_data('USA','United States')


##### ACTIONS #####
###case
indicator = "Total Export"
countries = [chl, arg]
period = (1960,2020)
periods = [(1970,1973),(1973, 1990), (1990, 2010)]
periods_titles = ['Allende Nationalization','Pinochet Dictatorship', 'Democracy']

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





