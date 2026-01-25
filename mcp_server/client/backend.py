"""Backend API client for MCP server.

Provides async HTTP client to communicate with the FastAPI backend.
"""

import httpx
import logging
import os
from dotenv import load_dotenv
from typing import Any, Dict, Optional

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API URL from environment
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


class BackendClient:
    """Async HTTP client for backend API communication."""

    def __init__(self, base_url: str = BACKEND_URL, timeout: float = 30.0):
        """Initialize the HTTP client."""
        self.client = httpx.AsyncClient(timeout=timeout, base_url=base_url)

    async def validate_token(
        self,
        token: str
    ) -> Optional[Dict[str, Any]]:
        """Validate a JWT token with the backend.

        Args:
            token: JWT token to validate

        Returns:
            User dict if valid, None if invalid

        Raises:
            httpx.HTTPStatusError: If validation fails
        """
        try:
            response = await self.client.post(
                "/api/v1/tasks/validate-token",
                content=token,
                headers={"Content-Type": "text/plain"}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.warning(f"Token validation failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error validating token: {e}")
            return None

    async def get_tasks(
        self,
        token: str,
        category_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Retrieve all tasks for authenticated user.

        Args:
            token: JWT session token
            category_filter: Optional category filter

        Returns:
            Task list response

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        headers = {"Authorization": f"Bearer {token}"}

        params = {}
        if category_filter:
            params["category"] = category_filter

        response = await self.client.get(
            "/api/v1/tasks",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    async def create_task(
        self,
        token: str,
        title: str,
        description: str = "",
        category: str = "General"
    ) -> Dict[str, Any]:
        """Create a new task.

        Args:
            token: JWT session token
            title: Task title
            description: Task description (optional)
            category: Task category (optional)

        Returns:
            Created task response

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        headers = {"Authorization": f"Bearer {token}"}

        response = await self.client.post(
            "/api/v1/tasks",
            headers=headers,
            json={
                "title": title,
                "description": description,
                "category": category
            }
        )
        response.raise_for_status()
        return response.json()

    async def toggle_task_status(
        self,
        token: str,
        task_id: int
    ) -> Dict[str, Any]:
        """Toggle task completion status.

        Args:
            token: JWT session token
            task_id: Task ID to toggle

        Returns:
            Updated task response

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        headers = {"Authorization": f"Bearer {token}"}

        response = await self.client.patch(
            f"/api/v1/tasks/{task_id}/toggle",
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    async def remove_task(
        self,
        token: str,
        task_id: int
    ) -> Dict[str, Any]:
        """Delete a task.

        Args:
            token: JWT session token
            task_id: Task ID to delete

        Returns:
            Empty response on success (204)

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        headers = {"Authorization": f"Bearer {token}"}

        response = await self.client.delete(
            f"/api/v1/tasks/{task_id}",
            headers=headers
        )
        # Delete returns 204, no body
        if response.status_code != 204:
            response.raise_for_status()
        return {"success": True, "message": "Task deleted"}

    async def health_check(self) -> Dict[str, str]:
        """Check if backend is accessible."""
        try:
            response = await self.client.get("/api/v1/tasks/")
            return {
                "status": "healthy",
                "backend_url": self.client.base_url
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "backend_url": self.client.base_url
            }


# Global client instance
client = BackendClient()
