from typing import Dict, Any, Optional
from .client import BinanceClient
from .logging_config import get_logger

logger = get_logger("trading_bot.orders")

def build_order_params(
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: float, 
    price: Optional[float] = None, 
    stop_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Assemble the network-ready dictionary required to successfully push a Binance Futures position.
    Formats pricing and quantitive parameters aggressively ensuring trailing decimals are bounded.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "quantity": f"{quantity:.8f}"
    }
    
    if order_type == "MARKET":
        params["type"] = "MARKET"
    elif order_type == "LIMIT":
        params["type"] = "LIMIT"
        params["timeInForce"] = "GTC"
        if price is not None:
            params["price"] = f"{price:.8f}"
    elif order_type == "STOP":
        params["type"] = "STOP"
        params["timeInForce"] = "GTC"
        if price is not None:
            params["price"] = f"{price:.8f}"
        if stop_price is not None:
            params["stopPrice"] = f"{stop_price:.8f}"
            
    logger.debug(f"Structurally generated target order parameters mapped: {params}")
    return params

def place_order(client: BinanceClient, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Forward explicitly constructed order parameters toward the designated authenticated network wrapper.
    """
    logger.info(f"Issuing outbound trade routine for {params.get('symbol')} ({params.get('side')} {params.get('type')})")
    return client.place_order(**params)

def format_order_response(response: Dict[str, Any]) -> str:
    """
    Map highly structural nested JSON outputs returned seamlessly by the node into human-viable visual feedback.
    """
    order_id = response.get("orderId", "N/A")
    symbol = response.get("symbol", "N/A")
    side = response.get("side", "N/A")
    order_type = response.get("type", "N/A")
    status = response.get("status", "N/A")
    orig_qty = response.get("origQty", "N/A")
    executed_qty = response.get("executedQty", "N/A")
    avg_price = response.get("avgPrice", "N/A")
    price = response.get("price", "N/A")
    
    formatted_block = (
        f"Order ID     : {order_id}\n"
        f"Symbol       : {symbol}\n"
        f"Side         : {side}\n"
        f"Type         : {order_type}\n"
        f"Status       : {status}\n"
        f"Orig Qty     : {orig_qty}\n"
        f"Executed Qty : {executed_qty}\n"
        f"Price        : {price}\n"
        f"Avg Price    : {avg_price}"
    )
    return formatted_block
