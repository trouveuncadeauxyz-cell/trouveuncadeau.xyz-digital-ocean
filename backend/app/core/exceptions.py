"""Custom exceptions for TrouveUnCadeau API

Définit les exceptions personnalisées utilisées par l'application.
"""

from typing import Optional, Dict, Any
from datetime import datetime


class TrouveUnCadeauException(Exception):
    """Exception de base pour TrouveUnCadeau"""
    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = datetime.now()
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convertir l'exception en dictionnaire"""
        return {
            "status": "error",
            "message": self.message,
            "error_code": self.error_code,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
        }


class ValidationError(TrouveUnCadeauException):
    """Erreur de validation"""
    def __init__(self, message: str, field: Optional[str] = None):
        details = {}
        if field:
            details["field"] = field
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class NotFoundError(TrouveUnCadeauException):
    """Ressource non trouvée"""
    def __init__(self, resource: str, resource_id: Optional[str] = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=404,
            details={"resource": resource},
        )


class AirtableServiceError(TrouveUnCadeauException):
    """Erreur de service Airtable"""
    def __init__(self, message: str, operation: Optional[str] = None):
        details = {}
        if operation:
            details["operation"] = operation
        super().__init__(
            message=message,
            error_code="AIRTABLE_ERROR",
            status_code=502,
            details=details,
        )


class AIServiceError(TrouveUnCadeauException):
    """Erreur du service IA/LangChain"""
    def __init__(
        self,
        message: str,
        model: Optional[str] = None,
        retry_available: bool = False,
    ):
        details = {}
        if model:
            details["model"] = model
        details["retry_available"] = retry_available
        super().__init__(
            message=message,
            error_code="AI_SERVICE_ERROR",
            status_code=502,
            details=details,
        )


class RateLimitError(TrouveUnCadeauException):
    """Dépassement du taux limite"""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        details = {}
        if retry_after:
            details["retry_after_seconds"] = retry_after
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details=details,
        )


class ConfigurationError(TrouveUnCadeauException):
    """Erreur de configuration"""
    def __init__(self, message: str, missing_key: Optional[str] = None):
        details = {}
        if missing_key:
            details["missing_key"] = missing_key
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            status_code=500,
            details=details,
        )


class UnauthorizedError(TrouveUnCadeauException):
    """Accès non autorisé"""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            message=message,
            error_code="UNAUTHORIZED",
            status_code=401,
        )


class ForbiddenError(TrouveUnCadeauException):
    """Accès interdit"""
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            message=message,
            error_code="FORBIDDEN",
            status_code=403,
        )
