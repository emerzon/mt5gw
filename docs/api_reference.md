# API Reference

This document provides detailed information about the classes, methods, and parameters available in the MT5GW package.

## MetaTraderManager

The main class for interacting with MetaTrader 5.

### Initialization

```python
from mt5gw import MetaTraderManager

mt = MetaTraderManager(
    server: str = None,
    login: int = None,
    password: str = None,
    path: str = None,
    timeout: int = 60000,
    retry_count: int = 3,
    retry_delay: int = 1000
)
```

#### Parameters
- `server` (str, optional): MetaTrader 5 server name
- `login` (int, optional): Account login number
- `password` (str, optional): Account password
- `path` (str, optional): Path to MetaTrader 5 terminal
- `timeout` (int, optional): Connection timeout in milliseconds
- `retry_count` (int, optional): Number of retry attempts
- `retry_delay` (int, optional): Delay between retries in milliseconds

### Data Retrieval Methods

#### fetch
```python
def fetch(
    self,
    instrument: str,
    timeframe: str,
    bars: int = None,
    start_dt: datetime = None,
    end_dt: datetime = None,
    **kwargs
) -> pd.DataFrame
```
Fetches historical data with optional technical indicators and features.

##### Parameters
- `instrument` (str): Trading instrument symbol
- `timeframe` (str): Time period for each bar
- `bars` (int, optional): Number of bars to retrieve
- `start_dt` (datetime, optional): Start date/time
- `end_dt` (datetime, optional): End date/time
- `**kwargs`: Additional configuration parameters

##### Returns
- pandas DataFrame containing requested data and indicators

#### get_all_symbols
```python
def get_all_symbols(self) -> List[SymbolInfo]
```
Returns list of all available trading symbols.

#### get_symbol_info
```python
def get_symbol_info(self, symbol: str) -> SymbolInfo
```
Returns detailed information about a specific symbol.

### Trading Methods

#### place_market_order
```python
def place_market_order(
    self,
    symbol: str,
    volume: float,
    order_type: str,
    stop_loss: float = None,
    take_profit: float = None,
    comment: str = "",
    magic: int = 0
) -> OrderResult
```
Places a market order.

##### Parameters
- `symbol` (str): Trading instrument
- `volume` (float): Trade volume in lots
- `order_type` (str): "buy" or "sell"
- `stop_loss` (float, optional): Stop loss price
- `take_profit` (float, optional): Take profit price
- `comment` (str, optional): Order comment
- `magic` (int, optional): Magic number

#### place_pending_order
```python
def place_pending_order(
    self,
    symbol: str,
    volume: float,
    order_type: str,
    price: float,
    stop_loss: float = None,
    take_profit: float = None,
    comment: str = "",
    magic: int = 0
) -> OrderResult
```
Places a pending order.

### Position Management Methods

#### get_open_positions
```python
def get_open_positions(
    self,
    symbol: str = None
) -> List[Position]
```
Returns list of open positions.

#### close_position
```python
def close_position(
    self,
    ticket: int,
    volume: float = None
) -> bool
```
Closes specified position.

### Account Methods

#### get_account_info
```python
def get_account_info(self) -> AccountInfo
```
Returns account information.

#### calculate_margin
```python
def calculate_margin(
    self,
    symbol: str,
    volume: float,
    order_type: str
) -> float
```
Calculates required margin for trade.

### Technical Analysis Methods

#### add_indicator
```python
def add_indicator(
    self,
    df: pd.DataFrame,
    indicator_type: str,
    **params
) -> pd.DataFrame
```
Adds technical indicator to DataFrame.

### Utility Methods

#### get_terminal_info
```python
def get_terminal_info(self) -> TerminalInfo
```
Returns MetaTrader 5 terminal information.

#### is_connected
```python
def is_connected(self) -> bool
```
Checks if connected to MetaTrader 5.

## Data Structures

### SymbolInfo
Contains trading instrument information.

#### Attributes
- `name` (str): Symbol name
- `description` (str): Symbol description
- `digits` (int): Price decimal places
- `trade_mode` (int): Trading mode
- `point` (float): Point value
- `spread` (int): Current spread
- `trade_contract_size` (float): Contract size
- `volume_min` (float): Minimum volume
- `volume_max` (float): Maximum volume
- `volume_step` (float): Volume step

### OrderResult
Contains order execution result.

#### Attributes
- `ticket` (int): Order ticket
- `volume` (float): Executed volume
- `price` (float): Execution price
- `comment` (str): Execution comment

### Position
Contains position information.

#### Attributes
- `ticket` (int): Position ticket
- `symbol` (str): Trading instrument
- `type` (int): Position type
- `volume` (float): Position volume
- `price_open` (float): Opening price
- `sl` (float): Stop loss
- `tp` (float): Take profit
- `profit` (float): Current profit
- `comment` (str): Position comment

### AccountInfo
Contains account information.

#### Attributes
- `login` (int): Account number
- `balance` (float): Account balance
- `equity` (float): Account equity
- `margin` (float): Used margin
- `margin_free` (float): Free margin
- `margin_level` (float): Margin level
- `currency` (str): Account currency

## Constants

### Timeframes
```python
TIMEFRAMES = {
    "1m": "1 minute",
    "5m": "5 minutes",
    "15m": "15 minutes",
    "30m": "30 minutes",
    "1h": "1 hour",
    "4h": "4 hours",
    "1d": "1 day",
    "1w": "1 week",
    "1mn": "1 month"
}
```

### Order Types
```python
ORDER_TYPES = {
    "buy": "Market Buy",
    "sell": "Market Sell",
    "buy_limit": "Buy Limit",
    "sell_limit": "Sell Limit",
    "buy_stop": "Buy Stop",
    "sell_stop": "Sell Stop"
}
```

## Error Handling

### MT5Error
Base exception class for MT5GW errors.

### ConnectionError
Raised when connection to MetaTrader 5 fails.

### OrderError
Raised when order placement fails.

### Example Usage
```python
from mt5gw import MetaTraderManager, MT5Error

try:
    mt = MetaTraderManager()
    df = mt.fetch("EURUSD", "1h", bars=100)
except MT5Error as e:
    print(f"MT5 error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Error Handling**
   - Always wrap operations in try-except blocks
   - Handle specific exceptions appropriately
   - Log errors for debugging

2. **Resource Management**
   - Close connections when done
   - Monitor memory usage with large datasets
   - Implement proper cleanup

3. **Performance**
   - Cache frequently used data
   - Optimize indicator calculations
   - Use appropriate timeframes

4. **Security**
   - Store credentials securely
   - Validate input parameters
   - Implement proper access controls
