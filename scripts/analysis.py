import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr, linregress

from scripts.country import Country

class Analyst:

    def __init__(self,routes):
        self.routes = routes

    def load_data(self):
        self.qog_db = pd.read_csv(self.routes['qog_db'])
        self.time_period = (1960,2020)
        self.non_year_columns = ['Economy ISO3', 'Economy Name', 'Indicator ID', 'Indicator']
        self.year_columns = [str(year) for year in range(self.time_period[0], self.time_period[1] + 1)]
        self.columns_to_keep = self.non_year_columns + self.year_columns
        self.qog_db = self.qog_db[self.columns_to_keep]

    def extract_country_data(self, iso_code, name):
    # Filter the DataFrame based on the 'Economy ISO3' column
        country_data = self.qog_db[self.qog_db['Economy ISO3'] == iso_code].set_index('Indicator')
        country_data = country_data.drop(self.columns_to_keep[:3], axis=1)
        country_data = country_data.map(lambda x: float(str(x).replace(',', '.')) if isinstance(x, str) else x)
        token = Country({'ISO': iso_code, 'data': country_data, 'name': name})
        return token
    
    def plot_time_series(self, countries, indicator, period=False, periods=None, periods_titles=None):
        plt.figure(figsize=(10, 6))

        # Set the default period if not provided
        if not period:
            period = (1960, 2020)

        # Define a list of pastel colors for shading the periods
        pastel_colors = ['#ffb3ba', '#baffc9', '#bae1ff', '#ffffba', '#ffdfba', '#ffb3ff']

        # Loop over each country in the provided list
        for country in countries:
            # Select the time series for the indicator and filter by the period
            time_series = country.data.loc[indicator, str(period[0]):str(period[1])]

            # Plot the time series for each country
            plt.plot(time_series.index, time_series.values, marker='o', linestyle='-', label=country.name)

        # If periods for shading are provided, highlight them with pastel colors
        if periods:
            for i, (start_year, end_year) in enumerate(periods):
                # Make sure the index is within bounds of the data
                start_year_str = str(max(start_year, period[0]))  # Ensuring period lies within range
                end_year_str = str(min(end_year, period[1]))
                
                # If start_year and end_year are in the index, fill between
                if start_year_str in time_series.index and end_year_str in time_series.index:
                    # Shade the area with pastel color
                    plt.axvspan(start_year_str, end_year_str, color=pastel_colors[i % len(pastel_colors)], alpha=0.3, 
                                label=periods_titles[i] if periods_titles else f'Period {i+1}')

        # Set the title and labels
        plt.title(f'Time Series of {indicator} ({period[0]}-{period[1]})', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Value', fontsize=12)

        # Enable the grid for a clean look
        plt.grid(True, linestyle='--', alpha=0.7)

        # Rotate the x-ticks for better readability
        plt.xticks(rotation=45)

        # Add a legend
        plt.legend(loc='best', fontsize=10)

        # Adjust the layout
        plt.tight_layout()

        # Display the plot
        plt.show()

    def calculate_period_stats(self, countries, indicator, periods=None, periods_titles=None, filename=None):
        """
        Calculate detailed statistics, including linear trend, volatility (standard deviation),
        and the count of downward movements for a specific indicator over specified periods 
        for each country, their pooled average, and the overall historical period.

        Parameters:
        - countries: A list of country instances.
        - indicator: The indicator to calculate statistics for (must be in the index).
        - periods: A list of tuples representing the start and end years (e.g., [(1960, 1971), (1973, 1990)]).
        - periods_titles: Optional list of period names (e.g., ["Privatización", "Nacionalización"]).
        - filename: Optional filename to save the resulting table as a CSV.

        Returns:
        - A pandas DataFrame with statistics for each country in each period and their average,
        along with a secondary dictionary containing trends and volatility for graphing.
        """
        if not periods:
            print("No periods provided.")
            return

        stats_list = []
        graph_data = {'indicator': indicator, 'periods': [], 'countries': {}, 'average': {}}

        # Historical full period (1960-2020)
        historical_period = (1960, 2020)
        historical_period_name = "Historical (1960-2020)"

        # Iterate over each country
        for country in countries:
            if indicator not in country.data.index:
                print(f"Indicator '{indicator}' not found for {country.name}. Skipping...")
                continue

            country_trend = []

            # Iterate over each period
            for i, (start_year, end_year) in enumerate(periods):
                period_name = periods_titles[i] if periods_titles else f'Period {i+1}'
                period_full_name = f"{period_name} ({start_year}-{end_year})"
                
                # Extract time series data for the period
                time_series = country.data.loc[indicator, str(start_year):str(end_year)].dropna()  # Drop NaN values
                years = np.array(time_series.index.astype(int))  # Convert index to integers
                
                # Count downward movements (times when value decreased from one year to the next)
                down_movements = (time_series.diff() < 0).sum()
                
                # Perform linear regression to get the trend (slope)
                if len(time_series) > 1:  # Ensure there are enough data points
                    model = LinearRegression().fit(years.reshape(-1, 1), time_series.values)
                    trend = model.coef_[0]  # Slope of the trend
                else:
                    trend = np.nan  # No trend if insufficient data

                # Add period data to graph dictionary for each country
                country_trend.append({'years': years, 'values': time_series.values, 'std_dev': time_series.std()})

                # Compute basic statistics and volatility
                stats = {
                    'Country': country.name,
                    'Period': period_full_name,
                    'Start Year': start_year,
                    'End Year': end_year,
                    'Mean': time_series.mean(),
                    'Median': time_series.median(),
                    'Min': time_series.min(),
                    'Max': time_series.max(),
                    'Std Dev': time_series.std(),  # Volatility measurement
                    'Linear Trend (Coeff)': trend,
                    'Down Movements': down_movements  # Count of downward movements
                }

                stats_list.append(stats)
            
            # Store country's data for graphing
            graph_data['countries'][country.name] = country_trend

            # Historical statistics (1960-2020) for the full time period
            historical_time_series = country.data.loc[indicator, str(historical_period[0]):str(historical_period[1])].dropna()  # Drop NaNs
            historical_years = np.array(historical_time_series.index.astype(int))

            if len(historical_time_series) > 1:
                historical_model = LinearRegression().fit(historical_years.reshape(-1, 1), historical_time_series.values)
                historical_trend = historical_model.coef_[0]
            else:
                historical_trend = np.nan

            # Add historical statistics for the country
            historical_stats = {
                'Country': country.name,
                'Period': historical_period_name,
                'Start Year': historical_period[0],
                'End Year': historical_period[1],
                'Mean': historical_time_series.mean(),
                'Median': historical_time_series.median(),
                'Min': historical_time_series.min(),
                'Max': historical_time_series.max(),
                'Std Dev': historical_time_series.std(),
                'Linear Trend (Coeff)': historical_trend,
                'Down Movements': (historical_time_series.diff() < 0).sum()  # Count downward movements in historical period
            }
            stats_list.append(historical_stats)

        # Create a DataFrame with the statistics
        stats_df = pd.DataFrame(stats_list)

        # Store period titles for graphing
        graph_data['periods'] = [{'title': periods_titles[i], 'start_year': periods[i][0], 'end_year': periods[i][1]} for i in range(len(periods))]

        # Calculate average statistics across all countries for each period, including historical
        avg_stats_list = []
        all_periods = periods_titles + [historical_period_name] if periods_titles else [f"Period {i+1}" for i in range(len(periods))] + [historical_period_name]

        for period_name in all_periods:
            # Filter the DataFrame for the current period
            period_stats = stats_df[stats_df['Period'] == period_name]

            # Calculate average statistics across all countries
            if not period_stats.empty:
                avg_stats = {
                    'Country': 'Average',
                    'Period': period_name,
                    'Mean': period_stats['Mean'].mean(),
                    'Median': period_stats['Median'].mean(),
                    'Min': period_stats['Min'].mean(),
                    'Max': period_stats['Max'].mean(),
                    'Std Dev': period_stats['Std Dev'].mean(),  # Average Volatility
                    'Linear Trend (Coeff)': period_stats['Linear Trend (Coeff)'].mean(),
                    'Down Movements': period_stats['Down Movements'].mean()
                }

                avg_stats_list.append(avg_stats)

        # Append the average statistics to the DataFrame
        avg_stats_df = pd.DataFrame(avg_stats_list)
        final_stats_df = pd.concat([stats_df, avg_stats_df], ignore_index=True)

        # Save to CSV if filename is provided
        if filename:
            final_stats_df.to_csv(filename, index=False)

        # Return the DataFrame and graph data for visualization
        return final_stats_df, graph_data
    
    def plot_trend_comparison(self, table, graph_data):
        """
        Plot the comparison of linear trends for multiple countries with shaded volatility and period markers.

        Parameters:
        - table: DataFrame containing statistics including period start and end years.
        - graph_data: Dictionary with trend and volatility data for plotting.

        Returns:
        - None, displays the plot.
        """
        indicator = graph_data['indicator']
        periods_info = graph_data['periods']
        
        if periods_info is None or len(periods_info) == 0:
            raise ValueError("No periods data found in graph_data.")

        plt.figure(figsize=(12, 7))

        # Set a color palette for countries
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

        # Store the period start years and titles for the x-axis
        shift_years = []
        shift_labels = []

        # Plot each country's trends with shaded volatility
        for country_idx, (country_name, country_data) in enumerate(graph_data['countries'].items()):
            for period_idx, period_data in enumerate(country_data):
                # Ensure years are numeric
                years = pd.to_numeric(np.array(period_data['years']), errors='coerce')  # Convert years to numeric array
                values = np.array(period_data['values'], dtype=float)  # Ensure values are floats
                std_dev = period_data['std_dev']
                
                # Perform linear regression to get the trend line across the period
                X = years.reshape(-1, 1)
                if len(values) > 1:
                    model = LinearRegression().fit(X, values)
                    trend_values = model.predict(X)  # Predicted values (trend line)
                    trend_coefficient = model.coef_[0]

                    # Plot the trend line
                    plt.plot(years, trend_values, color=colors[country_idx % len(colors)], label=f'{country_name} (Period {period_idx+1})')

                    # Add the trend coefficient as text above the line, using darker color and larger font
                    plt.text(np.mean(years), np.mean(trend_values), f'{trend_coefficient:.2f}', color=colors[country_idx % len(colors)],
                            fontsize=12, fontweight='bold', verticalalignment='bottom')

                    # Shade the area to represent volatility (1 std dev)
                    plt.fill_between(years, trend_values - std_dev, trend_values + std_dev, color=colors[country_idx % len(colors)], alpha=0.2)

        # Add vertical lines for the shift years and display the period titles
        for i, period_info in enumerate(periods_info):
            # We skip the last period since there's no next period
            start_year = period_info['start_year']
            title = period_info['title']
            
            shift_years.append(start_year)

            # Add vertical line for period transition
            plt.axvline(x=start_year, color='gray', linestyle='--', lw=1)

            # Add rotated -90° period title to the left of the shift line
            plt.text(start_year - 0.5, plt.ylim()[1], title, color='gray', fontsize=10, verticalalignment='top', horizontalalignment='right', rotation=90)

            # Add year below the shift line on the x-axis
            shift_labels.append(f"{start_year}")

        # Set the x-axis ticks for the shift years, showing only the years
        plt.xticks(shift_years, shift_labels, fontsize=12)

        # Add labels and title
        plt.title(f'Trend Comparison for {indicator} Across Periods', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Value', fontsize=12)

        # Remove intermediate grid lines for a cleaner look
        plt.grid(True, linestyle='--', alpha=0.7)

        # Show legend
        plt.legend(loc='best', fontsize=10)

        # Display the plot
        plt.tight_layout()
        plt.show()

    def indicator_relationship_stats(self, country, indicator_x, indicator_y, plot=True):
        """
        Return a table with important statistical values for the relationship between two indicators,
        and optionally plot a regression graph.
        
        Parameters:
        - country: A country instance (with the .data DataFrame containing indicators).
        - indicator_x: The indicator to use as the independent variable (x-axis).
        - indicator_y: The indicator to use as the dependent variable (y-axis).
        - plot: Boolean indicating whether to produce a regression plot.
        
        Returns:
        - DataFrame containing important statistics.
        - Optionally displays a plot of the regression.
        """
        if indicator_x not in country.data.index or indicator_y not in country.data.index:
            print(f"One or both indicators not found for {country.name}.")
            return None
        
        # Extract the values for both indicators
        x_values = country.data.loc[indicator_x].dropna()
        y_values = country.data.loc[indicator_y].dropna()

        # Only keep years that are available in both indicators
        common_years = x_values.index.intersection(y_values.index)
        x_values = x_values.loc[common_years]
        y_values = y_values.loc[common_years]
        
        if len(common_years) < 2:
            print(f"Not enough data points for {country.name}.")
            return None

        # Calculate linear regression statistics
        slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
        r_squared = r_value ** 2
        
        # Calculate Pearson correlation
        corr, _ = pearsonr(x_values, y_values)
        
        # Mean and standard deviation of both indicators
        x_mean = x_values.mean()
        x_std = x_values.std()
        y_mean = y_values.mean()
        y_std = y_values.std()
        
        # Create a table of statistics
        stats = {
            'Metric': ['Slope', 'Intercept', 'R-squared', 'Correlation (r)', 'P-value', 
                    f'Mean of {indicator_x}', f'Std Dev of {indicator_x}', 
                    f'Mean of {indicator_y}', f'Std Dev of {indicator_y}'],
            'Value': [slope, intercept, r_squared, corr, p_value, x_mean, x_std, y_mean, y_std]
        }
        
        stats_df = pd.DataFrame(stats)
        
        # Optionally plot the regression
        if plot:
            plt.figure(figsize=(10, 6))

            # Scatter plot of the data points
            plt.scatter(x_values, y_values, color='blue', label=f'{country.name}', marker='o')

            # Linear regression line
            X = np.array(x_values).reshape(-1, 1)
            trend_line = slope * X + intercept
            plt.plot(x_values, trend_line, color='red', label=f'Trend Line: y = {slope:.2f}x + {intercept:.2f}')
            
            # Display regression statistics in the plot
            plt.text(0.05, 0.95, f'R-squared: {r_squared:.2f}\nCorrelation: {corr:.2f}', 
                    transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

            # Set the title and labels
            plt.title(f'{indicator_y} vs. {indicator_x} for {country.name}', fontsize=16)
            plt.xlabel(f'{indicator_x}', fontsize=12)
            plt.ylabel(f'{indicator_y}', fontsize=12)

            # Create the legend with country name and trend line
            plt.legend(title=f'{country.name}', fontsize=10)

            # Add grid for readability
            plt.grid(True, linestyle='--', alpha=0.7)

            # Display the plot
            plt.tight_layout()
            plt.show()
        
        return stats_df