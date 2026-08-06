"""Bypass-case tests for the cart ownership-verification control (T06 BOLA)."""

import pytest
from cart_ownership_check import get_cart, OwnershipError

CART_STORE = {
    "cart-001": {"owner_id": "user-A", "items": [{"sku": "SHIRT-L", "qty": 2}]},
    "cart-002": {"owner_id": "user-B", "items": [{"sku": "JEANS-M", "qty": 1}]},
}


# --- bypass cases (the attack — must be BLOCKED) ---

def test_user_b_cannot_access_user_a_cart():
    """BOLA bypass: user-B manipulates cart ID to read user-A's cart."""
    with pytest.raises(OwnershipError):
        get_cart(user_id="user-B", cart_id="cart-001", cart_store=CART_STORE)


def test_unknown_user_cannot_access_any_cart():
    """BOLA bypass: unauthenticated / unknown user ID is rejected."""
    with pytest.raises(OwnershipError):
        get_cart(user_id="attacker-X", cart_id="cart-001", cart_store=CART_STORE)


def test_empty_user_id_is_rejected():
    """Edge case: empty string user_id is not treated as a wildcard match."""
    with pytest.raises(OwnershipError):
        get_cart(user_id="", cart_id="cart-001", cart_store=CART_STORE)


# --- happy path (ownership correct — must PASS) ---

def test_owner_can_access_own_cart():
    """Happy path: user-A accesses their own cart."""
    cart = get_cart(user_id="user-A", cart_id="cart-001", cart_store=CART_STORE)
    assert cart["owner_id"] == "user-A"


def test_unknown_cart_id_raises_key_error():
    """Unknown cart ID raises KeyError before ownership is checked."""
    with pytest.raises(KeyError):
        get_cart(user_id="user-A", cart_id="cart-999", cart_store=CART_STORE)
