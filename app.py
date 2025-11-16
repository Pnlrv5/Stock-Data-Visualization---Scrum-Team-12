import os
import csv
import io
import base64
from datetime import datetime

import requests
from flask import Flask, render_template, request

import matplotlib
matplotlib.use("Agg")  # so it works without a display (for Docker, etc.)
import matplotlib.pyplot as plt

app = Flask(__name__)

# Use env var if set, otherwise fall back to your existing key
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "HQXG2RROB6JX4YLI")


def load_stock_symbols(csv_path="stocks.csv"):
    """
    Read symbols + names from stocks.csv to populate the dropdown.
    Assumes a header row with at least 'Symbol' and maybe 'Name' or 'Security'.
    """
    symbols = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row.get("Symbol") or row.get("symbol") or row.get("Ticker")
            name = row.get("Name") or row.get("Security") or ""
            if symbol:
                symbols.append({"symbol": symbol.strip(), "name": name.strip()})
    return symbols


def get_stock_data(symbol, function_choice):
    """
    Similar to your get_stock_data() in main.py, but fixed + used by Flask.
    """
    function_map = {
        "intraday": "TIME_SERIES_INTRADAY",
        "daily": "TIME_SERIES_DAILY",
        "weekly": "TIME_SERIES_WEEKLY",
        "monthly": "TIME_SERIES_MONTHLY",
    }

    if function_choice not in function_map:
        raise ValueError("Invalid time series selection.")

    function = function_map[function_choice]

    base_url = "https://www.alphavantage.co/query"

    params = {
        "function": function,
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "full",
    }

    # Intraday requires an interval parameter
    if function_choice == "intraday":
        params["interval"] = "60min"

    resp = requests.get(base_url, params=params, timeout=20)

    if resp.status_code != 200:
        raise RuntimeError("Error: Could not reach the API.")

    data = resp.json()

    if "Error Message" in data or not data:
        raise RuntimeError("Invalid symbol or API issue.")

    return data


def extract_series_for_range(data, start_date, end_date):
    """
    Mimics your chart_generator() logic: find the Time Series key,
    filter by date range, and pull open/high/low/close.
    """
    time_series = None
    for key in data.keys():
        if "Time Series" in key:
            time_series = data[key]
            break

    if not time_series:
        raise RuntimeError("Invalid time series data returned from API.")

    # Filter by date range (YYYY-MM-DD)
    filtered_dates = [d for d in time_series.keys() if start_date <= d <= end_date]
    filtered_dates.sort()

    if not filtered_dates:
        raise ValueError("No data available for the given date range.")

    open_prices = [float(time_series[d]["1. open"]) for d in filtered_dates]
    high_prices = [float(time_series[d]["2. high"]) for d in filtered_dates]
    low_prices = [float(time_series[d]["3. low"]) for d in filtered_dates]
    close_prices = [float(time_series[d]["4. close"]) for d in filtered_dates]

    return filtered_dates, open_prices, high_prices, low_prices, close_prices


def create_chart_base64(
    dates, open_prices, high_prices, low_prices, close_prices,
    symbol, chart_type, start_date, end_date
):
    """
    Build a chart with matplotlib (line or bar) and return it as a base64 string
    so we can embed it directly in the HTML.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    if chart_type == "line":
        ax.plot(dates, open_prices, label="Open")
        ax.plot(dates, high_prices, label="High")
        ax.plot(dates, low_prices, label="Low")
        ax.plot(dates, close_prices, label="Close")
    else:
        # For bar, just show close prices to keep it readable
        ax.bar(dates, close_prices, label="Close")

    ax.set_title(f"Stock Data for {symbol}: {start_date} to {end_date}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_bytes = buf.getvalue()
    plt.close(fig)

    return base64.b64encode(img_bytes).decode("ascii")


@app.route("/", methods=["GET", "POST"])
def index():
    symbols = load_stock_symbols()

    # Defaults for page render
    chart_image = None
    error = None
    selected_symbol = None
    function_choice = "daily"
    chart_type = "line"
    start_date = None
    end_date = None

    if request.method == "POST":
        selected_symbol = request.form.get("symbol")
        function_choice = request.form.get("function_choice") or "daily"
        chart_type = request.form.get("chart_type") or "line"
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        try:
            if not selected_symbol:
                raise ValueError("Please select a stock symbol.")
            if not start_date or not end_date:
                raise ValueError("Please enter both start and end dates.")

            # Validate date order
            start_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_obj = datetime.strptime(end_date, "%Y-%m-%d")
            if end_obj < start_obj:
                raise ValueError("End date cannot be before start date.")

            data = get_stock_data(selected_symbol, function_choice)
            dates, open_p, high_p, low_p, close_p = extract_series_for_range(
                data, start_date, end_date
            )

            chart_image = create_chart_base64(
                dates, open_p, high_p, low_p, close_p,
                selected_symbol, chart_type, start_date, end_date
            )

        except Exception as e:
            # Do not crash; show the error message on the page
            error = str(e)

    return render_template(
        "index.html",
        symbols=symbols,
        chart_image=chart_image,
        error=error,
        selected_symbol=selected_symbol,
        function_choice=function_choice,
        chart_type=chart_type,
        start_date=start_date,
        end_date=end_date,
    )


if __name__ == "__main__":
    # For local dev (not in Docker yet)
    app.run(host="0.0.0.0", port=5001, debug=True)
