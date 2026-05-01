def validate_order_inputs(
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: float, 
    price: float = None, 
    stop_price: float = None
) -> dict:
    """
    Validate input parameters for an order dynamically based on the requested rules.
    Raises ValueError with a descriptive message if any criteria fail.
    Returns structurally guaranteed clean dictionary of order constraints.
    """
    # 1. Validate symbol
    if not symbol or not str(symbol).strip():
        raise ValueError("Symbol must be a non-empty string.")
    symbol_val = str(symbol).strip().upper()
    
    # 2. Validate side
    side_val = str(side).strip().upper()
    if side_val not in ("BUY", "SELL"):
        raise ValueError(f"Invalid side: '{side}'. Must be 'BUY' or 'SELL'.")
        
    # 3. Validate order type
    type_val = str(order_type).strip().upper()
    if type_val not in ("MARKET", "LIMIT", "STOP"):
        raise ValueError(f"Invalid order type: '{order_type}'. Must be 'MARKET', 'LIMIT', or 'STOP'.")
        
    # 4. Validate quantity universally as a positive float
    try:
        qty_val = float(quantity)
        if qty_val <= 0:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a positive float.")
        
    # 5. Check price conditional dependency
    price_val = None
    if type_val in ("LIMIT", "STOP"):
        if price is None:
            raise ValueError(f"Price is critically required for {type_val} orders.")
        try:
            price_val = float(price)
            if price_val <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Price must be a positive float resolving to realistic limit value.")
            
    # 6. Check conditional stop_price requirements
    stop_price_val = None
    if type_val == "STOP":
        if stop_price is None:
            raise ValueError("stop_price is explicitly required for STOP orders.")
        try:
            stop_price_val = float(stop_price)
            if stop_price_val <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("stop_price must represent a positive target float.")
            
    # Compile execution-ready result dictionary
    validated = {
        "symbol": symbol_val,
        "side": side_val,
        "order_type": type_val,
        "quantity": qty_val,
    }
    if price_val is not None:
        validated["price"] = price_val
    if stop_price_val is not None:
        validated["stop_price"] = stop_price_val
        
    return validated
