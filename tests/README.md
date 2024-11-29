# MT5GW Tests and Examples

This directory contains example usage and tests for the MetaTrader Gateway (MT5GW) package.

## Files

- `example_usage.py`: Demonstrates various features of the package including:
  - Basic initialization and connection
  - Data retrieval with different timeframes
  - Technical indicator calculations
  - Pivot level calculations
  - Wavelet denoising

## Running the Examples

1. Ensure you have MetaTrader 5 installed and running
2. Install required dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
3. Run the example:
   ```bash
   python example_usage.py
   ```

## Notes

- The examples assume you have MetaTrader 5 installed and properly configured
- Some examples use EURUSD symbol - make sure this symbol is available in your MetaTrader 5 terminal
- Error handling is included to gracefully handle cases where MetaTrader 5 is not running or symbols are not available
