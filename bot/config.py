"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from bot.exceptions import ValidationError

load_dotenv()

BINANCE_FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"

VALID_SIDES = frozenset({"BUY", "SELL"})
VALID_ORDER_TYPES = frozenset({"MARKET", "LIMIT", "STOP_LIMIT"})


@dataclass(frozen=True)
class AppConfig:
    """Immutable application configuration."""

    api_key: str
    api_secret: str
    futures_url: str = BINANCE_FUTURES_TESTNET_URL


def load_config() -> AppConfig:
    """
    Load and validate configuration from environment variables.

    Returns:
        AppConfig: Validated application configuration.

    Raises:
        ValidationError: If required environment variables are missing or empty.
    """
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key:
        raise ValidationError("BINANCE_API_KEY is required. Set it in your .env file.")
    if not api_secret:
        raise ValidationError(
            "BINANCE_API_SECRET is required. Set it in your .env file."
        )

    return AppConfig(api_key=api_key, api_secret=api_secret)
