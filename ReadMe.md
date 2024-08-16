# Economic Analysis Application

**Link to Video Tutorial**: [YouTube Tutorial](https://youtube.com/your-link-here)

## Overview
This application is designed to perform advanced economic data analysis across multiple countries and regions. It allows users to compare indicators, analyze time series, and compute weighted averages across countries based on various economic metrics. The application provides visualizations and statistical tools to analyze trends in economic data over time.

## Table of Contents
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Core Components](#core-components)
- [Usage Guide](#usage-guide)
- [Example Commands](#example-commands)
- [Additional Notes](#additional-notes)

## Features
- **Time Series Analysis**: Extract and plot time series data for a given indicator across countries or regions.
- **Region Analysis**: Create regions composed of multiple countries, calculate averages or weighted averages for each indicator across the region.
- **Statistical Analysis**: Perform statistical analysis, including trend analysis, volatility, and correlations between indicators.
- **Visualization**: Generate professional-grade graphs for time series, trends, and indicator comparisons.

## Setup Instructions

### Prerequisites
Make sure you have the following software installed:
- Python 3.x
- Required Python packages (use the command below to install dependencies)

```bash
pip install -r requirements.txt
```

### Running the App
1. Clone or download the repository from GitHub.
2. Extract the files into your desired directory.
3. Navigate to the project directory using the terminal or command line.
4. Ensure all dependencies are installed. Use the command:

```bash
pip install -r requirements.txt
```

5. Run the application by executing the following command:

```bash
python app.py
```

This will start the application, and you can follow the prompts or interact with the code to perform economic data analysis, visualize trends, and generate reports.

## Core Components

### 1. **Country Class**
   - The `Country` class stores economic data for an individual country. It contains a DataFrame where rows represent economic indicators and columns represent years (e.g., 1960–2020).

### 2. **Region Class**
   - The `Region` class allows the aggregation of data across multiple countries. It can compute simple averages or weighted averages for indicators based on economic metrics like GDP.

### 3. **Analysis Functions**
   - `plot_time_series()`: Generates a time series plot for selected countries and an indicator.
   - `calculate_period_stats()`: Computes statistical data for specific periods across countries or regions.
   - `plot_trend_comparison()`: Plots trend comparison graphs across different periods for countries or regions.

## Usage Guide

### 1. **Extracting Time Series Data**
To extract and visualize time series data for a specific indicator across countries, use the following command:

```python
analyst.plot_time_series([countries], 'indicator_name', period=(1960, 2020))
```
Where:
- `[countries]`: A list of `Country` instances.
- `'indicator_name'`: The name of the indicator (must match the index in the country's DataFrame).
- `period`: Optional. Define the start and end year for the time series plot.

### 2. **Creating a Region**
You can create a region by combining multiple `Country` instances:

```python
LA = Region([country1, country2, country3], weight='average')
```
This creates a region named 'LA' that averages the economic data for the specified countries. If you want to use a weighted average (e.g., by GDP), you can specify an indicator as the weight:

```python
LA = Region([country1, country2, country3], weight='GDP')
```

### 3. **Analyzing Indicator Trends**
You can compare trends between different periods by using the `calculate_period_stats()` function:

```python
table, table_data = analyst.calculate_period_stats([countries], 'indicator_name', periods=[(1970, 1990), (1990, 2010)])
```

This generates statistical data comparing trends across the specified periods.

### 4. **Comparing Two Indicators**
To plot the relationship between two indicators:

```python
analyst.plot_indicator_vs_indicator(country_instance, 'Indicator A', 'Indicator B')
```

This function creates a scatter plot with the option to calculate the linear trend and correlation between the two indicators.

## Example Commands
Here are some example commands to get you started with the app:

- **Plotting a Time Series**:
    ```python
    analyst.plot_time_series([chl, arg, bra], 'GDP (current US$)', period=(1980, 2020))
    ```

- **Creating a Region and Plotting**:
    ```python
    LA = Region([chl, arg, bra], weight='GDP')
    analyst.plot_time_series([LA], 'Foreign direct investment, net inflows (% of GDP)')
    ```

- **Analyzing Trends**:
    ```python
    table, table_data = analyst.calculate_period_stats([chl, arg], 'Foreign direct investment, net inflows (% of GDP)', periods=[(1970, 1990), (1990, 2010)])
    ```

## Additional Notes
- Ensure that your data is properly formatted before analysis. Each `Country` instance must have a DataFrame where rows are indicators and columns are years.
- The region analysis is flexible, allowing either a simple average or weighted average based on any valid indicator.
- Visualizations and tables generated by the app can be customized by modifying input parameters.

## Conclusion
This application provides powerful tools for economic data analysis across countries and regions. Its flexibility allows you to perform detailed analyses of trends, correlations, and relationships between key economic indicators. Refer to the [YouTube tutorial](https://youtube.com/your-link-here) for a step-by-step guide on using the app.

Feel free to reach out with any questions or contributions!
