# Stock Data Visualization - Scrum Team 12
# IT-4320 Project 3

import requests
import matplotlib.pyplot as plt
import pygal
from datetime import datetime
import webbrowser

def get_stock_data(symbol, api_key, function="TIME_SERIES_DAILY"):
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}&outputsize=full"
    response = requests.get(url)
    # Verify response
    if response.status_code != 200: #200 means request was successful
        print("Error: Could not reach the API.")
        return None
    data = response.json()
    if "Error Message" in data:
        print("Invalid symbol or API issue.")
        return
    return response.json()

def chart_generator(data, symbol, chart_type, start_date, end_date):
    time_series = data.get("Time Series (Daily)",{})
    #filters and sorts the dates and the times
    filtered_dates=[
        date for date in time_series.keys() 
        if start_date<=date<=end_date
    ]
    filtered_dates.sort()
    if not filtered_dates:
        print("No data available for the given date range.")
        return
    open_prices=[float(time_series[date]["1. open"]) for date in filtered_dates]
    high_prices=[float(time_series[date]["2. high"]) for date in filtered_dates]
    low_prices=[float(time_series[date]["3. low"]) for date in filtered_dates]
    close_prices=[float(time_series[date]["4. close"]) for date in filtered_dates]
    #Checks if chart_type is line, if not then bar
    if chart_type=="line":
        chart = pygal.Line(
            x_label_rotation=45,
            show_minor_x_labels=False,
            show_legend=True,
            dots_size=2,
            stroke_style={'width': 2}
        )
    else:
        chart=pygal.Bar(
            x_label_rotation=45,
            show_minor_x_labels=False,
            show_legend=True
        )
    #labels
    chart.title = f"Stock Data for {symbol}: {start_date} to {end_date}"
    chart.x_labels = filtered_dates
    chart.x_labels_major = filtered_dates[::len(filtered_dates)//10 or 1]  # major x labels
    chart.x_title = "Date"
    chart.y_title = "Stock Price (USD)"
    #data series
    chart.add("Open", open_prices)
    chart.add("High", high_prices)
    chart.add("Low", low_prices)
    chart.add("Close", close_prices)
    #opens chart in default browser
    chart.render_in_browser()

def main():
    api_key = ("8KOR8I2BG99OUCWG")
    print("Welcome to the Stock Data Visualization App!")

    # User Input
    symbol = input("Enter stock symbol: ").upper()
    
    # Query API 
    data = get_stock_data(symbol, api_key)
    while data is None:
        symbol = input("Enter a valid stock symbol: ").upper()
        data = get_stock_data(symbol, api_key)
    print("Data retrieved successfully!")


    chart_type = input("Enter chart type (line/bar): ").lower()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    try: 
        startdate = datetime.strptime(start_date, "%Y-%m-%d")
        enddate = datetime.strptime(end_date, "%Y-%m-%d")

    ## validates the ranges part of the rubric
        if enddate < startdate:
            print("Error: End date cannot be before start date.")
            return
    except ValueError:
        print("invalid Date, please sure the YYYY-DD-MM format.")
        return

if __name__ == "__main__":
    main()
