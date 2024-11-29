# Native Indicators

This document describes the custom indicators implemented natively in the MT5GW package. These indicators complement the standard technical indicators available through TA-Lib, Tulip, and pandas-ta libraries.

## Available Indicators

### 1. Supertrend
```python
{"method": "supertrend", "args": ["h", "l", "c"]}
```
- **Description**: A trend-following indicator that combines ATR with basic price levels
- **Parameters**:
  - High prices ("h")
  - Low prices ("l")
  - Close prices ("c")
- **Default Settings**:
  - Period: 10
  - Multiplier: 3
- **Output**: Trend direction (1 for uptrend, -1 for downtrend) and trend levels

### 2. Time-Weighted Average Price (TWAP)
```python
{"method": "twap", "args": ["o", "h", "l", "c"]}
```
- **Description**: Calculates the average price weighted by time within each bar
- **Parameters**:
  - Open prices ("o")
  - High prices ("h")
  - Low prices ("l")
  - Close prices ("c")
- **Output**: TWAP value for each bar

### 3. Percentage of Volume (POV)
```python
{"method": "pov", "args": ["c", "v"]}
```
- **Description**: Measures the relationship between price changes and volume
- **Parameters**:
  - Close prices ("c")
  - Volume ("v")
- **Default Settings**:
  - Period: 14
- **Output**: POV ratio indicating volume-price relationship

### 4. Relative Strength Levy (RSL)
```python
{"method": "rsl", "args": ["c"]}
```
- **Description**: A momentum indicator comparing current price to historical prices
- **Parameters**:
  - Close prices ("c")
- **Default Settings**:
  - Period: 20
- **Output**: RSL value indicating relative strength

### 5. Ehlers Relative Price Index (RPI)
```python
{"method": "ehlers_rpi", "args": ["h", "l", "v"]}
```
- **Description**: Advanced price momentum indicator incorporating volume
- **Parameters**:
  - High prices ("h")
  - Low prices ("l")
  - Volume ("v")
- **Default Settings**:
  - Alpha: 0.1
- **Output**: RPI value indicating price momentum

### 6. Ultra Williams %R
```python
{"method": "ultra_wpr", "args": ["h", "l", "c"]}
```
- **Description**: Enhanced version of Williams %R with adaptive periods
- **Parameters**:
  - High prices ("h")
  - Low prices ("l")
  - Close prices ("c")
- **Default Settings**:
  - Primary Period: 14
  - Secondary Period: 28
- **Output**: Ultra WPR value and signal line

### 7. Ultra RSI
```python
{"method": "ultra_rsi", "args": ["c"]}
```
- **Description**: Enhanced RSI incorporating multiple timeframes
- **Parameters**:
  - Close prices ("c")
- **Default Settings**:
  - Primary Period: 14
  - Secondary Period: 28
- **Output**: Ultra RSI value and signal line

## Usage Example

```python
from mt5gw import MetaTraderManager

mt = MetaTraderManager()

# Fetch data with native indicators
df = mt.fetch(
    instrument="EURUSD",
    timeframe="1h",
    bars=100,
    native_indicators=[
        {"method": "supertrend", "args": ["h", "l", "c"]},
        {"method": "twap", "args": ["o", "h", "l", "c"]},
        {"method": "ultra_rsi", "args": ["c"]}
    ]
)
```

## Implementation Details

### Column Naming Convention
Native indicators follow this naming pattern:
- Single value outputs: `{indicator_name}`
- Multiple outputs: `{indicator_name}_{output_type}`

Example:
- `supertrend_direction`
- `supertrend_level`
- `ultra_rsi_value`
- `ultra_rsi_signal`

### Data Requirements
- Minimum required bars: Most indicators need at least 30 bars for accurate calculation
- Missing data handling: Forward-filled automatically
- NaN values: First few bars may contain NaN due to calculation requirements

### Performance Considerations
- Native indicators are optimized for performance
- Calculations are vectorized using NumPy operations
- Memory usage is optimized for large datasets

## Common Use Cases

1. **Trend Following**
   ```python
   native_indicators=[
       {"method": "supertrend", "args": ["h", "l", "c"]},
       {"method": "rsl", "args": ["c"]}
   ]
   ```

2. **Volume Analysis**
   ```python
   native_indicators=[
       {"method": "pov", "args": ["c", "v"]},
       {"method": "ehlers_rpi", "args": ["h", "l", "v"]}
   ]
   ```

3. **Advanced Momentum**
   ```python
   native_indicators=[
       {"method": "ultra_rsi", "args": ["c"]},
       {"method": "ultra_wpr", "args": ["h", "l", "c"]}
   ]
   ```

## Error Handling

Native indicators include robust error handling:
- Invalid parameters trigger informative exceptions
- Insufficient data is handled gracefully
- NaN values are managed appropriately

Example error handling:
```python
try:
    df = mt.fetch(
        instrument="EURUSD",
        timeframe="1h",
        bars=100,
        native_indicators=[
            {"method": "supertrend", "args": ["h", "l", "c"]}
        ]
    )
except ValueError as e:
    print(f"Invalid parameters: {e}")
except Exception as e:
    print(f"Calculation error: {e}")
```

## Best Practices

1. **Data Quality**
   - Ensure sufficient historical data
   - Check for data gaps
   - Verify price data validity

2. **Parameter Selection**
   - Start with default parameters
   - Adjust based on instrument characteristics
   - Consider timeframe when selecting periods

3. **Combination Usage**
   - Combine complementary indicators
   - Avoid redundant calculations
   - Consider computational overhead

4. **Performance Optimization**
   - Request only needed indicators
   - Use appropriate number of bars
   - Consider caching results for repeated analysis
