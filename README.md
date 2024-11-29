# mt5gw: MetaTrader 5 Gateway

`mt5gw` is a comprehensive Python library that transforms MetaTrader 5 into a versatile and reliable data pipeline for machine learning (ML) applications. It simplifies the process of retrieving, enriching, and managing financial data while ensuring reproducibility across ML workflows.

## Installation

```bash
# Install from source
git clone https://github.com/emerzon/mt5gw.git
cd mt5gw
pip install -e .
```

### Prerequisites
- Python 3.7+
- MetaTrader 5 terminal installed and configured
- Windows OS (MetaTrader 5 requirement)

## Quick Start

### Python Library Usage

```python
from mt5gw import MetaTraderManager

# Initialize the manager
mt = MetaTraderManager()

# Basic data retrieval
df = mt.fetch(
    instrument="EURUSD",
    timeframe="1h",
    bars=100,
    add_meta_dates=True
)

# Data retrieval with technical indicators
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
    ]
)
```

### REST API Usage

Start the API server:
```bash
# Start with default settings (host: 0.0.0.0, port: 8000)
mt5gw-api

# Start with custom settings
mt5gw-api --host 127.0.0.1 --port 8080 --reload
```

Example API requests:
```python
import requests

# Base URL for API endpoints
BASE_URL = "http://localhost:8000/api/v1"

# Get available symbols
symbols = requests.get(f"{BASE_URL}/symbols").json()

# Fetch market data with indicators
data = requests.post(f"{BASE_URL}/data", json={
    "instrument": "EURUSD",
    "timeframe": "1h",
    "bars": 100,
    "ta_indicators": [
        {"method": "rsi", "args": ["c"], "kwargs": {"length": 14}}
    ]
}).json()

# Place a market order
order = requests.post(f"{BASE_URL}/order", json={
    "instrument": "EURUSD",
    "order_type": "buy_market",
    "lot_size": 0.1,
    "stop_loss": 1.0500,
    "take_profit": 1.0600
}).json()
```

See [examples/api_usage.py](examples/api_usage.py) for more comprehensive API usage examples.

## Key Features

### 1. **REST API Integration**
- **Full Feature Access**: Access all MetaTrader 5 Gateway functionality through HTTP endpoints
- **Real-time Data**: Fetch market data, place orders, and manage positions via REST API
- **Swagger Documentation**: Interactive API documentation available at `/docs`
- **Cross-Platform**: Language-agnostic access to MetaTrader 5 functionality

### 2. **Structured Data Retrieval**
- **Flexible Timeframes**: Supports multiple timeframes from 1 minute to 1 month
- **Multi-Instrument Support**: Fetch data for one or more instruments simultaneously
- **Customizable Parameters**: Specify date ranges, bar limits, and open/close behaviors

### 3. **Technical Indicator Integration**
- **Broad Indicator Support**: Leverages popular libraries like `ta`, `talib`, `pandas_ta`, and `tulipy`
- **Candle Pattern Detection**: Includes recognition of candlestick patterns from TA-Lib
- **Moving Averages and Lookbacks**: Offers multiple methods such as SMA, EMA, and customizable lookbacks

### 4. **Data Enrichment**
- **Pivot Levels**: Adds standard, Fibonacci, Camarilla, Woodie, and Demark pivot levels
- **Meta Information**: Enriches data with metadata such as day, month, hour, minute
- **Support and Resistance Levels**: Calculates key levels based on rolling windows

### 5. **Advanced Filtering and Smoothing**
- **Wavelet Denoising**: Smoothens data using wavelet transforms
- **Gap Analysis**: Identifies gaps between consecutive bars
- **Null Handling**: Fills missing values with forward-fill or back-fill techniques

### 6. **Trading and Order Management**
- **Order Placement**: Simplifies placing market, limit, and stop orders
- **Position Management**: Easily fetch and manage open positions and orders
- **Trade Execution**: Supports position closing and ensures robust order sending

## API Endpoints

### Market Data
- `GET /api/v1/symbols` - Get all available trading symbols
- `GET /api/v1/timeframes` - Get supported timeframes
- `GET /api/v1/symbol/{symbol}` - Get detailed symbol information
- `GET /api/v1/tick/{symbol}` - Get latest tick data
- `POST /api/v1/data` - Fetch market data with indicators

### Trading
- `GET /api/v1/orders/{symbol}` - Get orders for a symbol
- `GET /api/v1/positions` - Get all open positions
- `POST /api/v1/order` - Place a new order
- `DELETE /api/v1/position/{ticket}` - Close a position

## Documentation
- [Data Retrieval Configuration](docs/configuration/data_retrieval.md)
- [Example Usage](tests/example_usage.py)
- [Sample Configuration](samples/sample_retrieval.json)
- API Documentation (available at `/docs` when server is running)

## Troubleshooting

### Common Issues
1. **MetaTrader Connection Failed**
   - Ensure MetaTrader 5 terminal is running
   - Check if the symbol is available in your MT5 terminal
   - Verify your MT5 account has necessary permissions

2. **Missing Indicators**
   - Install required dependencies: `pip install ta-lib pandas-ta tulipy`
   - For TA-Lib on Windows, use: `pip install TA-Lib-binary`

3. **API Server Issues**
   - Verify MetaTrader 5 is running before starting the API server
   - Check if the port is available and not blocked by firewall
   - Ensure all dependencies are installed: `pip install -e .`

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---

With its robust data management, analysis capabilities, and REST API integration, `mt5gw` bridges the gap between MetaTrader 5 and modern development workflows.
