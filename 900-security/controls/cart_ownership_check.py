"""
Preventive control for T06 BOLA — cart ownership verification.
Rejects any request where the authenticated user is not the cart owner.
"""


class OwnershipError(PermissionError):
    """Raised when the authenticated user does not own the requested cart."""


def get_cart(user_id: str, cart_id: str, cart_store: dict) -> dict:
    """
    Return cart data only if user_id matches the cart's owner_id.

    Args:
        user_id:    Authenticated user ID from the JWT session token.
        cart_id:    Cart ID from the request path parameter.
        cart_store: Dict mapping cart_id -> {"owner_id": str, "items": list}.

    Returns:
        Cart dict if ownership is verified.

    Raises:
        KeyError:        cart_id does not exist.
        OwnershipError:  user_id does not match cart.owner_id (HTTP 403).
    """
    cart = cart_store[cart_id]  # raises KeyError for unknown cart
    if cart["owner_id"] != user_id:
        raise OwnershipError(
            f"User '{user_id}' is not authorised to access cart '{cart_id}'."
        )
    return cart
