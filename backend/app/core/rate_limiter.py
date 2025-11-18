"""Rate limiting and throttling for API protection."""

from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """In-memory rate limiter with configurable limits."""
    
    def __init__(self, default_requests: int = 100, window_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            default_requests: Requests allowed per window (default: 100)
            window_seconds: Time window in seconds (default: 60)
        """
        self.default_requests = default_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def get_identifier(self, ip_address: str, user_id: Optional[str] = None) -> str:
        """Generate unique identifier for rate limiting."""
        if user_id:
            return f"user_{user_id}"
        return f"ip_{ip_address}"
    
    def is_allowed(self, identifier: str, max_requests: Optional[int] = None) -> bool:
        """Check if request is allowed within rate limit."""
        if max_requests is None:
            max_requests = self.default_requests
        
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check if allowed
        if len(self.requests[identifier]) < max_requests:
            self.requests[identifier].append(now)
            return True
        
        logger.warning(f"Rate limit exceeded for {identifier}")
        return False
    
    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests for identifier."""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        return max(0, self.default_requests - len(self.requests[identifier]))
    
    def get_reset_time(self, identifier: str) -> int:
        """Get seconds until rate limit resets."""
        if not self.requests[identifier]:
            return 0
        
        oldest_request = min(self.requests[identifier])
        reset_time = oldest_request + timedelta(seconds=self.window_seconds)
        seconds_until_reset = (reset_time - datetime.utcnow()).total_seconds()
        
        return max(0, int(seconds_until_reset))
    
    def cleanup_old_entries(self, max_age_minutes: int = 60):
        """Remove old entries to prevent memory leak."""
        cutoff_time = datetime.utcnow() - timedelta(minutes=max_age_minutes)
        
        keys_to_remove = []
        for identifier, requests in self.requests.items():
            self.requests[identifier] = [
                req_time for req_time in requests
                if req_time > cutoff_time
            ]
            if not self.requests[identifier]:
                keys_to_remove.append(identifier)
        
        for key in keys_to_remove:
            del self.requests[key]


class EndpointRateLimits:
    """Different rate limits for different endpoints."""
    
    # Conservative limits for expensive operations
    RECOMMENDATIONS = 30  # 30 requests per minute
    PRODUCTS = 60  # 60 requests per minute
    HEALTH = 200  # 200 requests per minute
    
    @staticmethod
    def get_limit(endpoint: str) -> int:
        """Get rate limit for specific endpoint."""
        limits = {
            "/api/recommendations": EndpointRateLimits.RECOMMENDATIONS,
            "/api/products": EndpointRateLimits.PRODUCTS,
            "/health": EndpointRateLimits.HEALTH,
            "/api/health": EndpointRateLimits.HEALTH,
        }
        return limits.get(endpoint, 100)  # Default to 100


class AdaptiveRateLimiter:
    """Adaptive rate limiter that adjusts based on server load."""
    
    def __init__(self, base_limiter: RateLimiter):
        self.base_limiter = base_limiter
        self.cpu_threshold = 80  # %
        self.memory_threshold = 85  # %
        self.load_factor = 1.0  # Multiplier for rate limits
    
    def adjust_limits_based_on_load(self, cpu_percent: float, memory_percent: float):
        """Dynamically adjust rate limits based on system load."""
        if cpu_percent > self.cpu_threshold or memory_percent > self.memory_threshold:
            self.load_factor = 0.5  # Reduce limits by 50%
            logger.warning(f"High load detected. Reducing rate limits by 50%. CPU: {cpu_percent}%, Memory: {memory_percent}%")
        else:
            self.load_factor = 1.0  # Normal limits
    
    def is_allowed(self, identifier: str, endpoint: str) -> bool:
        """Check if request is allowed with adaptive limits."""
        limit = EndpointRateLimits.get_limit(endpoint)
        adjusted_limit = int(limit * self.load_factor)
        return self.base_limiter.is_allowed(identifier, adjusted_limit)


def get_client_ip(request) -> str:
    """Extract client IP from request, accounting for proxies."""
    # Check X-Forwarded-For header first (behind proxy)
    if hasattr(request, 'headers'):
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
    
    # Fallback to direct IP
    if hasattr(request, 'client'):
        return request.client.host if request.client else "unknown"
    
    return "unknown"


# Global rate limiter instance
_rate_limiter = RateLimiter(default_requests=100, window_seconds=60)


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance."""
    return _rate_limiter


def reset_rate_limiter():
    """Reset all rate limit counters (for testing)."""
    global _rate_limiter
    _rate_limiter = RateLimiter(default_requests=100, window_seconds=60)
