# mt5gw: MetaTrader 5 Gateway

`mt5gw` is a comprehensive Python library that transforms MetaTrader 5 into a versatile and reliable data pipeline for machine learning (ML) applications. It simplifies the process of retrieving, enriching, and managing financial data while ensuring reproducibility across ML workflows.

## Installation

```bash
# Install from PyPI
pip install mt5gw

# Or install from source
git clone https://github.com/emerzon/mt5gw.git
cd mt5gw
pip install -e .
```

### Prerequisites
- Python 3.7+
- MetaTrader 5 terminal installed and configured
- Windows OS (MetaTrader 5 requirement)

## Quick Start

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

## Key Features

### 1. **Structured Data Retrieval**
- **Flexible Timeframes**: Supports multiple timeframes from 1 minute to 1 month, enabling granular or broad data analysis.
- **Multi-Instrument Support**: Fetch data for one or more instruments simultaneously, with consistent and unified outputs.
- **Customizable Parameters**: Specify date ranges, bar limits, and open/close behaviors for tailored data extraction.

### 2. **Technical Indicator Integration**
- **Broad Indicator Support**: Leverages popular libraries like `ta`, `talib`, `pandas_ta`, and `tulipy` for comprehensive technical indicator computation.
- **Candle Pattern Detection**: Includes recognition of candlestick patterns from TA-Lib for advanced technical analysis.
- **Moving Averages and Lookbacks**: Offers multiple methods such as SMA, EMA, and customizable lookback calculations.

### 3. **Data Enrichment**
- **Pivot Levels**: Adds standard, Fibonacci, Camarilla, Woodie, and Demark pivot levels, along with distances to these levels for deeper insights.
- **Meta Information**: Enriches data with metadata such as day, month, hour, minute, and price summaries.
- **Support and Resistance Levels**: Calculates key levels based on rolling windows and specific fields like close prices.

### 4. **Advanced Filtering and Smoothing**
- **Wavelet Denoising**: Smoothens data using wavelet transforms for noise reduction and improved signal clarity.
- **Gap Analysis**: Identifies gaps between consecutive bars for anomaly detection or trading strategies.
- **Null Handling**: Fills missing values with forward-fill or back-fill techniques for consistent datasets.

### 5. **Trading and Order Management**
- **Order Placement**: Simplifies placing market, limit, and stop orders with MetaTrader 5.
- **Position Management**: Easily fetch and manage open positions and orders for active trading.
- **Trade Execution**: Supports position closing and ensures robust order sending mechanisms.

### 6. **Reproducibility and Workflow Integration**
- **Replicable Settings**: Define retrieval settings to ensure consistency between training and inference datasets.
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

---

With its robust data management and analysis capabilities, `mt5gw` bridges the gap between MetaTrader 5 and cutting-edge machine learning workflows.
