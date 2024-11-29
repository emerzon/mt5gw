from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
import pandas as pd
from datetime import datetime

from ..mt5gw import MetaTraderManager
from .models import OrderRequest, FetchDataRequest, SymbolInfo, OrderResult

router = APIRouter()
mt_manager = MetaTraderManager()

@router.get("/symbols", response_model=List[str])
async def get_symbols():
    """Get all available trading symbols"""
    try:
        symbols = mt_manager.get_all_symbols()
        return [symbol.name for symbol in symbols]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/timeframes")
async def get_timeframes():
    """Get all supported timeframes"""
    try:
        return mt_manager.get_supported_timeframes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/symbol/{symbol}", response_model=SymbolInfo)
async def get_symbol_info(symbol: str):
    """Get detailed information about a specific symbol"""
    try:
        info = mt_manager.get_symbol_info(symbol)
        if info is None:
            raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
        return SymbolInfo(
            symbol=info.name,
            point=info.point,
            digits=info.digits,
            spread=info.spread,
            trade_mode=info.trade_mode,
            trade_allowed=info.trade_allowed,
            volume_min=info.volume_min,
            volume_max=info.volume_max,
            volume_step=info.volume_step
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{symbol}")
async def get_orders(symbol: str):
    """Get all orders for a specific symbol"""
    try:
        orders = mt_manager.get_orders(symbol)
        if orders is None:
            return []
        return [order._asdict() for order in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/positions")
async def get_positions(symbol: Optional[str] = None):
    """Get all open positions, optionally filtered by symbol"""
    try:
        positions = mt_manager.get_positions(symbol)
        if positions is None:
            return []
        return [position._asdict() for position in positions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/order", response_model=OrderResult)
async def place_order(order: OrderRequest):
    """Place a new trading order"""
    try:
        result = mt_manager.place_order(order.dict(exclude_none=True))
        if result.retcode != 10009:  # MT5_TRADE_RETCODE_DONE
            raise HTTPException(status_code=400, detail=f"Order failed with code {result.retcode}")
        return OrderResult(
            retcode=result.retcode,
            deal=result.deal,
            order=result.order,
            volume=result.volume,
            price=result.price,
            bid=result.bid,
            ask=result.ask,
            comment=result.comment,
            request_id=result.request_id,
            retcode_external=result.retcode_external
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/position/{ticket}")
async def close_position(ticket: int):
    """Close an open position by ticket number"""
    try:
        result = mt_manager.close_position(ticket)
        if result is None or result.retcode != 10009:  # MT5_TRADE_RETCODE_DONE
            raise HTTPException(status_code=400, detail="Failed to close position")
        return {"status": "success", "result": result._asdict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data")
async def fetch_data(request: FetchDataRequest):
    """Fetch market data with optional indicators"""
    try:
        df = mt_manager.fetch(
            instrument=request.instrument,
            timeframe=request.timeframe,
            bars=request.bars,
            date_from=request.date_from,
            date_to=request.date_to,
            mas=request.mas or [],
            lookbacks=request.lookbacks or [],
            native_indicators=request.native_indicators or [],
            ta_indicators=request.ta_indicators or [],
            pandasta_indicators=request.pandasta_indicators or [],
            talib_indicators=request.talib_indicators or [],
            denoise_data=request.denoise_data,
            add_meta_dates=request.add_meta_dates,
            add_price_summaries=request.add_price_summaries,
            pivot_levels=request.pivot_levels
        )
        
        # Convert DataFrame to dict for JSON serialization
        return df.reset_index().to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tick/{symbol}")
async def get_last_tick(symbol: str):
    """Get the last tick data for a specific symbol"""
    try:
        tick = mt_manager.get_last_tick(symbol)
        if tick is None:
            raise HTTPException(status_code=404, detail=f"No tick data found for {symbol}")
        return tick._asdict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
