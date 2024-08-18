# https://github.com/blankhall98/CaseCountryAnalysis

from scripts.country import Country, Region
from case import Case
from scripts.analysis import Analyst

# Initialize analyst instance
routes = Case['routes']
analyst = Analyst(routes)

# Countries
chl = analyst.extract_country_data('CHL','Chile')
arg = analyst.extract_country_data('ARG','Argentina')
mex = analyst.extract_country_data('MEX','Mexico')
usa = analyst.extract_country_data('USA','United States')
bra = analyst.extract_country_data('BRA','Brazil')
col = analyst.extract_country_data('COL','Colombia')
bol = analyst.extract_country_data('BOL','Bolivia')
per = analyst.extract_country_data('PER','Peru')
ecu = analyst.extract_country_data('ECU','Ecuador')
ven = analyst.extract_country_data('VEN','Venezuela')

#Region
neo_populist = Region([arg,bol,ecu,bra,ven],'Neo-Populist', weight='Real GDP (2005)')
neo_liberal = Region([chl,col,per],'Neo-Liberal', weight='Real GDP (2005)')

##### CASE #####
indicator = "Unemployment, total (% of total labor force) (modeled ILO)"
countries = [chl,arg]
period = (1989,2020)

chilean_periods = [(1960,1970),(1970,1973),(1973,1990),(1990,2000),(2000,2020)]
chilean_titles = ['Pre-Nationalization','Nationalization','Chile Privatization','Chilean Transition','Chilean Modernization']

argentinian_periods = [(1980,1989),(1989,1999),(2003,2020)]
argentinian_titles = ['Pre-Privatization','Argentina Privatization','Long-Term Kirchnerism']

regional_periods = [(1960,1980),(1980,1990),(1990,2000),(2000,2020)]
regional_titles = ['Historical Trend','Privatization Wave','Short-Term','Long-Term']

periods = [(1973,1990),(1989,1999),(2000,2006)]
periods_titles = ['Chile Privatization',"Argentina Privatization",'Argentina Kirchnerism']

mixed_periods = [(1989,1999),(2003,2010),(2010,2020)]
mixed_titles = ["Argentina Privatization",'Argentina Kirchnerism','Long-Term']

###########
periods = mixed_periods
periods_titles = mixed_titles

##### ACTIONS #####
if __name__ == "__main__":
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
    print(table['Mean'])
    analyst.plot_trend_comparison(table, table_data)

    # Indicator vs Indicator
    #indicators = ['Foreign direct investment, net inflows (% of GDP)', 'Gini index (World Bank estimate)']
    #table = analyst.indicator_relationship_stats(arg, indicators[0], indicators[1])
    #print(table)

    ##########
