# mt5gw: MetaTrader 5 Gateway

`mt5gw` is a comprehensive Python library that transforms MetaTrader 5 into a versatile and reliable data pipeline for machine learning (ML) applications. It simplifies the process of retrieving, enriching, and managing financial data while ensuring reproducibility across ML workflows.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Key Features](#key-features)
  - [Structured Data Retrieval](#structured-data-retrieval)
  - [Technical Indicator Integration](#technical-indicator-integration)
  - [Data Enrichment](#data-enrichment)
  - [Advanced Filtering and Smoothing](#advanced-filtering-and-smoothing)
  - [Trading and Order Management](#trading-and-order-management)
  - [Reproducibility and Workflow Integration](#reproducibility-and-workflow-integration)
- [Example Use Cases](#example-use-cases)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites
- **Python**: Ensure you have Python 3.7 or later installed. You can download it from the [official website](https://www.python.org/downloads/).
- **MetaTrader 5 Terminal**: Install and configure MetaTrader 5 on your Windows machine. Download it from the [MetaQuotes website](https://www.metatrader5.com/en/download).
- **Windows OS**: `mt5gw` is designed to work on Windows operating systems.

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/emerzon/mt5gw.git
   cd mt5gw
   ```
2. **Install from Source**
   - Run:
     ```bash
     pip install -e .
     ```

## Quick Start

### Basic Data Retrieval

To fetch basic data for a specific instrument and timeframe:

```python
from mt5gw import MetaTraderManager

# Initialize the manager
mt = MetaTraderManager()

# Fetch 100 bars of EURUSD at 1-hour intervals
df = mt.fetch(
    instrument="EURUSD",
    timeframe="1h",
    bars=100,
    add_meta_dates=True
)

print(df)
```

### Data Retrieval with Technical Indicators

To fetch data along with technical indicators:

```python
from mt5gw import MetaTraderManager

# Initialize the manager
mt = MetaTraderManager()

# Fetch 100 bars of EURUSD at 1-hour intervals with RSI and MACD indicators
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

print(df)
```

### Data Retrieval with Custom Parameters

To fetch data with custom parameters such as date ranges and open/close behaviors:

```python
from mt5gw import MetaTraderManager
import datetime

# Initialize the manager
mt = MetaTraderManager()

# Fetch EURUSD from 2023-01-01 to 2023-01-31 at 1-hour intervals
df = mt.fetch(
    instrument="EURUSD",
    timeframe="1h",
    start_date=datetime.datetime(2023, 1, 1),
    end_date=datetime.datetime(2023, 1, 31),
    add_meta_dates=True,
    open_close_behavior="open"
)

print(df)
```

## Key Features

### 1. **Structured Data Retrieval**
- **Flexible Timeframes**: Supports multiple timeframes from 1 minute to 1 month, enabling granular or broad data analysis.
- **Multi-Instrument Support**: Fetch data for one or more instruments simultaneously, with consistent and unified outputs.
- **Customizable Parameters**: Specify date ranges, bar limits, and open/close behaviors for tailored data extraction.

### 2. **Technical Indicator Integration**
- **Broad Indicator Support**: Leverages popular libraries like `ta`, `talib`, `pandas_ta`, and `tulipy` to compute a wide range of technical indicators.
- **Candle Pattern Detection**: Recognizes candlestick patterns using TA-Lib for advanced technical analysis.
- **Moving Averages and Lookbacks**: Provides methods such as Simple Moving Average (SMA), Exponential Moving Average (EMA), and customizable lookback calculations.

### 3. **Data Enrichment**
- **Pivot Levels**: Adds standard, Fibonacci, Camarilla, Woodie, and Demark pivot levels along with distances to these levels for deeper insights.
- **Meta Information**: Enhances data with metadata including day, month, hour, minute, and price summaries.
- **Support and Resistance Levels**: Calculates key support and resistance levels based on rolling windows and specific fields like close prices.

### 4. **Advanced Filtering and Smoothing**
- **Wavelet Denoising**: Applies wavelet transforms to smooth data, reducing noise and improving signal clarity.
- **Gap Analysis**: Identifies gaps between consecutive bars for anomaly detection or trading strategies.
- **Null Handling**: Fills missing values using forward-fill or back-fill techniques to ensure consistent datasets.

### 5. **Trading and Order Management**
- **Order Placement**: Simplifies placing market, limit, and stop orders with MetaTrader 5.
- **Position Management**: Facilitates fetching and managing open positions and orders for active trading.
- **Trade Execution**: Supports position closing and ensures robust order sending mechanisms.

### 6. **Reproducibility and Workflow Integration**
- **Replicable Settings**: Allows defining retrieval settings to ensure consistency between training and inference datasets.
- **Multi-Instrument Aggregation**: Combines data from multiple instruments into a unified dataset, ensuring consistency in multi-asset analysis.

## Example Use Cases
- **ML Pipeline**: Use `mt5gw` to fetch, preprocess, and enrich financial data for training predictive models.
- **Quantitative Analysis**: Perform detailed technical analysis using enriched data and advanced indicators.
- **Automated Trading**: Develop and backtest trading strategies with the included trading and order management features.

## Documentation
- [Data Retrieval Configuration](docs/configuration/data_retrieval.md): Detailed guide on configuring data retrieval parameters
- [Example Usage](tests/example_usage.py): Comprehensive examples demonstrating various features
- [Sample Configuration](samples/sample_retrieval.json): Reference configuration with common settings

## Troubleshooting

### Common Issues
1. **MetaTrader Connection Failed**
   - Ensure MetaTrader 5 terminal is running
   - Check if the symbol is available in your MT5 terminal
   - Verify your MT5 account has necessary permissions

2. **Missing Indicators**
   - Install required dependencies: `pip install ta-lib pandas-ta tulipy`
   - For TA-Lib on Windows, use: `pip install TA-Lib-binary`

3. **Data Quality Issues**
   - Verify symbol availability during the requested timeframe
   - Check for sufficient historical data in MT5
   - Ensure proper market hours for the requested instrument

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
`mt5gw` is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
