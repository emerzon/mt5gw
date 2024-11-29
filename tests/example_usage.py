import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mt5gw.mt5gw import MetaTraderManager
import datetime
import pandas as pd

# Configure pandas display options for better readability
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)        # Auto-detect terminal width
pd.set_option('display.precision', 4)       # Round floats to 4 decimal places
pd.set_option('display.float_format', lambda x: '%.4f' % x)  # Consistent float format

def print_dataframe_sample(df, title, num_rows=5):
    """Helper function to pretty print a sample of the dataframe"""
    print(f"\n=== {title} ===")
    print(f"Shape: {df.shape} (rows, columns)")
    print(f"\nFirst {num_rows} rows:")
    print("-" * 100)
    print(df.head(num_rows).to_string())
    print("-" * 100)
    print("\nColumns:", ", ".join(df.columns.tolist()))

def main():
    """
    Example usage of the MetaTrader Gateway (mt5gw) package.
    This script demonstrates various features of the package with pretty-printed output.
    """
    print("Initializing MetaTrader Manager...")
    mt = MetaTraderManager()

    # Example 1: Basic Symbol Information
    print("\n=== Example 1: Getting Symbol Information ===")
    symbols = mt.get_all_symbols()
    if symbols:
        print(f"Total available symbols: {len(symbols)}")
        # Print first 3 symbols' details as example
        print("\nFirst 3 symbols:")
        for i, symbol in enumerate(symbols[:3], 1):
            print(f"{i}. {symbol.name}: Digits={symbol.digits}, Trade Mode={symbol.trade_mode}")

    # Example 2: Data Retrieval with Different Timeframes
    print("\n=== Example 2: Data Retrieval ===")
    timeframes = mt.get_supported_timeframes()
    print(f"Supported timeframes: {timeframes}")

    try:
        # Fetch last 100 bars of EURUSD with 1-hour timeframe
        df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=100,
            add_meta_dates=True
        )
        print_dataframe_sample(df, "EURUSD 1H Data Sample")

    except Exception as e:
        print(f"Error fetching data: {e}")

    # Example 3: Technical Indicators
    print("\n=== Example 3: Technical Indicators ===")
    try:
        # Fetch data with various technical indicators
        df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=100,
            talib_indicators=[
                {"method": "RSI", "args": ["c"], "kwargs": {"timeperiod": 14}},
                {"method": "MACD", "args": ["c"]}
            ],
            mas=[
                {"method": "SMA", "field": "close", "periods": [20, 50]}
            ],
            add_price_summaries=True
        )
        print_dataframe_sample(df, "Data with Technical Indicators")

    except Exception as e:
        print(f"Error calculating indicators: {e}")

    # Example 4: Pivot Levels
    print("\n=== Example 4: Pivot Levels ===")
    try:
        df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=100,
            pivot_levels=3
        )
        pivot_columns = [col for col in df.columns if 'distance_to' in col]
        print_dataframe_sample(df[pivot_columns], "Pivot Level Distances")

    except Exception as e:
        print(f"Error calculating pivot levels: {e}")

    # Example 5: Wavelet Denoising
    print("\n=== Example 5: Wavelet Denoising ===")
    try:
        df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=400,
            denoise_data=False
        )

        denoised_df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=400,
            denoise_data={
                "wavelet": "sym15",
                "level": 1
            }
        )

        # Compare original vs denoised close prices
        print_dataframe_sample(df[["close"]], "Original Close Prices")
        print_dataframe_sample(denoised_df[["close"]], "Denoised Close Prices")

    except Exception as e:
        print(f"Error applying wavelet denoising: {e}")

if __name__ == "__main__":
    main()
