# Binance Futures Testnet Trading Bot

A command-line Python trading bot to place MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M).

## Features
- Place MARKET and LIMIT orders (BUY/SELL)
- Validates mandatory order parameters locally before making network requests
- Connects directly to the Binance Futures Testnet via REST API (No third-party Binance SDKs)
- Detailed logging of API requests, responses, and errors to log files
- Structured separation of CLI and API layers

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/NightCrawler909/binance-trading-bot.git
   cd binance-trading-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup `.env` file**
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

## Environment Variables

Open the newly created `.env` file and add your testnet API keys:
```env
BINANCE_API_KEY=your_binance_testnet_api_key
BINANCE_API_SECRET=your_binance_testnet_api_secret
```

## How to Run

Use the `cli.py` script to interact with the bot.

### MARKET Order Example
```bash
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### LIMIT Order Example
```bash
python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 95000
```

## Example Output

```text
╭─────────────────────────── Order Request Summary ────────────────────────────╮
│ Symbol: BTCUSDT                                                              │
│ Side: BUY                                                                    │
│ Type: LIMIT                                                                  │
│ Quantity: 0.001                                                              │
│ Price: 50000.0                                                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────── Order Response ───────────────────────────────╮
│ Order ID     : 13096982100                                                   │
│ Symbol       : BTCUSDT                                                       │
│ Side         : BUY                                                           │
│ Type         : LIMIT                                                         │
│ Status       : NEW                                                           │
│ Orig Qty     : 0.0010                                                        │
│ Executed Qty : 0.0000                                                        │
│ Price        : 50000.00                                                      │
│ Avg Price    : 0.00                                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
✅ Order placed successfully!
```

## Project Structure

```text
binance-trading-bot/
├── bot/                   
│   ├── __init__.py        
│   ├── client.py          # API interaction and HMAC-SHA256 signature logic
│   ├── logging_config.py  # Logger setup for writing to file and console
│   ├── orders.py          # Order parameter construction and response formatting
│   └── validators.py      # Input validation for order parameters
├── logs/                  # Ignored by Git (except sample logs)
│   ├── market_order.log   
│   └── limit_order.log    
├── cli.py                 # Typer-based CLI entry point
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── .env.example           # Example environment variables template
```

## Assumptions
- **Testnet Only:** The bot is hardcoded to use the Binance Futures Testnet (`https://demo-fapi.binance.com`). 
- **Pairs:** Operates exclusively on USDT-M futures pairs (e.g., BTCUSDT).
- **Precision:** Quantity and price values are strictly formatted defensively into floats avoiding scientific notation. Complex exchange tick-size filters are not queried live.
- **REST Implementation:** Direct HTTP calls and manual HMAC-SHA256 signing were implemented per requirements to avoid dependency on heavy off-the-shelf SDKs like `python-binance`.