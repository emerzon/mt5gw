import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def print_response(response):
    """Helper function to print API responses"""
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 80)

def main():
    # Get available symbols
    print("Getting available symbols...")
    response = requests.get(f"{BASE_URL}/symbols")
    print_response(response)

    # Get supported timeframes
    print("\nGetting supported timeframes...")
    response = requests.get(f"{BASE_URL}/timeframes")
    print_response(response)

    # Get symbol info
    symbol = "EURUSD"
    print(f"\nGetting symbol info for {symbol}...")
    response = requests.get(f"{BASE_URL}/symbol/{symbol}")
    print_response(response)

    # Get last tick
    print(f"\nGetting last tick for {symbol}...")
    response = requests.get(f"{BASE_URL}/tick/{symbol}")
    print_response(response)

    # Fetch market data with indicators
    print(f"\nFetching market data for {symbol}...")
    data_request = {
        "instrument": symbol,
        "timeframe": "1h",
        "bars": 100,
        "date_from": (datetime.now() - timedelta(days=7)).isoformat(),
        "date_to": datetime.now().isoformat(),
        "add_meta_dates": True,
        "add_price_summaries": True,
        "mas": [
            {
                "method": "sma",
                "field": "close",
                "periods": [14, 50]
            }
        ],
        "ta_indicators": [
            {
                "method": "rsi",
                "args": ["c"],
                "kwargs": {"length": 14}
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/data", json=data_request)
    print_response(response)

    # Get open positions
    print("\nGetting open positions...")
    response = requests.get(f"{BASE_URL}/positions")
    print_response(response)

    # Example order placement (uncomment to test)
    """
    print("\nPlacing a market order...")
    order_request = {
        "instrument": symbol,
        "order_type": "buy_market",
        "lot_size": 0.1,
        "stop_loss": 1.0500,
        "take_profit": 1.0600
    }
    response = requests.post(f"{BASE_URL}/order", json=order_request)
    print_response(response)
    """

if __name__ == "__main__":
    main()
