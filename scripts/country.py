import pandas as pd
import numpy as np

class Country:

    def __init__(self, inputs):
        self.ISO = inputs['ISO']
        self.name = inputs['name']
        self.data = inputs['data']

class Region:
    def __init__(self, countries, name="Region", weight='average'):
        """
        Initialize a Region instance with a list of countries and an optional weight parameter.

        Parameters:
        - countries: List of Country instances.
        - name: The name of the region (default is "Region").
        - weight: 'average' (default) to average all indicators across countries,
                  or a specific indicator (e.g., 'GDP') to weight the countries based on that indicator.
        """
        self.countries = countries
        self.weight = weight
        self.name = f"{name} ({weight})"

        # Compute the region data based on the weight
        self.data = self.compute_region_data()

    def compute_region_data(self):
        """
        Compute the region's aggregated data based on the given weight.
        
        If the weight is 'average', it averages the indicators across countries.
        If the weight is an indicator, it calculates a weighted average based on that indicator.
        """
        if self.weight == 'average':
            return self.average_indicators()
        else:
            return self.weighted_indicators()

    def ensure_unique_index(self, country_data):
        """
        Ensure the index (indicators) in the country's data is unique.
        If there are duplicates, rename them by appending a suffix to make them unique.
        """
        # If there are duplicates in the index, append a suffix to make them unique
        if country_data.index.duplicated().any():
            country_data.index = pd.Index([f"{idx}_{i}" if is_dup else idx
                                           for i, (idx, is_dup) in enumerate(zip(country_data.index, country_data.index.duplicated(keep=False)))])
        return country_data

    def average_indicators(self):
        """
        Calculate the average of each indicator across all countries (ignoring missing values).
        """
        # Ensure that the index and columns align for all country data
        aligned_data = []
        for country in self.countries:
            # Ensure each country data has unique indicator names
            country.data = self.ensure_unique_index(country.data)
            aligned_data.append(country.data)

        # Concatenate country data along the columns (so we can average them)
        combined_data = pd.concat(aligned_data, axis=1, join='outer')

        # Calculate the row-wise mean for each indicator-year pair (ignoring NaNs)
        averaged_data = combined_data.groupby(combined_data.columns, axis=1).mean()

        return averaged_data

    def weighted_indicators(self):
        """
        Calculate the weighted average of each indicator across all countries based on the given indicator.
        """
        # Ensure that all countries have the weight indicator
        weight_data = {}
        for country in self.countries:
            if self.weight not in country.data.index:
                raise ValueError(f"Indicator '{self.weight}' not found in {country.name}'s data.")
            # Store the weight for this country
            weight_data[country.name] = country.data.loc[self.weight]

        # Align country data and create combined data
        combined_data = []
        for country in self.countries:
            # Ensure unique index for each country data
            country.data = self.ensure_unique_index(country.data)
            combined_data.append(country.data)

        # Initialize DataFrame to accumulate weighted results
        weighted_sum = pd.DataFrame(0, index=combined_data[0].index, columns=combined_data[0].columns)

        # Initialize DataFrame to accumulate the total weights (to normalize later)
        total_weights = pd.DataFrame(0, index=combined_data[0].index, columns=combined_data[0].columns)

        # Loop through each country and apply weights
        for i, country in enumerate(self.countries):
            country_data = combined_data[i]  # Country data (indicators x years)
            country_weights = weight_data[country.name]  # Weights for this country (1D array of years)
            
            for year in country_data.columns:  # Iterate over the years (columns)
                # Apply the weight to the data for this year
                weight_for_year = country_weights[year]  # Weight for the current year
                weighted_sum[year] += country_data[year] * weight_for_year  # Weighted sum for this year
                total_weights[year] += weight_for_year  # Accumulate the total weights for normalization

        # Normalize the weighted sum by dividing by the total weights
        weighted_average = weighted_sum.div(total_weights)

        return weighted_average