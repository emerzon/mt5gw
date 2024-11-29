# Trading with MT5GW

This document describes the trading functionality provided by the MT5GW package, including order placement, position management, and trade execution.

## Order Types

### Market Orders
```python
from mt5gw import MetaTraderManager

mt = MetaTraderManager()

# Place market buy order
result = mt.place_market_order(
    symbol="EURUSD",
    volume=0.1,  # 0.1 lots
    order_type="buy",
    comment="Market buy order"
)

# Place market sell order
result = mt.place_market_order(
    symbol="EURUSD",
    volume=0.1,
    order_type="sell",
    comment="Market sell order"
)
```

### Pending Orders
```python
# Place limit buy order
result = mt.place_pending_order(
    symbol="EURUSD",
    volume=0.1,
    order_type="buy_limit",
    price=1.0500,  # Limit price
    comment="Limit buy order"
)

# Place stop sell order
result = mt.place_pending_order(
    symbol="EURUSD",
    volume=0.1,
    order_type="sell_stop",
    price=1.0600,
    comment="Stop sell order"
)
```

## Position Management

### Fetching Positions
```python
# Get all open positions
positions = mt.get_open_positions()

# Get positions for specific symbol
positions = mt.get_open_positions(symbol="EURUSD")

# Get position by ticket
position = mt.get_position(ticket=12345)
```

### Modifying Positions
```python
# Modify stop loss and take profit
result = mt.modify_position(
    ticket=12345,
    stop_loss=1.0450,
    take_profit=1.0650
)

# Partial close
result = mt.close_position(
    ticket=12345,
    volume=0.05  # Close half of 0.1 lot position
)
```

### Closing Positions
```python
# Close single position
result = mt.close_position(ticket=12345)

# Close all positions for a symbol
result = mt.close_positions(symbol="EURUSD")

# Close all positions
result = mt.close_all_positions()
```

## Order Management

### Fetching Orders
```python
# Get all pending orders
orders = mt.get_pending_orders()

# Get orders for specific symbol
orders = mt.get_pending_orders(symbol="EURUSD")

# Get order by ticket
order = mt.get_order(ticket=12345)
```

### Modifying Orders
```python
# Modify pending order
result = mt.modify_order(
    ticket=12345,
    price=1.0550,
    stop_loss=1.0450,
    take_profit=1.0650
)
```

### Canceling Orders
```python
# Cancel single order
result = mt.cancel_order(ticket=12345)

# Cancel all orders for a symbol
result = mt.cancel_orders(symbol="EURUSD")

# Cancel all pending orders
result = mt.cancel_all_orders()
```

## Risk Management

### Position Sizing
```python
# Calculate position size based on risk percentage
size = mt.calculate_position_size(
    symbol="EURUSD",
    risk_percent=1.0,  # Risk 1% of account
    stop_loss_pips=50
)
```

### Account Information
```python
# Get account details
account = mt.get_account_info()
print(f"Balance: {account.balance}")
print(f"Equity: {account.equity}")
print(f"Margin Level: {account.margin_level}%")
```

## Error Handling

```python
from mt5gw.exceptions import MT5Error

try:
    result = mt.place_market_order(
        symbol="EURUSD",
        volume=0.1,
        order_type="buy"
    )
except MT5Error as e:
    print(f"Trading error: {e}")
    # Handle specific error cases
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle other errors
```

## Best Practices

1. **Order Validation**
   - Always verify symbol availability
   - Check sufficient margin before trading
   - Validate price levels for pending orders

2. **Position Management**
   - Use stop loss for risk management
   - Monitor position exposure
   - Implement position sizing rules

3. **Error Handling**
   - Implement comprehensive error handling
   - Log trading activities
   - Monitor order execution results

4. **Risk Management**
   - Set maximum position sizes
   - Monitor total exposure
   - Implement drawdown limits

## Common Issues

1. **Invalid Price Levels**
   ```python
   # Check if price level is valid
   if mt.is_valid_price(symbol="EURUSD", price=1.0500):
       # Place order
       pass
   ```

2. **Insufficient Margin**
   ```python
   # Check margin before trading
   if mt.check_margin(symbol="EURUSD", volume=0.1):
       # Place order
       pass
   ```

3. **Symbol Trading Hours**
   ```python
   # Check if symbol is tradeable
   if mt.is_symbol_tradeable("EURUSD"):
       # Place order
       pass
   ```

## Example Trading Strategy

```python
class SimpleMAStrategy:
    def __init__(self, mt_manager):
        self.mt = mt_manager
        
    def check_signals(self, symbol="EURUSD"):
        # Get data with moving averages
        df = self.mt.fetch(
            instrument=symbol,
            timeframe="1h",
            bars=100,
            mas=[
                {"method": "sma", "field": "close", "periods": [20, 50]}
            ]
        )
        
        # Check for crossover
        if df["SMA_20"].iloc[-1] > df["SMA_50"].iloc[-1] and \
           df["SMA_20"].iloc[-2] <= df["SMA_50"].iloc[-2]:
            # MA crossover - buy signal
            self._execute_trade(symbol, "buy")
            
        elif df["SMA_20"].iloc[-1] < df["SMA_50"].iloc[-1] and \
             df["SMA_20"].iloc[-2] >= df["SMA_50"].iloc[-2]:
            # MA crossover - sell signal
            self._execute_trade(symbol, "sell")
    
    def _execute_trade(self, symbol, direction):
        try:
            # Close existing positions
            self.mt.close_positions(symbol=symbol)
            
            # Calculate position size
            size = self.mt.calculate_position_size(
                symbol=symbol,
                risk_percent=1.0,
                stop_loss_pips=50
            )
            
            # Place new order
            result = self.mt.place_market_order(
                symbol=symbol,
                volume=size,
                order_type=direction,
                stop_loss_pips=50,
                take_profit_pips=100,
                comment=f"MA Crossover {direction}"
            )
            
            print(f"Trade executed: {result}")
            
        except Exception as e:
            print(f"Error executing trade: {e}")
```

## Safety Considerations

1. **Network Reliability**
   - Implement retry mechanisms
   - Handle connection interruptions
   - Monitor order execution status

2. **Price Validation**
   - Check for price gaps
   - Validate stop loss/take profit levels
   - Monitor slippage

3. **Risk Limits**
   - Implement maximum position sizes
   - Set daily loss limits
   - Monitor overall exposure

4. **System Health**
   - Check MetaTrader connection
   - Monitor system resources
   - Implement failsafes
