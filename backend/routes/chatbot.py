"""
Chatbot API- Text2NoSQL shopping assistant using Pydantic AI

How it works:
- Normal coversation : agent replies with plain text
-Proeduct queries (shown me X, find Y under Z Price): agent calls 'search products'
tool which queries mongodb and returns matching products
- The endpoi9nt figures out which type of respone to sned to frontend

"""

from fastapi import APIRouter,Body
from backend.database import products_collection
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import os


load_dotenv()

router = APIRouter(prefix="/chat", tags=["Chatbot"])


class StoreDeps(BaseModel):
    """Holds the list of products found during this run. """
    found_products: List[Dict[str, Any]] = []

    class Config:
        arbitrary_types_allowed = True



agent =Agent(
    "groq:qwen/qwen-3-32b",
    deps_type=StoreDeps,
    system_prompt=(
        " yoou are a friendly shopping assistant for clothstore- an online clothing styore."
        "the store has 3 categories: men , women and kids."
        "\n\n"
        "RULES:\n"
        "1. if the user greets you  or ask who you are ->reply naturally and warmly.\n"
        "2. if the user wants to browse products, find  or buy products -> AL:WAYS call the search+products tool with the appropriate category, price range and other filters. NEVER return products directly from the agent. \n" 
        "3. after calling 'search_products', confirm to the user what you saerched for and how many products you found. \n"
        "4. if the user asks something completety unrelated to shopping, reply that you are a shopping assistant and can only help with shopping related queries. \n"
        "5. DO NOT make product names, prices or details ever."
    ),
)


@agent.tool("search_products")
def search_products(
    category: Optional[str] = None,
    price_range: Optional[str] = None,
    keywords: Optional[str] = None,
    context: RunContext[StoreDeps] = None
):
    """Search products in the database based on the given criteria."""
    query = {}
    if category:
        query["category"] = category
    if price_range:
        try:
            min_price, max_price = map(float, price_range.split("-"))
            query["price"] = {"$gte": min_price, "$lte": max_price}
        except ValueError:
            pass  # Invalid price range format, ignore it
    if keywords:
        query["name"] = {"$regex": keywords, "$options": "i"}

    results = list(products_collection.find(query, {"_id": 0}))
    
    # Store the found products in the agent's dependencies for later use
    if context is not None and context.deps is not None:
        context.deps.found_products = results

    return results

@rounter.post("")
def chat(message: str):
    """
    Endpoint to handle user messages and generate chatbot responses.
    """
    response = agent.run(message)
    return {"response": response}   