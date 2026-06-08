# Trading Bot — Binance Futures Testnet (USDT-M)

A production-quality, CLI-based Python trading bot for placing orders on the **Binance Futures Testnet**. Built for clarity, modularity, and interview review — with full input validation, structured logging, and robust error handling.

**Testnet URL:** [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

---

## Project Overview

This project demonstrates a clean layered architecture for interacting with the Binance Futures API:

- **CLI layer** — parses arguments and prints user-friendly output
- **Validation layer** — enforces business rules before any API call
- **Client layer** — manages authenticated connection to the testnet
- **Order layer** — places MARKET, LIMIT, and STOP_LIMIT orders

The bot is designed to run safely on testnet only. No real funds are at risk when using testnet API keys.

---

## Features

- Place **MARKET** orders (BUY / SELL)
- Place **LIMIT** orders (BUY / SELL)
- Place **STOP_LIMIT** orders (BUY / SELL)
- Input validation with custom `ValidationError`
- Rotating file logging (`REQUEST`, `RESPONSE`, `ERROR`)
- Graceful handling of API, network, and unexpected errors
- Type hints and docstrings throughout
- PEP 8 compliant, modular package structure

---

## Folder Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py          # Package metadata
│   ├── config.py            # Environment configuration
│   ├── client.py            # Binance client wrapper
│   ├── orders.py            # Order placement logic
│   ├── validators.py        # Input validation
│   ├── logging_config.py    # Rotating file logger setup
│   └── exceptions.py        # Custom exceptions
│
├── logs/
│   └── trading_bot.log      # Application log file
│
├── .env.example             # Environment variable template
├── .gitignore
├── cli.py                   # CLI entry point
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites

- Python **3.11+**
- pip
- Binance Futures **Testnet** API key and secret

### Steps

```bash
# Clone or navigate to the project
cd trading_bot

# Create a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Setup

### 1. Create a Testnet Account

1. Visit [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in with your GitHub account
3. Generate API Key and Secret from the testnet dashboard

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

> **Never commit `.env` to version control.** It is listed in `.gitignore`.

---

## Environment Variables

| Variable             | Required | Description                          |
|----------------------|----------|--------------------------------------|
| `BINANCE_API_KEY`    | Yes      | Binance Futures Testnet API key      |
| `BINANCE_API_SECRET` | Yes      | Binance Futures Testnet API secret   |

---

## Usage Examples

All commands are run from the `trading_bot/` directory.

### Market Buy

```bash
python cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

### Market Sell

```bash
python cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --type MARKET \
  --quantity 0.001
```

### Limit Buy

```bash
python cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type LIMIT \
  --quantity 0.001 \
  --price 100000
```

### Limit Sell

```bash
python cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.001 \
  --price 120000
```

### Stop Limit Buy

```bash
python cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type STOP_LIMIT \
  --quantity 0.001 \
  --price 100000 \
  --stop-price 99000
```

### CLI Arguments

| Argument       | Required | Description                                      |
|----------------|----------|--------------------------------------------------|
| `--symbol`     | Yes      | Trading pair (e.g. `BTCUSDT`)                    |
| `--side`       | Yes      | `BUY` or `SELL`                                  |
| `--type`       | Yes      | `MARKET`, `LIMIT`, or `STOP_LIMIT`               |
| `--quantity`   | Yes      | Order quantity (must be > 0)                     |
| `--price`      | LIMIT / STOP_LIMIT | Limit price (must be > 0)              |
| `--stop-price` | STOP_LIMIT only    | Stop trigger price (must be > 0)       |

---

## Logging

Logs are written to `logs/trading_bot.log` using a `RotatingFileHandler`:

- **Max file size:** 5 MB
- **Backup count:** 3 rotated files

The `logs/` directory is created automatically on first run.

### Log Format

```
REQUEST:
symbol=BTCUSDT
side=BUY
type=MARKET
quantity=0.001

RESPONSE:
orderId=12345
status=FILLED

ERROR:
Invalid quantity
```

---

## Error Handling

The CLI catches and displays friendly messages for:

| Exception            | User Message                                      |
|----------------------|---------------------------------------------------|
| `ValidationError`    | Specific validation failure (e.g. invalid side)   |
| `BinanceAPIException`| Binance API error code and message                |
| `OrderExecutionError`| Client initialization or order execution failure|
| `ConnectionError`    | Network connection failure                        |
| `TimeoutError`       | Request timeout                                   |
| `RequestException`   | General HTTP request failure                      |
| `Exception`          | Unexpected errors (full details logged to file) |

Validation errors are raised **before** any API call is made.

---

## Assumptions

1. **Testnet only** — The client is hardcoded to `https://testnet.binancefuture.com/fapi`.
2. **USDT-M Futures** — Orders use the USDT-margined futures endpoint.
3. **One-way position mode** — Default Binance futures position mode is assumed.
4. **GTC time in force** — LIMIT and STOP_LIMIT orders use Good-Til-Cancelled.
5. **Credentials via `.env`** — API keys are loaded with `python-dotenv` at startup.
6. **Quantity precision** — The user is responsible for providing quantities that meet exchange filter rules (step size, min notional, etc.).

---

## Future Improvements

- [ ] Add `--dry-run` mode to validate without placing orders
- [ ] Support `STOP_MARKET` and `TAKE_PROFIT` order types
- [ ] Fetch and cache exchange info (symbol filters, precision)
- [ ] Add order cancellation and status query commands
- [ ] WebSocket integration for real-time fill notifications
- [ ] Unit tests with mocked Binance API responses
- [ ] Docker support for containerized deployment
- [ ] Configuration file support (YAML/TOML) alongside `.env`

---

## License

This project is provided for educational and interview demonstration purposes.
