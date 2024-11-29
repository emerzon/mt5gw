# MT5GW Tests and Examples

This directory contains example usage and tests for the MetaTrader Gateway (MT5GW) package. These examples demonstrate the core functionality and serve as a reference for implementing your own solutions.

## Prerequisites

### System Requirements
- Windows OS (required for MetaTrader 5)
- Python 3.7 or higher
- MetaTrader 5 terminal installed and configured
- Active internet connection for market data retrieval

### MetaTrader 5 Setup
1. Install MetaTrader 5 from your broker's website
2. Log in to your trading account
3. Enable algorithmic trading:
   - Tools → Options → Expert Advisors
   - Enable "Allow automated trading"
   - Enable "Allow WebRequest for listed URL"

### Python Environment Setup
1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. Install required dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

## Files

- `example_usage.py`: Comprehensive examples demonstrating:
  - Basic initialization and connection
  - Data retrieval with different timeframes
  - Technical indicator calculations
  - Pivot level calculations
  - Wavelet denoising
  - Error handling and best practices

## Running the Examples

1. Ensure MetaTrader 5 is running and logged in
2. Activate your Python environment if using one
3. Run the example:
   ```bash
   python example_usage.py
   ```

## Understanding the Output

The examples produce several types of output:

1. **Symbol Information**: Lists available trading instruments
2. **Data Samples**: Shows DataFrame samples with various features
3. **Technical Indicators**: Demonstrates calculated indicators
4. **Pivot Levels**: Shows support and resistance levels
5. **Denoised Data**: Compares original vs. denoised price data

Each output section includes:
- Shape information (rows × columns)
- Sample data rows
- Column names and descriptions
- Relevant calculations and transformations

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify MetaTrader 5 is running
   - Check internet connection
   - Ensure MT5 is logged in to your account

2. **Symbol Not Found**
   - Verify the symbol exists in your MT5 terminal
   - Check symbol spelling and case
   - Ensure your account has access to the symbol

3. **Data Retrieval Issues**
   - Check if market is open for requested timeframe
   - Verify sufficient historical data is available
   - Ensure date range is valid

4. **Indicator Calculation Errors**
   - Verify all required dependencies are installed
   - Check input data validity
   - Ensure sufficient data points for calculation

### Debug Tips

1. Enable verbose logging:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. Verify MetaTrader connection:
   ```python
   from mt5gw import MetaTraderManager
   mt = MetaTraderManager()
   print(mt.get_terminal_info())  # Should show connection details
   ```

3. Test basic data retrieval:
   ```python
   # Simple test with minimal parameters
   df = mt.fetch("EURUSD", "1h", bars=10)
   print(df.head())
   ```

## Notes

- Examples use EURUSD as default symbol - adjust according to your needs
- Some features may require specific MT5 account types
- Data availability depends on your broker and account type
- Error handling is included to demonstrate proper exception management
- Code is commented to explain key concepts and implementation details

## Next Steps

After running these examples, you might want to:
1. Modify parameters to suit your needs
2. Implement additional technical indicators
3. Create custom data processing pipelines
4. Develop automated trading strategies

For more detailed information, refer to:
- Main package documentation
- [Data Retrieval Configuration](../docs/configuration/data_retrieval.md)
- Sample configurations in the `samples` directory
