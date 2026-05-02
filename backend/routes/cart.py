"""
Shopping cart routes for addomg amd retrieving items in the user's cart.
"""

from fastapi import APIRouter
from ..models import CartItem
from ..database import carts_collection

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add")
def add_to_cart(item: CartItem):
    """
    Add an item to the user's cart.
    """
    item_data=item.model_dump() if hasattr(item, "model_dump") else item.dict()
    carts_collection.insert_one(item_data)
    return {"message": "Item added to cart"}



@router.get("/{user_email}")
def get_cart(user_email: str):
    """
    Clear all items in the user's cart.
    """
    cart_items = list(carts_collection.find({"user_email": user_email}, {"_id": 0}))
    return {"cart_items": cart_items}   

@router.delete("/{user_email}")
def clear_cart(user_email: str):
    """
    Delete all items from the user's cart.
    """
    carts_collection.delete_many({"user_email": user_email})
    return {"message": "Cart cleared"}