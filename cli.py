#!/usr/bin/env python3
"""CLI entry point for the Binance Futures Testnet trading bot."""

import argparse
import sys

from binance.exceptions import BinanceAPIException
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import RequestException, Timeout

from bot.client import get_client
from bot.exceptions import OrderExecutionError, ValidationError
from bot.logging_config import get_logger, setup_logging
from bot.orders import place_order
from bot.validators import OrderParams, validate_order_params

logger = get_logger("cli")

SEPARATOR = "===================================="


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet (USDT-M) Trading Bot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  Market Buy:\n"
            "    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001\n\n"
            "  Limit Sell:\n"
            "    python cli.py --symbol BTCUSDT --side SELL --type LIMIT "
            "--quantity 0.001 --price 120000\n\n"
            "  Stop Limit Buy:\n"
            "    python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT "
            "--quantity 0.001 --price 100000 --stop-price 99000"
        ),
    )
    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g. BTCUSDT)",
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        dest="order_type",
        required=True,
        choices=["MARKET", "LIMIT", "STOP_LIMIT", "market", "limit", "stop_limit"],
        help="Order type: MARKET, LIMIT, or STOP_LIMIT",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity (must be > 0)",
    )
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Limit price (required for LIMIT and STOP_LIMIT orders)",
    )
    parser.add_argument(
        "--stop-price",
        dest="stop_price",
        type=float,
        default=None,
        help="Stop trigger price (required for STOP_LIMIT orders)",
    )
    return parser


def print_request_summary(params: OrderParams) -> None:
    """Print a formatted order request summary to stdout."""
    print(SEPARATOR)
    print("ORDER REQUEST SUMMARY")
    print(SEPARATOR)
    print(f"Symbol: {params.symbol}")
    print(f"Side: {params.side}")
    print(f"Type: {params.order_type}")
    print(f"Quantity: {params.quantity}")
    if params.price is not None:
        print(f"Price: {params.price}")
    if params.stop_price is not None:
        print(f"Stop Price: {params.stop_price}")
    print()


def print_order_response(result: dict) -> None:
    """Print a formatted order response to stdout."""
    print(SEPARATOR)
    print("ORDER RESPONSE")
    print(SEPARATOR)
    print(f"Order ID: {result.get('orderId', 'N/A')}")
    print(f"Status: {result.get('status', 'N/A')}")
    print(f"Executed Qty: {result.get('executedQty', 'N/A')}")
    print(f"Average Price: {result.get('avgPrice', 'N/A')}")
    print()
    print("SUCCESS:")
    print("Order placed successfully.")
    print()


def print_error(message: str) -> None:
    """Print a formatted error message to stdout."""
    print()
    print("ERROR:")
    print(message)
    print()


def run(args: argparse.Namespace) -> int:
    """
    Execute the trading bot CLI workflow.

    Args:
        args: Parsed command-line arguments.

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    setup_logging()

    try:
        params = validate_order_params(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except ValidationError as exc:
        logger.error("ERROR:\n%s", exc.message)
        print_error(exc.message)
        return 1

    print_request_summary(params)

    try:
        client = get_client()
        result = place_order(client, params)
        print_order_response(result)
        return 0

    except ValidationError as exc:
        logger.error("ERROR:\n%s", exc.message)
        print_error(exc.message)
        return 1

    except BinanceAPIException as exc:
        message = f"Binance API error ({exc.code}): {exc.message}"
        logger.error("ERROR:\n%s", message, exc_info=True)
        print_error(message)
        return 1

    except OrderExecutionError as exc:
        logger.error("ERROR:\n%s", exc.message, exc_info=True)
        print_error(exc.message)
        return 1

    except (RequestsConnectionError, ConnectionError) as exc:
        message = "Network connection failed. Check your internet connection."
        logger.error("ERROR:\n%s\n%s", message, exc, exc_info=True)
        print_error(message)
        return 1

    except (Timeout, TimeoutError) as exc:
        message = "Request timed out. Please try again later."
        logger.error("ERROR:\n%s\n%s", message, exc, exc_info=True)
        print_error(message)
        return 1

    except RequestException as exc:
        message = f"HTTP request failed: {exc}"
        logger.error("ERROR:\n%s", message, exc_info=True)
        print_error(message)
        return 1

    except Exception as exc:
        message = f"An unexpected error occurred: {exc}"
        logger.error("ERROR:\n%s", message, exc_info=True)
        print_error(message)
        return 1


def main() -> None:
    """Parse arguments and run the CLI."""
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(run(args))


if __name__ == "__main__":
    main()
