# Stock Data Visualization - Scrum Team 12
# IT-4320 Project 3

import requests
import matplotlib.pyplot as plt

def get_stock_data(symbol, api_key, function="TIME_SERIES_DAILY"):
    """Retrieve stock data from Alpha Vantage API"""
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
    # TODO: Add chart generation later (rubric: correct graph produced)


    chart_type = input("Enter chart type (line/bar): ").lower()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    # --- Validate Date Range (rubric: validates date range) ---
    if end_date < start_date:
        print("Error: End date cannot be before start date.")
        return

if __name__ == "__main__":
    main()
