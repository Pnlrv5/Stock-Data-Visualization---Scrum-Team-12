# Stock Data Visualization - Scrum Team 12
# IT-4320 Project 3

import requests
import pygal
from datetime import datetime
import input_handler

def get_stock_data(symbol, api_key, function_choice):
    function_map = {
        "intraday": "TIME_SERIES_INTRADAY", "daily": "TIME_SERIES_DAILY", "weekly": "TIME_SERIES_WEEKLY", "monthly": "TIME_SERIES_MONTHLY"}
    #includes interval for intraday
    if function_choice== "intraday":
        url =f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval=60min&apikey={api_key}&outputsize=full"
    else:
        url =f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}&outputsize=full"
    response =requests.get(url)
    if response.status_code!= 200: #200 is error code for successful response
        print("Error: Could not reach the API.")
        return None
    data = response.json()
    if "Error Message" in data or not data:
        print("Invalid symbol or API issue.")
        return None
    return data
def chart_generator(data, symbol, chart_type, start_date, end_date):
    # Automatically detect the key that contains time series data
    time_series = None
    for key in data.keys():
        if "Time Series" in key:
            time_series = data[key]
            print(f"DEBUG: Using time series key '{key}'")
            break

    if not time_series:
        print("invalid time series.")
        print("Keys found:", list(data.keys()))
        return
    #filer by date range
    filtered_dates = [date for date in time_series.keys() if start_date <= date <= end_date]
    filtered_dates.sort()
    if not filtered_dates:
        print("No data available for the given date range.")
        return
    open_prices = [float(time_series[date]["1. open"]) for date in filtered_dates]
    high_prices = [float(time_series[date]["2. high"]) for date in filtered_dates]
    low_prices = [float(time_series[date]["3. low"]) for date in filtered_dates]
    close_prices = [float(time_series[date]["4. close"]) for date in filtered_dates]
    #chart type selection
    if chart_type == "line":
        chart = pygal.Line(
            x_label_rotation=45,
            show_minor_x_labels=False,
            show_legend=True,
            dots_size=2,
            stroke_style={'width': 2}
        )
    else:
        chart = pygal.Bar(
            x_label_rotation=45,
            show_minor_x_labels=False,
            show_legend= True
        )
    chart.title = f"Stock Data for {symbol}: {start_date} to {end_date}"
    chart.x_labels = filtered_dates
    chart.x_labels_major = filtered_dates[::max(len(filtered_dates)//10, 1)]
    chart.x_title = "Date"
    chart.y_title = "Stock Price (USD)"
    chart.add("Open", open_prices)
    chart.add("High", high_prices)
    chart.add("Low", low_prices)
    chart.add("Close", close_prices)
    chart.render_in_browser()


def main():
    api_key = "HQXG2RROB6JX4YLI"
    print("Welcome to the Stock Data Visualization App!\n")
    #user inputss 
    symbol = input_handler.get_symbol()
    function_choice = input_handler.get_time_series_function()
    chart_type = input_handler.get_chart_type()
    start_date = input_handler.get_start_date()
    end_date = input_handler.get_end_date()
    #Checker for date range
    try:
        startdate_obj = datetime.strptime(start_date, "%Y-%m-%d")
        enddate_obj = datetime.strptime(end_date, "%Y-%m-%d")
        if enddate_obj < startdate_obj:
            print("Error: End date cannot be before start date.")
            return
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    #Retrievse the data 
    data = get_stock_data(symbol, api_key, function_choice)
    while data is None:
        symbol = input_handler.get_symbol()
        data = get_stock_data(symbol, api_key, function_choice)
    print("Data retrieved successfully!")
    chart_generator(data, symbol, chart_type, start_date, end_date)


if __name__ == "__main__":
    main()
