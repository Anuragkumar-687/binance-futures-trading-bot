"""Input validation for CLI order parameters."""

from __future__ import annotations

from dataclasses import dataclass

from bot.config import VALID_ORDER_TYPES, VALID_SIDES
from bot.exceptions import ValidationError


@dataclass(frozen=True)
class OrderParams:
    """Validated order parameters."""

    symbol: str
    side: str
    order_type: str
    quantity: float
    price: float | None = None
    stop_price: float | None = None


def _validate_symbol(symbol: str | None) -> str:
    if symbol is None or not str(symbol).strip():
        raise ValidationError("Symbol is required.")
    normalized = str(symbol).strip().upper()
    if not normalized.isalnum():
        raise ValidationError("Symbol must contain only letters and numbers.")
    return normalized


def _validate_side(side: str | None) -> str:
    if side is None or not str(side).strip():
        raise ValidationError("Side is required. Must be BUY or SELL.")
    normalized = str(side).strip().upper()
    if normalized not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be BUY or SELL.")
    return normalized


def _validate_order_type(order_type: str | None) -> str:
    if order_type is None or not str(order_type).strip():
        raise ValidationError("Order type is required. Must be MARKET, LIMIT, or STOP_LIMIT.")
    normalized = str(order_type).strip().upper()
    if normalized not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Must be MARKET, LIMIT, or STOP_LIMIT."
        )
    return normalized


def _validate_quantity(quantity: float | str | None) -> float:
    if quantity is None:
        raise ValidationError("Quantity is required.")
    try:
        parsed = float(quantity)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Quantity must be a valid number.") from exc
    if parsed <= 0:
        raise ValidationError("Quantity must be greater than 0.")
    return parsed


def _validate_price(price: float | str | None, field_name: str = "Price") -> float:
    if price is None:
        raise ValidationError(f"{field_name} is required.")
    try:
        parsed = float(price)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a valid number.") from exc
    if parsed <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")
    return parsed


def validate_order_params(
    symbol: str | None,
    side: str | None,
    order_type: str | None,
    quantity: float | str | None,
    price: float | str | None = None,
    stop_price: float | str | None = None,
) -> OrderParams:
    """
    Validate and normalize all order parameters from CLI input.

    Args:
        symbol: Trading pair symbol (e.g. BTCUSDT).
        side: Order side (BUY or SELL).
        order_type: Order type (MARKET, LIMIT, or STOP_LIMIT).
        quantity: Order quantity.
        price: Limit price (required for LIMIT and STOP_LIMIT).
        stop_price: Stop trigger price (required for STOP_LIMIT).

    Returns:
        OrderParams: Validated order parameters.

    Raises:
        ValidationError: If any parameter fails validation.
    """
    validated_symbol = _validate_symbol(symbol)
    validated_side = _validate_side(side)
    validated_type = _validate_order_type(order_type)
    validated_quantity = _validate_quantity(quantity)

    validated_price: float | None = None
    validated_stop_price: float | None = None

    if validated_type == "LIMIT":
        validated_price = _validate_price(price)

    if validated_type == "STOP_LIMIT":
        validated_price = _validate_price(price)
        validated_stop_price = _validate_price(stop_price, field_name="Stop price")

    if validated_type == "MARKET" and price is not None:
        raise ValidationError("Price must not be provided for MARKET orders.")

    if validated_type == "MARKET" and stop_price is not None:
        raise ValidationError("Stop price must not be provided for MARKET orders.")

    if validated_type == "LIMIT" and stop_price is not None:
        raise ValidationError("Stop price must not be provided for LIMIT orders.")

    return OrderParams(
        symbol=validated_symbol,
        side=validated_side,
        order_type=validated_type,
        quantity=validated_quantity,
        price=validated_price,
        stop_price=validated_stop_price,
    )
