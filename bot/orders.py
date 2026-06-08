"""Order placement layer for Binance Futures Testnet."""

from __future__ import annotations

from typing import Any

from binance.client import Client

from bot.logging_config import get_logger
from bot.validators import OrderParams

logger = get_logger("orders")


def _log_request(params: OrderParams, extra: dict[str, Any] | None = None) -> None:
    lines = [
        "REQUEST:",
        f"symbol={params.symbol}",
        f"side={params.side}",
        f"type={params.order_type}",
        f"quantity={params.quantity}",
    ]
    if params.price is not None:
        lines.append(f"price={params.price}")
    if params.stop_price is not None:
        lines.append(f"stopPrice={params.stop_price}")
    if extra:
        for key, value in extra.items():
            lines.append(f"{key}={value}")
    logger.info("\n".join(lines))


def _log_response(response: dict[str, Any]) -> None:
    order_id = response.get("orderId", "N/A")
    status = response.get("status", "N/A")
    logger.info("RESPONSE:\norderId=%s\nstatus=%s", order_id, status)


def _parse_order_response(response: dict[str, Any]) -> dict[str, Any]:
    """
    Extract key fields from a Binance futures order response.

    Args:
        response: Raw API response dictionary.

    Returns:
        dict: Structured order result with orderId, status, executedQty, avgPrice.
    """
    executed_qty = response.get("executedQty") or response.get("cumQty") or "0"
    avg_price = response.get("avgPrice") or response.get("price") or "0"

    if float(executed_qty) == 0:
        executed_qty = response.get("origQty", executed_qty)

    return {
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": executed_qty,
        "avgPrice": avg_price,
        "raw": response,
    }


def place_market_order(client: Client, params: OrderParams) -> dict[str, Any]:
    """
    Place a MARKET order on Binance Futures Testnet.

    Args:
        client: Authenticated Binance client.
        params: Validated order parameters.

    Returns:
        dict: Structured order response.
    """
    _log_request(params)

    response = client.futures_create_order(
        symbol=params.symbol,
        side=params.side,
        type="MARKET",
        quantity=params.quantity,
    )

    _log_response(response)
    return _parse_order_response(response)


def place_limit_order(client: Client, params: OrderParams) -> dict[str, Any]:
    """
    Place a LIMIT order on Binance Futures Testnet.

    Args:
        client: Authenticated Binance client.
        params: Validated order parameters (price required).

    Returns:
        dict: Structured order response.
    """
    _log_request(params)

    response = client.futures_create_order(
        symbol=params.symbol,
        side=params.side,
        type="LIMIT",
        timeInForce="GTC",
        quantity=params.quantity,
        price=params.price,
    )

    _log_response(response)
    return _parse_order_response(response)


def place_stop_limit_order(client: Client, params: OrderParams) -> dict[str, Any]:
    """
    Place a STOP_LIMIT order on Binance Futures Testnet.

    Uses Binance futures STOP order type (stop-limit).

    Args:
        client: Authenticated Binance client.
        params: Validated order parameters (price and stop_price required).

    Returns:
        dict: Structured order response.
    """
    _log_request(params)

    response = client.futures_create_order(
        symbol=params.symbol,
        side=params.side,
        type="STOP",
        timeInForce="GTC",
        quantity=params.quantity,
        price=params.price,
        stopPrice=params.stop_price,
    )

    _log_response(response)
    return _parse_order_response(response)


def place_order(client: Client, params: OrderParams) -> dict[str, Any]:
    """
    Route order placement to the appropriate handler based on order type.

    Args:
        client: Authenticated Binance client.
        params: Validated order parameters.

    Returns:
        dict: Structured order response.
    """
    if params.order_type == "MARKET":
        return place_market_order(client, params)
    if params.order_type == "LIMIT":
        return place_limit_order(client, params)
    if params.order_type == "STOP_LIMIT":
        return place_stop_limit_order(client, params)

    raise ValueError(f"Unsupported order type: {params.order_type}")
