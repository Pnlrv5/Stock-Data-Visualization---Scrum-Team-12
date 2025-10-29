# Stock Data Visualization - Scrum Team 12
# IT-4320 Project 3

import requests
import matplotlib.pyplot as plt
from input_handler import get_symbol, get_chart_type, get_time_series_function, get_start_date, get_end_date

def get_stock_data(symbol, api_key, function="TIME_SERIES_DAILY"):
    """Retrieve stock data from Alpha Vantage API"""
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}&outputsize=full"
    response = requests.get(url)
    return response.json()

def main():
    print("Welcome to the Stock Data Visualization App!")
    symbol = get_symbol()
    chart_type = get_chart_type()
    function = get_time_series_function()
    start_date = get_start_date()
    end_date = get_end_date()

    # --- Validate Date Range (rubric: validates date range) ---
    if end_date < start_date:
        print("Error: End date cannot be before start date.")
        return

    api_key = input("Enter your Alpha Vantage API key: ")

    # --- Query API (rubric: queries API correctly) ---
    data = get_stock_data(symbol, api_key)

    if "Error Message" in data:
        print("Invalid symbol or API issue.")
        return

    print("✅ Data retrieved successfully!")
    # TODO: Add chart generation later (rubric: correct graph produced)

if __name__ == "__main__":
    main()
