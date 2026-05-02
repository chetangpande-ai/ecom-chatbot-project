"""
Product management routes indcluding adding, retrieving, updating, and deleting products.

"""

from fastapi import APIRouter, UploadFile, File, From, HTTPException
from ..models import Product
from ..database import products_collection
import base64
from bson import ObjectId


router = APIRouter(prefix="/products", tags=["products"])

@router.post("")
def add_product(
    name: str = From(...),
    category: str = From(...),
    price: float = From(...),
    description: str = From(...),
    image: UploadFile = File(...)
):
    """
    Add a new product to the database.
    """
    image_data = base64.b64encode(image.file.read()).decode("utf-8")
    product = Product(
        name=name,
        category=category,
        price=price,
        description=description,
        image=image_data
    )
    product_data=product.model_dump() if hasattr(product, "model_dump") else product.dict()
    products_collection.insert_one(product_data)
    return {"message": "Product added successfully"}


@router.get("")
def get_products(category: str = "",min_price: int = None, max_price: float = None):
    """
    Retrieve products from the database, optionally filtered by category.
    """
    products = []
    query = {"category":{"$regex": category, "$options": "i"}} if category else {}

    #Apply price range filter if provided