# Installation and Setup Guide

This guide provides detailed instructions for installing and setting up the MT5GW package along with its dependencies.

## System Requirements

### Operating System
- Windows 10/11 (required for MetaTrader 5)
- 64-bit system recommended

### Python Environment
- Python 3.7 or higher
- pip package manager
- Virtual environment recommended

### MetaTrader 5
- MetaTrader 5 terminal installed
- Active trading account (demo or live)
- Algorithmic trading permissions enabled

## Installation Steps

### 1. Python Setup

#### Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer with "Add Python to PATH" checked
3. Verify installation:
   ```bash
   python --version
   pip --version
   ```

#### Create Virtual Environment (Recommended)
```bash
# Create new environment
python -m venv mt5gw_env

# Activate environment
# Windows
mt5gw_env\Scripts\activate

# Unix/MacOS
source mt5gw_env/bin/activate
```

### 2. MetaTrader 5 Setup

1. Download MT5
   - Get from your broker's website
   - Or download from [MetaTrader 5 website](https://www.metatrader5.com/en/download)

2. Install MT5
   - Run installer
   - Complete first-time setup
   - Log in to your trading account

3. Configure MT5 Settings
   - Tools → Options → Expert Advisors
   - Enable "Allow automated trading"
   - Enable "Allow WebRequest for listed URL"
   - Add necessary URLs if required

### 3. MT5GW Installation

#### Option 1: Install from PyPI
```bash
pip install mt5gw
```

#### Option 2: Install from Source
```bash
# Clone repository
git clone https://github.com/yourusername/mt5gw.git

# Navigate to directory
cd mt5gw

# Install in development mode
pip install -e .
```

### 4. Install Dependencies

#### Core Dependencies
```bash
pip install -r requirements.txt
```

#### Technical Analysis Libraries

1. TA-Lib Installation
   ```bash
   # Windows
   pip install TA-Lib-binary

   # Linux
   sudo apt-get install ta-lib
   pip install TA-Lib
   ```

2. Other TA Libraries
   ```bash
   pip install pandas-ta tulipy
   ```

## Verification

### 1. Test Installation
```python
from mt5gw import MetaTraderManager

# Initialize manager
mt = MetaTraderManager()

# Check connection
print(mt.get_terminal_info())
```

### 2. Test Data Retrieval
```python
# Fetch basic data
df = mt.fetch(
    instrument="EURUSD",
    timeframe="1h",
    bars=10
)
print(df.head())
```

### 3. Test Trading Functions
```python
# Get account info
account = mt.get_account_info()
print(f"Balance: {account.balance}")
```

## Troubleshooting

### Common Issues

1. **MetaTrader Connection Failed**
   - Verify MT5 is running
   - Check account login status
   - Ensure algorithmic trading is enabled

2. **TA-Lib Installation Issues**
   ```bash
   # Windows alternative installation
   pip install --index-url=https://pypi.org/simple/ TA-Lib
   ```

3. **Import Errors**
   - Check Python version compatibility
   - Verify virtual environment activation
   - Reinstall package dependencies

4. **Permission Issues**
   - Run terminal as administrator
   - Check antivirus/firewall settings
   - Verify trading permissions in MT5

### Environment Variables

Set these if needed:
```bash
# Windows
set MT5_PATH="C:\Path\To\MetaTrader5\terminal64.exe"

# Unix/MacOS
export MT5_PATH="/path/to/metatrader5/terminal64.exe"
```

## Configuration

### Basic Configuration
```python
from mt5gw import MetaTraderManager

mt = MetaTraderManager(
    server="BrokerServerName",
    login=12345,
    password="YourPassword",
    path="C:\\Path\\To\\MetaTrader5\\terminal64.exe"
)
```

### Advanced Configuration
```python
mt = MetaTraderManager(
    server="BrokerServerName",
    login=12345,
    password="YourPassword",
    path="C:\\Path\\To\\MetaTrader5\\terminal64.exe",
    timeout=60000,
    retry_count=3,
    retry_delay=1000
)
```

## Development Setup

For contributing or development:

1. Install Development Dependencies
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Setup Pre-commit Hooks
   ```bash
   pre-commit install
   ```

3. Run Tests
   ```bash
   pytest tests/
   ```

## Best Practices

1. **Virtual Environment**
   - Always use virtual environment
   - Keep dependencies updated
   - Document environment setup

2. **Security**
   - Store credentials securely
   - Use environment variables
   - Implement proper error handling

3. **Performance**
   - Monitor system resources
   - Optimize data retrieval
   - Cache frequently used data

4. **Maintenance**
   - Regular updates
   - Backup configurations
   - Monitor error logs

## Additional Resources

1. **Documentation**
   - [Data Retrieval Guide](configuration/data_retrieval.md)
   - [Trading Guide](trading.md)
   - [Sample Configurations](configuration/sample_config_explained.md)

2. **Examples**
   - [Example Usage](../tests/example_usage.py)
   - [Sample Retrieval Configuration](../samples/sample_retrieval.json)

3. **Support**
   - GitHub Issues
   - Documentation Updates
   - Community Forums
