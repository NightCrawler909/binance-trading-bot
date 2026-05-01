# Binance Futures Testnet Trading Bot

## 1. Overview
This project is a production-quality Python trading bot for the Binance Futures Testnet (USDT-M). It is implemented completely from scratch using direct HTTP REST API calls, supporting `MARKET`, `LIMIT`, and `STOP` (Stop-Limit) logic. No off-the-shelf Binance wrappers are used. 

## 2. Prerequisites
- Python 3.10+
- A Binance Futures Testnet account (and valid API Keys).

## 3. Setup Steps
1. **Clone the repo** to your local machine.
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your keys:**
   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and insert your API credentials for Binance Futures Testnet.
5. **Get Testnet API Keys:**
   Visit [https://testnet.binancefuture.com](https://testnet.binancefuture.com), log in using your Binance credentials, and automatically generate testnet API keys from the mock platform.

## 4. How to Run
Use the `cli.py` module to execute commands. Here are some real examples:

- **Market BUY:**
  ```bash
  python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
  ```
- **Limit SELL:**
  ```bash
  python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 95000
  ```
- **Stop-Limit Order:**
  ```bash
  python cli.py place-order --symbol BTCUSDT --side SELL --type STOP --quantity 0.01 --price 94000 --stop-price 94500
  ```
- **Account info:** (Check balance to verify connectivity)
  ```bash
  python cli.py account-info
  ```

## 5. Project Structure
```
trading_bot/
├── bot/
│   ├── __init__.py        # Exposes package 
│   ├── client.py          # Binance Futures Testnet API HTTP wrapper and signer
│   ├── orders.py          # Abstracted order logic (format handling & REST integration)
│   ├── validators.py      # Rigid logic to validate CLI inputs (prices, quantities, types)
│   └── logging_config.py  # Structured file/console logging instantiation
├── cli.py                 # CLI entry point (Typer-based interface)
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
└── logs/                  # Auto-created structure holding execution log outputs
```

## 6. Assumptions
- This bot uses the **USDT-M Futures Testnet** only (`testnet.binancefuture.com`).
- Quantity precision is validated locally to ensure it is generic (converted securely to strings avoiding scientific notation), but it is not aggressively validated against real-time exchange step-size filters (this is outside the requested scope).
- A Stop order specifically uses the `STOP` type in Binance (acts natively as a Stop-Limit, not an OCO). 

## 7. Logging
- **Console Output:** Outputs high-priority messages (WARNING level and above), as well as rich CLI tables for explicit command feedback. 
- **File Output:** Every HTTP request payload footprint and network response is tracked carefully via a `RotatingFileHandler`. These verbose records, perfect for system debugging, are securely written to `logs/trading_bot.log` directly at `DEBUG` level. Ensure your folder `logs/` exists locally alongside the bot.
