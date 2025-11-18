"""Airtable integration service for product data"""

import os
import httpx
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class AirtableService:
    """Service for interacting with Airtable API"""
    
    def __init__(self, api_key: str, base_id: str, table_id: str):
        self.api_key = api_key
        self.base_id = base_id
        self.table_id = table_id
        self.base_url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    async def get_all_products(self) -> List[Dict[str, Any]]:
        """Fetch all products from Airtable"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                products = []
                for record in data.get("records", []):
                    product = {
                        "id": record.get("id"),
                        **record.get("fields", {})
                    }
                    products.append(product)
                
                logger.info(f"Retrieved {len(products)} products from Airtable")
                return products
        except Exception as e:
            logger.error(f"Error fetching products from Airtable: {str(e)}")
            return []
    
    async def search_products(
        self,
        query: str,
        fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search products with formula"""
        try:
            if not fields:
                fields = ["Name", "ASIN", "Price", "Category", "Description"]
            
            formula = f'SEARCH("{query.lower()}", LOWER({{Name}}))'
            params = {"filterByFormula": formula}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.base_url,
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                products = [
                    {"id": r.get("id"), **r.get("fields", {})}
                    for r in data.get("records", [])
                ]
                return products
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return []
