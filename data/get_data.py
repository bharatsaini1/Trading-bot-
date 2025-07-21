import MetaTrader5 as mt5
import pandas as pd
import datetime
import os

def initialize_mt5(login, password, server):
    """Initialize MetaTrader 5 connection."""
    if not mt5.initialize(login=login, password=password, server=server):
        print("initialize() failed, error code =", mt5.last_error())
        return False
    
    print("MetaTrader 5 initialized successfully.")
    print("MT5 Version :", mt5.version())
    return True

def get_data(symbol, timeframe, start_date, end_date):
    """Fetch historical data for a given symbol and timeframe."""
    # Ensure MT5 is initialized
    if not mt5.initialize():
        print("MetaTrader 5 initialization failed.")
        return None

    # Convert dates to datetime objects
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    # Fetch historical data
    rates = mt5.copy_rates_range(symbol, timeframe, start, end)

    # Shutdown MT5 connection
    mt5.shutdown()

    if rates is None:
        print("Failed to retrieve data for", symbol)
        return None

    # Convert to DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    return df

if __name__ == "__main__":
    # Replace these with your actual credentials
    login = 52219537
    password = "S25Erl$0EIHLgx"
    server = " ICMarketsSC-Demo"

    if initialize_mt5(login, password, server):
        symbol = "EURUSD"
        timeframe = mt5.TIMEFRAME_H1  # 1-hour timeframe
        start_date = "2023-01-01"
        end_date = "2023-01-31"

        data = get_data(symbol, timeframe, start_date, end_date)
        if data is not None:
            print(data.head())

            # Create filename
            filename = f"{symbol}_{start_date}_to_{end_date}.csv"

            # Save to same directory as script
            filepath = os.path.join(os.getcwd(), filename)
            data.to_csv(filepath, index=False)

            print(f"\nData saved to: {filepath}")
