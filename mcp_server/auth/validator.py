"""Token validation for MCP tools."""

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TokenValidationError(Exception):
    """Raised when token validation fails."""
    pass


async def validate_session_token(
    session_token: str,
    backend_client
) -> Dict[str, Any]:
    """Validate session token before executing MCP tools.

    Args:
        session_token: JWT token to validate
        backend_client: Backend client for token validation

    Returns:
        User dict with user information if valid

    Raises:
        TokenValidationError: If token is invalid or expired
    """
    logger.info(f"Validating session token for tool execution")

    user_info = await backend_client.validate_token(session_token)

    if user_info is None or not user_info.get("valid"):
        logger.warning("Token validation failed")
        raise TokenValidationError("Invalid or expired session token")

    logger.info(f"Token validated for user: {user_info.get('username', 'unknown')}")
    return user_info
