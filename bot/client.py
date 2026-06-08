"""Binance Futures Testnet client wrapper."""

from __future__ import annotations

from binance.client import Client
from binance.exceptions import BinanceAPIException

from bot.config import AppConfig, BINANCE_FUTURES_TESTNET_URL, load_config
from bot.exceptions import OrderExecutionError, ValidationError
from bot.logging_config import get_logger

logger = get_logger("client")

_client: Client | None = None


def get_client(config: AppConfig | None = None) -> Client:
    """
    Create or return a cached Binance Futures Testnet client.

    Reads API credentials from environment variables via AppConfig.
    Connects to the USDT-M Futures Testnet endpoint.

    Args:
        config: Optional pre-loaded configuration. Loaded from env if omitted.

    Returns:
        Client: Initialized python-binance client for futures testnet.

    Raises:
        ValidationError: If API credentials are missing.
        OrderExecutionError: If the client cannot be initialized.
    """
    global _client

    if _client is not None:
        return _client

    try:
        app_config = config or load_config()
    except ValidationError:
        raise

    try:
        client = Client(app_config.api_key, app_config.api_secret)
        client.FUTURES_URL = app_config.futures_url or BINANCE_FUTURES_TESTNET_URL

        # Verify connectivity with a lightweight authenticated call.
        client.futures_account()
        _client = client
        logger.info("Connected to Binance Futures Testnet successfully.")
        return _client

    except BinanceAPIException as exc:
        logger.error("ERROR:\n%s", exc)
        raise OrderExecutionError(
            f"Failed to connect to Binance Futures Testnet: {exc.message}"
        ) from exc
    except Exception as exc:
        logger.error("ERROR:\n%s", exc, exc_info=True)
        raise OrderExecutionError(
            f"Unexpected error while initializing Binance client: {exc}"
        ) from exc


def reset_client() -> None:
    """Reset the cached client instance. Useful for testing."""
    global _client
    _client = None
