# Trading Bot — Binance Futures Testnet (USDT-M)

A production-quality CLI-based Python trading bot for placing orders on the Binance Futures Testnet. The project demonstrates clean architecture, robust validation, structured logging, and proper exception handling.

## Project Overview

This application interacts with the Binance Futures Testnet API and supports placing multiple order types through a command-line interface.

Architecture:

- CLI Layer – Parses command-line arguments and displays results.
- Validation Layer – Validates user input before API requests.
- Client Layer – Manages authenticated Binance Testnet connection.
- Order Layer – Handles order placement logic.

The project operates exclusively on Binance Futures Testnet, ensuring no real funds are used.

---

## Features

- Place MARKET orders (BUY / SELL)
- Place LIMIT orders (BUY / SELL)
- Place STOP_LIMIT orders (BUY / SELL)
- Input validation using custom exceptions
- Structured logging with rotating log files
- Robust error handling for API and network failures
- Modular and maintainable code structure
- Type hints and documentation throughout the codebase
- PEP 8 compliant implementation

---

## Folder Structure

```text
binance-futures-trading-bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── orders.py
│   └── validators.py
│
├── logs/
│
├── .env.example
├── .gitignore
├── cli.py
├── requirements.txt
└── README.md
```

---

## Tech Stack

- Python 3
- Binance Futures Testnet API
- python-binance
- python-dotenv
- argparse
- logging

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/binance-futures-trading-bot.git

cd binance-futures-trading-bot
```

### Create Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

---

## Binance Testnet Setup

### Create Testnet Account

1. Visit:

https://testnet.binancefuture.com

2. Login using GitHub.

3. Generate a Testnet API Key and Secret.

### Configure Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Update `.env`:

```env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

---

## Usage

### MARKET BUY

```bash
python3 cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

### MARKET SELL

```bash
python3 cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --type MARKET \
  --quantity 0.001
```

### LIMIT BUY

```bash
python3 cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type LIMIT \
  --quantity 0.001 \
  --price 50000
```

### LIMIT SELL

```bash
python3 cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.001 \
  --price 70000
```

### STOP_LIMIT BUY

```bash
python3 cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type STOP_LIMIT \
  --quantity 0.001 \
  --price 66000 \
  --stop-price 65000
```

---

## Sample Output

```text
====================================
ORDER REQUEST SUMMARY
====================================

Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.001

====================================
ORDER RESPONSE
====================================

Order ID: 14506055477
Status: NEW

SUCCESS:
Order placed successfully.
```

---

## Logging

Application logs are stored in:

```text
logs/trading_bot.log
```

Logged events include:

- API requests
- API responses
- Validation failures
- Runtime errors
- Unexpected exceptions

Example:

```text
REQUEST:
symbol=BTCUSDT
side=BUY
type=MARKET

RESPONSE:
orderId=14506055477
status=NEW
```

---

## Error Handling

The application gracefully handles:

| Exception | Description |
|------------|-------------|
| ValidationError | Invalid user input |
| BinanceAPIException | Binance API errors |
| OrderExecutionError | Order placement failures |
| ConnectionError | Network connectivity issues |
| TimeoutError | Request timeout |
| RequestException | HTTP request failures |
| Exception | Unexpected runtime errors |

---

## Assumptions

1. Binance Futures Testnet is used exclusively.
2. Orders are placed on USDT-M Futures.
3. API credentials are loaded through `.env`.
4. LIMIT and STOP_LIMIT orders use GTC (Good Till Cancelled).
5. User is responsible for valid quantity precision and exchange filters.

---

## Future Improvements

- Add STOP_MARKET orders
- Add TAKE_PROFIT orders
- Implement order cancellation
- Fetch exchange filters dynamically
- Add WebSocket support
- Add unit and integration tests
- Add Docker support
- Add dry-run mode

---

## Security

- API keys are stored in `.env`
- `.env` is excluded using `.gitignore`
- No secrets are committed to source control

---

## Author
Anurag Kumar
