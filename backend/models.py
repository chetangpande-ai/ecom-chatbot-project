"""
pydantic models for the backend.
"""

from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    size: List[str] = None
    color: List[str] = None
    image: str = None