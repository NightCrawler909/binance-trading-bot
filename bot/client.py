import os
import hmac
import hashlib
import time
from urllib.parse import urlencode
import httpx
from typing import Dict, Any, Optional

from .logging_config import get_logger

logger = get_logger("trading_bot.client")

class BinanceAPIError(Exception):
    """Custom exception raised for structurally valid but functionally failed Binance API messages."""
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"Binance API Error [{code}]: {msg}")

class BinanceClient:
    """HTTP Client wrapper connecting securely and exclusively to the Binance Futures Testnet."""
    BASE_URL = "https://demo-fapi.binance.com"
    
    def __init__(self):
        """
        Initialize HTTP client, resolving keys from OS environment directly.
        Raises RuntimeError strictly to prevent unauthorized ghost execution.
        """
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        
        if not self.api_key or not self.api_secret:
            raise RuntimeError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in the environment. "
                "Ensure your .env file is loaded and structured correctly."
            )
            
        self.session = httpx.Client(base_url=self.BASE_URL)
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })
        
    def _sign(self, params: Dict[str, Any]) -> str:
        """Sign request strings using HMAC-SHA256 according to Binance security policies."""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            msg=query_string.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return signature

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, signed: bool = False) -> Dict[str, Any]:
        """Base request router responsible for appending cryptographic headers and tracking."""
        if params is None:
            params = {}
            
        # Safely log footprint context before inserting active network payload timestamps or signatures
        logger.debug(f"HTTP Outbound {method} {endpoint} | Raw Params Filtered: {params}")
        
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["recvWindow"] = 5000 
            params["signature"] = self._sign(params)
            
        try:
            if method.upper() == "GET":
                response = self.session.get(endpoint, params=params)
            else:
                response = self.session.request(method, endpoint, params=params)
                
            # Keep aggressive track of body results regardless of structural integrity
            logger.debug(f"HTTP Inbound {response.status_code} | Body: {response.text}")
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            try:
                error_data = e.response.json()
                if "code" in error_data and "msg" in error_data:
                    raise BinanceAPIError(error_data["code"], error_data["msg"])
            except ValueError:
                pass 
            raise ConnectionError(f"HTTP Error {e.response.status_code} on {method} {endpoint}: {e.response.text}") from e
        except httpx.RequestError as e:
            logger.error(f"Transport block failure detected while reaching Binance testnet: {str(e)}")
            raise ConnectionError(f"Network error routing request to {method} {endpoint}: {str(e)}") from e

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, signed: bool = False) -> Dict[str, Any]:
        """Perform a standard GET call internally."""
        return self._request("GET", endpoint, params, signed)

    def _post(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a standard POST call (Always signed by Binance standards)."""
        return self._request("POST", endpoint, params, signed=True)

    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch static rules mapping the exchange (ticks, lots, etc).
        If symbol passed, filters internally locally via API target node args.
        """
        params = {"symbol": symbol} if symbol else {}
        return self._get("/fapi/v1/exchangeInfo", params=params, signed=False)

    def get_account(self) -> Dict[str, Any]:
        """Retrive real user account position mapping properties (funds dict tree)."""
        return self._get("/fapi/v2/account", params={}, signed=True)

    def place_order(self, **kwargs) -> Dict[str, Any]:
        """Submit the transaction logic immediately towards the node endpoint."""
        return self._post("/fapi/v1/order", params=kwargs)
