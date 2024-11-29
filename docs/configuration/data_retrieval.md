# Data Retrieval Configuration

This document provides a detailed explanation of the parameters in the data retrieval configuration, extracted from analyzing the library code. These parameters enable powerful, customizable data retrieval and preprocessing for financial analysis and machine learning workflows.

---

## General Parameters

### `bars`
- **Type**: Integer
- **Description**: Specifies the number of historical bars (candlesticks) to retrieve.
- **Default**: `None` (fetch all available bars within the date range if not specified)
- **Example**: `"bars": 30000`

---

### `fill_empty_ranges`
- **Type**: Boolean
- **Description**: When `true`, fills missing time intervals with data to ensure continuous time series, using forward-fill for prices and `0` for volume.
- **Default**: `false`

---

### `talib_candle_patterns`
- **Type**: Boolean
- **Description**: Enables detection of candlestick patterns using TA-Lib's pattern recognition functions.
- **Default**: `false`
- **Notes**: Useful for identifying trend reversal signals and other market conditions.

---

### `taf_all`
- **Type**: Boolean
- **Description**: Adds all available technical indicators from the `ta` library.
- **Default**: `false`
- **Impact**: If enabled, automatically computes a wide range of features, which can increase computation time.

---

### `ta_all`
- **Type**: Boolean
- **Description**: Adds all indicators from the `ta` library to the dataset.
- **Default**: `true`
- **Usage**: Ideal for comprehensive analysis when specific indicators are not predetermined.

---

### `add_gap`
- **Type**: Boolean
- **Description**: Adds a column that calculates the price gap between the current bar’s open and the previous bar’s close.
- **Default**: `false`
- **Use Case**: Identify and analyze market anomalies or trading opportunities.

---

### `add_price_summaries`
- **Type**: Boolean
- **Description**: Adds summary features such as:
  - **`avgPrice`**: Average of high and low prices.
  - **`ohlcPrice`**: Mean of open, high, low, and close prices.
  - **`range`**: Difference between high and low prices.
  - **`momentum`**: Difference between open and close prices.
- **Default**: `true`

---

### `add_meta_dates`
- **Type**: Boolean
- **Description**: Adds metadata such as:
  - Minute (`minute`), hour (`hour`), day (`day`), month (`month`), and weekday (`weekday`) extracted from the bar timestamp.
- **Default**: `true`

---

### `add_year`
- **Type**: Boolean
- **Description**: Adds the year as a metadata feature to the dataset.
- **Default**: `false`

---

### `denoise_data`
- **Type**: Boolean
- **Description**: Applies wavelet-based smoothing to reduce noise in the dataset.
- **Default**: `true`
- **Customization**:
  - **Wavelet type**: Default is `'sym15'`.
  - **Decomposition level**: Default is `2`.

---

### `sr_levels`
- **Type**: List of Integers
- **Description**: Specifies rolling window lengths to compute support and resistance levels based on specified fields (e.g., close prices).
- **Default**: `[]`

---

### `pivot_levels`
- **Type**: Integer
- **Description**: Number of pivot levels to calculate using various methods, including:
  - **Standard**: Based on high, low, and close prices.
  - **Fibonacci**: Adds retracement levels.
  - **Camarilla**: Emphasizes tighter levels for intraday trading.
  - **Woodie's**: Incorporates opening price into calculations.
  - **Demark's**: Adjusts for different opening and closing conditions.
- **Default**: `0` (disabled)

---

## Lookback Features

### `lookbacks`
- **Type**: List of Objects
- **Description**: Computes features over specified lookback periods for selected fields.
- **Attributes**:
  - **`field`**: Target column (e.g., close, volume).
  - **`periods`**: List of lookback windows.
  - **`ratio`**: If `true`, computes ratios between current and historical values; otherwise, computes absolute differences.
- **Default**: `[]`
- **Example**:
    ```json
    "lookbacks": [
        {
            "field": "close",
            "periods": [1, 2, 3, 5, 7],
            "ratio": true
        }
    ]
    ```

---

## Moving Averages

### `mas`
- **Type**: List of Objects
- **Description**: Defines moving averages to calculate for specified fields and periods.
- **Attributes**:
  - **`method`**: Method for calculating moving averages (e.g., SMA, EMA).
  - **`field`**: Target column (e.g., close, volume).
  - **`periods`**: List of time periods for moving averages.
- **Example**:
    ```json
    "mas": [
        {
            "method": "sma",
            "field": "close",
            "periods": [7, 14, 21]
        }
    ]
    ```

---

## Technical Indicators

### `talib_indicators`
- **Type**: List of Objects
- **Description**: Configures indicators from TA-Lib with methods, arguments, and keyword arguments.
- **Example**:
    ```json
    "talib_indicators": [
        {
            "method": "STOCHRSI",
            "args": ["c"],
            "kwargs": {
                "timeperiod": 14,
                "fastk_period": 5,
                "fastd_period": 3,
                "fastd_matype": 0
            }
        }
    ]
    ```

---

### `tulip_indicators`
- **Type**: List
- **Description**: Specifies Tulip indicators to calculate.
- **Default**: `[]`

---

### `native_indicators`
- **Type**: List of Objects
- **Description**: Adds custom or library-specific indicators.
- **Example**:
    ```json
    "native_indicators": [
        {
            "method": "supertrend",
            "args": ["h", "l", "c"]
        }
    ]
    ```

---

### `pandasta_indicators`
- **Type**: List of Objects
- **Description**: Defines indicators from `pandas_ta` library.
- **Example**:
    ```json
    "pandasta_indicators": [
        {
            "method": "entropy",
            "args": ["c"]
        }
    ]
    ```

---

## Miscellaneous

### `provide_open_bar`
- **Type**: Boolean
- **Description**: Includes the open bar in the dataset if `true`.
- **Default**: `false`

---

## Usage Notes
- The configuration enables efficient and consistent feature engineering for ML workflows.
- Default values minimize computation for basic setups, while customizations allow tailored use cases.
- Comprehensive preprocessing ensures compatibility with machine learning models and trading strategies.

This configuration allows advanced data enrichment and technical analysis, supporting applications in automated trading, strategy backtesting, and predictive modeling.
