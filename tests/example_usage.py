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
    """
    Helper function to pretty print a sample of the dataframe with detailed information
    
    Args:
        df (pd.DataFrame): DataFrame to display
        title (str): Section title
        num_rows (int): Number of rows to display
    
    Prints:
        - DataFrame shape
        - Sample rows
        - Column names
        - Basic statistics if numerical data is present
    """
    print(f"\n=== {title} ===")
    print(f"Shape: {df.shape} (rows, columns)")
    print(f"\nFirst {num_rows} rows:")
    print("-" * 100)
    print(df.head(num_rows).to_string())
    print("-" * 100)
    print("\nColumns:", ", ".join(df.columns.tolist()))
    
    # Print basic statistics for numerical columns if present
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        print("\nBasic Statistics:")
        print(df[numeric_cols].describe().to_string())

def main():
    """
    Example usage of the MetaTrader Gateway (mt5gw) package.
    This script demonstrates various features of the package with detailed output and explanations.
    
    Key demonstrations:
    1. Basic symbol information retrieval
    2. Data retrieval with different timeframes
    3. Technical indicator calculations
    4. Pivot level analysis
    5. Wavelet denoising for noise reduction
    
    Each section includes error handling and detailed output explanation.
    """
    print("Initializing MetaTrader Manager...")
    mt = MetaTraderManager()

    # Example 1: Basic Symbol Information
    # This section demonstrates how to retrieve and display available trading instruments
    print("\n=== Example 1: Getting Symbol Information ===")
    symbols = mt.get_all_symbols()
    if symbols:
        print(f"Total available symbols: {len(symbols)}")
        print("\nFirst 3 symbols with detailed information:")
        for i, symbol in enumerate(symbols[:3], 1):
            print(f"\n{i}. {symbol.name}:")
            print(f"   - Digits: {symbol.digits} (price precision)")
            print(f"   - Trade Mode: {symbol.trade_mode} (trading rules)")
            print(f"   - Point: {symbol.point} (minimum price change)")
            print(f"   - Spread: {symbol.spread} (current spread in points)")
            if hasattr(symbol, 'description'):
                print(f"   - Description: {symbol.description}")

    # Example 2: Data Retrieval with Different Timeframes
    # Demonstrates fetching historical data with various timeframes and data enrichment
    print("\n=== Example 2: Data Retrieval ===")
    timeframes = mt.get_supported_timeframes()
    print(f"Supported timeframes: {timeframes}")
    print("\nTimeframe descriptions:")
    for tf in timeframes:
        print(f"- {tf}: {mt.get_timeframe_description(tf)}")

    try:
        # Fetch last 100 bars of EURUSD with 1-hour timeframe
        # Including meta dates helps in time-based analysis
        df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=100,
            add_meta_dates=True  # Adds hour, day, month information
        )
        print_dataframe_sample(df, "EURUSD 1H Data Sample")
        
        # Explain the meta date columns
        print("\nMeta Date Columns Explanation:")
        print("- hour: Hour of the day (0-23)")
        print("- day: Day of the month (1-31)")
        print("- month: Month of the year (1-12)")
        print("- weekday: Day of the week (0-6, Monday=0)")

    except Exception as e:
        print(f"Error fetching data: {e}")
        print("Troubleshooting tips:")
        print("1. Verify MetaTrader 5 is running")
        print("2. Check if EURUSD is available in your terminal")
        print("3. Ensure you have sufficient historical data")

    # Example 3: Technical Indicators
    # Shows how to calculate and combine various technical indicators
    print("\n=== Example 3: Technical Indicators ===")
    try:
        # Fetch data with multiple technical indicators
        df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=100,
            # RSI and MACD are momentum indicators
            talib_indicators=[
                {"method": "RSI", "args": ["c"], "kwargs": {"timeperiod": 14}},
                {"method": "MACD", "args": ["c"]}
            ],
            # Moving averages for trend analysis
            mas=[
                {"method": "SMA", "field": "close", "periods": [20, 50]}
            ],
            add_price_summaries=True  # Adds derived price metrics
        )
        print_dataframe_sample(df, "Data with Technical Indicators")
        
        # Explain the indicators
        print("\nIndicator Explanations:")
        print("1. RSI (Relative Strength Index):")
        print("   - Measures momentum and overbought/oversold conditions")
        print("   - Range: 0-100, Overbought: >70, Oversold: <30")
        
        print("\n2. MACD (Moving Average Convergence Divergence):")
        print("   - Trend-following momentum indicator")
        print("   - Components: MACD line, Signal line, and Histogram")
        
        print("\n3. Moving Averages:")
        print("   - SMA_20: Short-term trend (20-period Simple Moving Average)")
        print("   - SMA_50: Medium-term trend (50-period Simple Moving Average)")

    except Exception as e:
        print(f"Error calculating indicators: {e}")

    # Example 4: Pivot Levels
    # Demonstrates calculation of support and resistance levels
    print("\n=== Example 4: Pivot Levels ===")
    try:
        df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=100,
            pivot_levels=3  # Calculate 3 levels of support and resistance
        )
        pivot_columns = [col for col in df.columns if 'distance_to' in col]
        print_dataframe_sample(df[pivot_columns], "Pivot Level Distances")
        
        print("\nPivot Level Explanation:")
        print("- Positive distances: Price is above the pivot level")
        print("- Negative distances: Price is below the pivot level")
        print("- Larger absolute values indicate greater distance from pivot levels")

    except Exception as e:
        print(f"Error calculating pivot levels: {e}")

    # Example 5: Wavelet Denoising
    # Shows how to reduce noise in price data using wavelet transformation
    print("\n=== Example 5: Wavelet Denoising ===")
    try:
        # Original data without denoising
        df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=400,
            denoise_data=False
        )

        # Data with wavelet denoising applied
        denoised_df = mt.fetch(
            instrument="EURUSD",
            timeframe="1h",
            bars=400,
            denoise_data={
                "wavelet": "sym15",  # Symlet wavelet family
                "level": 1           # Decomposition level
            }
        )

        # Compare original vs denoised close prices
        print_dataframe_sample(df[["close"]], "Original Close Prices")
        print_dataframe_sample(denoised_df[["close"]], "Denoised Close Prices")
        
        print("\nWavelet Denoising Explanation:")
        print("- Purpose: Remove market noise while preserving important price movements")
        print("- Method: Symlet wavelet transform (sym15)")
        print("- Level 1 decomposition provides moderate noise reduction")
        print("- Compare the smoothness of the denoised prices vs original")

    except Exception as e:
        print(f"Error applying wavelet denoising: {e}")

if __name__ == "__main__":
    main()
