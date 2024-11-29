from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class OrderRequest(BaseModel):
    instrument: str
    order_type: str = Field(..., description="One of: buy_market, sell_market, buy_limit, sell_limit, buy_stop, sell_stop")
    lot_size: float
    entry_level: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    magic: Optional[int] = 2121
    expiration: Optional[int] = None
    comment: Optional[str] = None

class FetchDataRequest(BaseModel):
    instrument: str
    timeframe: str = Field(..., description="One of: 1min, 5min, 15min, 30min, 1h, 4h, 1d, 1w, 1m")
    bars: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    mas: Optional[List[Dict[str, Any]]] = []
    lookbacks: Optional[List[Dict[str, Any]]] = []
    native_indicators: Optional[List[Dict[str, Any]]] = []
    ta_indicators: Optional[List[Dict[str, Any]]] = []
    pandasta_indicators: Optional[List[Dict[str, Any]]] = []
    talib_indicators: Optional[List[Dict[str, Any]]] = []
    denoise_data: Optional[Dict[str, Any]] = None
    add_meta_dates: Optional[bool] = False
    add_price_summaries: Optional[bool] = True
    pivot_levels: Optional[int] = 0

class SymbolInfo(BaseModel):
    symbol: str
    point: float
    digits: int
    spread: float
    trade_mode: int
    trade_allowed: bool
    volume_min: float
    volume_max: float
    volume_step: float

class OrderResult(BaseModel):
    retcode: int
    deal: Optional[int] = None
    order: Optional[int] = None
    volume: Optional[float] = None
    price: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    comment: Optional[str] = None
    request_id: Optional[int] = None
    retcode_external: Optional[int] = None
    message: Optional[str] = None
