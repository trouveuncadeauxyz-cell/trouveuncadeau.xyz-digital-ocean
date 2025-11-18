"""Advanced search engine with semantic and keyword matching."""

from typing import List, Dict, Any, Optional
import re
from difflib import SequenceMatcher
from app.core.utils import normalize_text
import logging

logger = logging.getLogger(__name__)


class SearchEngine:
    """Advanced search with multiple matching strategies."""
    
    def __init__(self):
        self.min_score = 0.3  # 30% minimum match score
    
    def keyword_search(self, query: str, items: List[Dict[str, Any]], 
                       search_fields: List[str]) -> List[tuple]:
        """
        Search items using keyword matching.
        Returns: List of (item, score) tuples sorted by score.
        """
        query_normalized = normalize_text(query)
        query_words = set(query_normalized.split())
        
        results = []
        for item in items:
            item_text = " ".join([
                normalize_text(str(item.get(field, "")))
                for field in search_fields
            ])
            item_words = set(item_text.split())
            
            # Calculate word overlap
            overlap = len(query_words & item_words)
            score = overlap / len(query_words) if query_words else 0
            
            if score >= self.min_score:
                results.append((item, score))
        
        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def fuzzy_search(self, query: str, items: List[Dict[str, Any]], 
                     search_field: str) -> List[tuple]:
        """
        Search items using fuzzy (similarity-based) matching.
        Returns: List of (item, score) tuples.
        """
        query_normalized = normalize_text(query)
        results = []
        
        for item in items:
            field_value = normalize_text(str(item.get(search_field, "")))
            
            # Calculate similarity ratio
            ratio = SequenceMatcher(None, query_normalized, field_value).ratio()
            
            if ratio >= self.min_score:
                results.append((item, ratio))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def range_search(self, items: List[Dict[str, Any]], field: str,
                     min_value: Optional[float] = None,
                     max_value: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Filter items by numeric range.
        """
        results = []
        for item in items:
            value = item.get(field)
            if value is None:
                continue
            
            try:
                value = float(value)
                if (min_value is None or value >= min_value) and \
                   (max_value is None or value <= max_value):
                    results.append(item)
            except (ValueError, TypeError):
                continue
        
        return results
    
    def category_search(self, items: List[Dict[str, Any]], field: str,
                       categories: List[str]) -> List[Dict[str, Any]]:
        """
        Filter items by categories.
        """
        return [
            item for item in items
            if normalize_text(str(item.get(field, ""))) in 
               [normalize_text(cat) for cat in categories]
        ]
    
    def combined_search(self, query: str, items: List[Dict[str, Any]],
                       filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Combine keyword search with optional filters.
        Filters format: {
            'price_min': float,
            'price_max': float,
            'categories': List[str],
            'search_fields': List[str]
        }
        """
        if not filters:
            filters = {}
        
        # Apply range filters first
        results = items
        if 'price_min' in filters or 'price_max' in filters:
            results = self.range_search(
                results,
                field='price',
                min_value=filters.get('price_min'),
                max_value=filters.get('price_max')
            )
        
        # Apply category filter
        if 'categories' in filters and filters['categories']:
            results = self.category_search(results, 'category', filters['categories'])
        
        # Apply keyword search
        search_fields = filters.get('search_fields', ['name', 'description'])
        search_results = self.keyword_search(query, results, search_fields)
        
        # Extract items (remove scores)
        return [item for item, score in search_results]
    
    def suggest(self, query: str, items: List[Dict[str, Any]], 
                field: str, limit: int = 5) -> List[str]:
        """
        Generate search suggestions based on query.
        """
        query_normalized = normalize_text(query)
        suggestions = set()
        
        for item in items:
            field_value = normalize_text(str(item.get(field, "")))
            
            # Check if field starts with query (strong match)
            if field_value.startswith(query_normalized):
                suggestions.add(field_value)
            # Check if query is substring of field
            elif query_normalized in field_value:
                suggestions.add(field_value)
        
        return list(suggestions)[:limit]


def get_search_engine() -> SearchEngine:
    """Get search engine instance."""
    return SearchEngine()
