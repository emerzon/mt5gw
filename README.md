# mt5gw: MetaTrader 5 Gateway

`mt5gw` is a comprehensive Python library that transforms MetaTrader 5 into a versatile and reliable data pipeline for machine learning (ML) applications. It simplifies the process of retrieving, enriching, and managing financial data while ensuring reproducibility across ML workflows.

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

### Example Use Cases
- **ML Pipeline**: Use `mt5gw` to fetch, preprocess, and enrich financial data for training predictive models.
- **Quantitative Analysis**: Perform detailed technical analysis using enriched data and advanced indicators.
- **Automated Trading**: Develop and backtest trading strategies with the included trading and order management features.

---

With its robust data management and analysis capabilities, `mt5gw` bridges the gap between MetaTrader 5 and cutting-edge machine learning workflows.
