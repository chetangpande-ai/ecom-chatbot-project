"""
pydantic models for the backend.
"""

from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    """Product model for the e-commerce application."""
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    size: List[str] = None
    color: List[str] = None
    image: str = None

class Order(BaseModel):
    """Order model for placing an order."""
    user_email: str
    product_name: str
    quantity: int

class CartItem(BaseModel):
    """Cart item model for adding items to the cart."""
    user_email: str
    product_name: str
    quantity: int

