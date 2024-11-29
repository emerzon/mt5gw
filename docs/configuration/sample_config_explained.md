# Sample Configuration Explained

This document provides a detailed explanation of the sample retrieval configuration found in `samples/sample_retrieval.json`. The configuration demonstrates a comprehensive setup for financial data retrieval and analysis.

## Basic Configuration

```json
{
  "bars": 30000,
  "fill_empty_ranges": false,
  "provide_open_bar": false
}
```
- `bars`: Retrieves 30,000 historical bars, suitable for long-term analysis and machine learning
- `fill_empty_ranges`: Disabled to maintain data authenticity
- `provide_open_bar`: Disabled to exclude incomplete current bar data

## Feature Selection

```json
{
  "talib_candle_patterns": false,
  "taf_all": false,
  "ta_all": true,
  "add_gap": false,
  "add_price_summaries": true,
  "add_meta_dates": true,
  "add_year": false
}
```
- Basic technical indicators enabled (`ta_all: true`)
- Price summaries and meta dates included for time-based analysis
- Gap analysis disabled to reduce computation overhead
- Year feature excluded to prevent data leakage in ML models

## Data Processing

```json
{
  "denoise_data": true,
  "sr_levels": [],
  "pivot_levels": 4
}
```
- Wavelet denoising enabled for cleaner price signals
- No custom support/resistance levels
- 4 pivot levels calculated for key price zone analysis

## Historical Analysis

### Lookbacks Configuration
The configuration includes lookback periods based on Fibonacci sequence for various metrics:

```json
"lookbacks": [
  {
    "field": "close",
    "periods": [1, 2, 3, 5, 7, 14, 21, 35, 56, 91, 147, 238, 385, 623],
    "ratio": true
  }
]
```
Fields analyzed:
- Close price (momentum analysis)
- Volume (participation analysis)
- Standard deviation (volatility analysis)
- TWAP (average price analysis)
- CCI trend (trend strength analysis)

Periods follow Fibonacci sequence for natural market cycle analysis.

## Moving Averages

```json
"mas": [
  {
    "method": "sma",
    "field": "close",
    "periods": [7, 14, 21, 35, 56, 91, 200, 500]
  }
]
```
Includes both SMA and EMA for:
- Price trend analysis (close price)
- Volume trend analysis (volume)
- Multiple timeframes from short-term (7) to long-term (500)

## Technical Indicators

### TA-Lib Indicators
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
Selected indicators include:
1. Momentum Indicators
   - StochRSI (combined momentum)
   - ROCR (price momentum)
   - Ultimate Oscillator
   - Williams %R

2. Trend Analysis
   - Linear Regression suite
   - Hilbert Transform indicators
   - Beta

3. Volatility Measures
   - Standard Deviation
   - Variance

### Native Indicators
```json
"native_indicators": [    
  {"method": "supertrend", "args": ["h", "l", "c"]},
  {"method": "twap", "args": ["o", "h", "l", "c"]}
]
```
Custom indicators for:
- Trend following (Supertrend)
- Price averaging (TWAP)
- Volume analysis (POV)
- Relative strength (RSL)
- Enhanced traditional indicators (Ultra WPR, Ultra RSI)

### Pandas TA Indicators
```json
"pandasta_indicators": [
  {"method": "entropy", "args": ["c"]},
  {"method": "mcgd", "args": ["c"]}
]
```
Advanced indicators for:
1. Market Structure
   - Entropy (price randomness)
   - Vertical Horizontal Filter
   - Choppiness Index

2. Price Dynamics
   - Market Gradient
   - Price Swing
   - Coppock Curve

3. Volume/Price Relationship
   - Accumulation/Distribution Oscillator
   - Relative Vigor Index

## Configuration Benefits

1. **Comprehensive Analysis**
   - Multiple timeframes
   - Various analytical approaches
   - Complementary indicators

2. **Performance Optimization**
   - Selective feature enabling
   - Efficient data processing
   - Balanced computation load

3. **ML-Ready Features**
   - Normalized indicators
   - Multiple lookback periods
   - Clean data through denoising

4. **Market Insight**
   - Price action analysis
   - Volume analysis
   - Trend strength measurement
   - Volatility assessment

## Usage Recommendations

1. **For High-Frequency Analysis**
   - Reduce lookback periods
   - Disable denoising
   - Focus on short-term indicators

2. **For Long-Term Analysis**
   - Keep Fibonacci-based lookbacks
   - Enable all trend indicators
   - Include pivot levels

3. **For ML Applications**
   - Keep denoising enabled
   - Use ratio-based lookbacks
   - Include meta dates
   - Consider removing highly correlated indicators

4. **For Performance Optimization**
   - Disable unused indicators
   - Reduce lookback periods
   - Limit pivot levels
