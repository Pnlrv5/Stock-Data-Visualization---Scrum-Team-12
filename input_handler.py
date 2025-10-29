
from datetime import datetime

def get_chart_type():
    chart_type = input("Enter type of chart that is desired (line/bar):").lower().strip()
    
    #ERROR CHECKS IF THE LINE OR BAR WAS ENTERED CORRECTLY
    while chart_type != "line" and chart_type != "bar":
        print("Error, not correct line or bar was entered, try again")
        chart_type = input("Enter type of chart that is desired (line/bar):").lower().strip()

    return chart_type

def get_time_series_function():
    while True:
        choice = input("Select time series (1=Intraday, 2=Daily, 3=Weekly, 4=Monthly): ").lower().strip()
        if choice != "intraday" and choice != "daily" and choice != "weekly" and choice != "monthly":
            print("Invalid choice. Enter intraday, daily, weekly, or monthly.")
        else:
            return choice
    
def get_start_date():
    #since datetime doesnt return true or false we habe to do a while true loop
    #I attempted a while not first but it didn't like it because of that
     while True:
        start_date = input("Enter start-date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            return start_date 
        except ValueError:
            print("Invalid date. Please enter in YYYY-MM-DD format.")

def get_end_date():
    #I just copied this function from above and changed the return variable.
    while True:
        end_date = input("Enter end-date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
            return end_date 
        except ValueError:
            print("Invalid date. Please enter in YYYY-MM-DD format.")

def get_symbol():
    
    #make it uppercase and strip whitespace
    symbol = input("Enter stock Symbol: (Eample: APPL, MSFT, ABCD) ").upper().strip()
    #this error checks is its four letters and has no numbers or white space.
    while not symbol.isalpha():
        print(" Invalid symbol, needs to be four letters with no spaces.")
        symbol = input("Enter stock Symbol: (Eample: APPL, MSFT, ABCD) ").upper().strip()
    return symbol