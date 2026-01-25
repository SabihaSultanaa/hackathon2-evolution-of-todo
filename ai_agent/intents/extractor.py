"""Entity extractor for natural language task management.

This module extracts task details (title, description, category) and
task references from natural language user input.
"""

import re
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class EntityExtractor:
    """Extract task entities and references from natural language input."""

    # Category keyword patterns
    CATEGORY_PATTERNS = {
        'Work': [
            r'\b(?:report|meeting|review|presentation|project|deadline|client|team|standup|sprint)\b',
            r'\b(?:work|office|business|corporate)\b.*?\btask\b',
        ],
        'Personal': [
            r'\b(?:grocery|groceries|shopping|exercise|workout|gym|doctor|dentist|appointment)\b',
            r'\b(?:home|personal|family|friend)\b.*?\btask\b',
            r'\bbuy\b.*?\b(?:milk|bread|eggs|food)\b',
        ],
        'Urgent': [
            r'\b(?:urgent|asap|today|now|immediately|deadline|critical)\b',
            r'\b(?:emergency|priority|important)\b',
        ],
    }

    # Common phrases to remove from task titles
    STOP_WORDS = {
        'i', 'need', 'to', 'the', 'a', 'an', 'and', 'or', 'but', 'for',
        'my', 'me', 'do', 'did', 'have', 'has', 'had', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'should', 'would', 'could',
        'will', 'shall', 'may', 'might', 'must', 'can', 'add', 'create',
        'make', 'get', 'give', 'keep', 'let', 'seem', 'help'
    }

    @classmethod
    def extract_create_entities(cls, user_input: str) -> Dict[str, str]:
        """Extract task creation entities from user input.

        Args:
            user_input: Natural language input

        Returns:
            Dict with 'title', 'description', 'category' keys

        Examples:
            >>> EntityExtractor.extract_create_entities("I need to finish the quarterly report by Friday")
            {'title': 'Finish quarterly report', 'description': 'Due by Friday', 'category': 'Work'}
        """
        logger.info(f"Extracting create entities from: '{user_input[:50]}...'")

        entities = {
            'title': '',
            'description': '',
            'category': 'General'  # Default
        }

        # Remove common intent phrases
        cleaned = cls._remove_intent_phrases(user_input)

        # Extract title (the core action/task)
        entities['title'] = cls._extract_title(cleaned)

        # Extract description (additional context or details)
        entities['description'] = cls._extract_description(user_input, cleaned)

        # Infer category from content
        entities['category'] = cls._infer_category(user_input)

        logger.info(f"Extracted entities: {entities}")
        return entities

    @classmethod
    def extract_task_reference(cls, user_input: str, tasks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Extract and match task reference from user input.

        Args:
            user_input: Natural language input referring to a task
            tasks: List of existing tasks to match against

        Returns:
            Matched task dict or None if no match found

        Examples:
            >>> EntityExtractor.extract_task_reference("mark the report task as done", tasks)
            {'id': 5, 'title': 'Finish quarterly report', 'category': 'Work', ...}
        """
        logger.info(f"Extracting task reference from: '{user_input[:50]}...'")

        # Clean input to get reference text
        reference_text = cls._clean_reference(user_input)

        # Try exact title match first
        for task in tasks:
            if task['title'].lower() == reference_text.lower():
                logger.info(f"Found exact match: {task['title']}")
                return task

        # Try partial title match
        for task in tasks:
            if reference_text.lower() in task['title'].lower():
                logger.info(f"Found partial match: {task['title']}")
                return task

        # Try word-based matching
        reference_words = set(reference_text.lower().split())
        for task in tasks:
            task_words = set(task['title'].lower().split())
            overlap = len(reference_words & task_words)
            if overlap >= len(reference_words) * 0.5 and overlap > 0:
                logger.info(f"Found word overlap match: {task['title']}")
                return task

        logger.warning(f"No task match found for: '{reference_text}'")
        return None

    @classmethod
    def extract_inquiry_filters(cls, user_input: str) -> Dict[str, Any]:
        """Extract filters for task inquiry from user input.

        Args:
            user_input: Natural language inquiry

        Returns:
            Dict with 'category' and 'priority' filters

        Examples:
            >>> EntityExtractor.extract_inquiry_filters("show me my work tasks")
            {'category': 'Work', 'priority': None}
        """
        filters = {
            'category': None,
            'priority': None
        }

        # Check for category filters
        for category, patterns in cls.CATEGORY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    filters['category'] = category
                    logger.info(f"Found category filter: {category}")
                    break

        return filters

    @classmethod
    def _remove_intent_phrases(cls, text: str) -> str:
        """Remove common intent phrases from text.

        Args:
            text: Input text

        Returns:
            Cleaned text
        """
        # Remove common intent patterns
        patterns_to_remove = [
            r'^\s*i (?:need to|should|want to|have to)\s+',
            r'^\s*(?:add|create|make)\s+(?:a|an)?\s*',
            r'^\s*i\s+',
        ]

        cleaned = text
        for pattern in patterns_to_remove:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

        return cleaned.strip()

    @classmethod
    def _extract_title(cls, text: str) -> str:
        """Extract task title from cleaned text.

        Args:
            text: Cleaned text

        Returns:
            Task title
        """
        # Remove time-based phrases for description extraction
        title = re.sub(
            r'\s+(?:by|on|at|before|after)\s+(?:today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|this|next)\b.*$',
            '',
            text,
            flags=re.IGNORECASE
        )

        # Capitalize first letter
        title = title.strip().capitalize()

        # Ensure title is not empty
        if not title:
            title = "New task"

        # Truncate if too long (max 500 chars)
        if len(title) > 500:
            title = title[:497] + "..."

        return title

    @classmethod
    def _extract_description(cls, original: str, cleaned: str) -> str:
        """Extract task description from original input.

        Args:
            original: Original user input
            cleaned: Text with intent phrases removed

        Returns:
            Task description or empty string
        """
        # Look for time-based details
        time_pattern = re.search(
            r'(?:by|on|at|before|after)\s+(?:today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|this|next)\b.*$',
            original,
            re.IGNORECASE
        )

        if time_pattern:
            return f"Due {time_pattern.group(0)}"

        # Look for additional context after the main task
        if len(original) > len(cleaned) + 10:
            additional = original[len(cleaned):].strip()
            # Remove common stop phrases
            additional = re.sub(r'^(?:for|to|with|because|since)\s+', '', additional)
            return additional

        return ""

    @classmethod
    def _infer_category(cls, text: str) -> str:
        """Infer task category from text content.

        Args:
            text: User input text

        Returns:
            Inferred category
        """
        text_lower = text.lower()

        # Check each category pattern
        for category, patterns in cls.CATEGORY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return category

        return 'General'

    @classmethod
    def _clean_reference(cls, user_input: str) -> str:
        """Clean user input to extract task reference.

        Args:
            user_input: Input with task reference

        Returns:
            Cleaned reference text
        """
        # Remove action phrases
        patterns_to_remove = [
            r'\b(?:mark|set|toggle|remove|delete|get rid of)\b',
            r'\b(?:done|complete|completed|finished)\b.*?\bwith\b',
            r'\b(?:the|a|an|my)\b',
            r'\b(?:task|item)\b',
        ]

        reference = user_input
        for pattern in patterns_to_remove:
            reference = re.sub(pattern, '', reference, flags=re.IGNORECASE)

        return reference.strip()


# Convenience functions
def extract_create_entities(user_input: str) -> Dict[str, str]:
    """Extract task creation entities (convenience function)."""
    return EntityExtractor.extract_create_entities(user_input)


def extract_task_reference(user_input: str, tasks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Extract task reference (convenience function)."""
    return EntityExtractor.extract_task_reference(user_input, tasks)


def extract_inquiry_filters(user_input: str) -> Dict[str, Any]:
    """Extract inquiry filters (convenience function)."""
    return EntityExtractor.extract_inquiry_filters(user_input)