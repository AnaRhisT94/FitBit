import logging
import json
from typing import Dict, Any, Union
from langchain.tools import tool

logger = logging.getLogger(__name__)

# --- Mock Data Store ---
# This simulates a database of user data.
mock_user_database = {
    "alex_fitbit": {
        "user_name": "Alex",
        "goals": {"steps": 10000, "weekly_active_days": 5},
        "daily_summary": {
            "date": "01-08-2025",
            "steps": 8500,
            "sleep": {
                "duration_hours": 6.5,
                "quality": "fair",
                "details": "Woke up twice during the night."
            },
            "heart_rate": {"resting": 65, "active_zones_minutes": 45}
        },
        "weekly_summary": {"active_days": 4, "comparison_to_last_week": "more_active"}
    }
}

def _extract_user_id(user_input: Union[str, Dict]) -> str:
    """Helper function to extract user_id from either string or dict input"""
    try:
        # If it's a string that looks like JSON, try to parse it
        if isinstance(user_input, str) and user_input.strip().startswith('{'):
            user_input = json.loads(user_input.strip())["user_id"]
        
        # Now handle either dict or simple string
        if isinstance(user_input, dict):
            return user_input.get("user_id", "")
        return user_input
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON input: {user_input}, error: {e}")
        return user_input if isinstance(user_input, str) else ""

@tool
def get_daily_summary(user_id: Union[str, Dict]) -> Dict[str, Any]:
    """Returns the daily health summary for a given user, including steps, sleep, and heart rate."""
    actual_user_id = _extract_user_id(user_id)
    logger.info(f"Getting daily summary for user (raw input: {user_id}, extracted: {actual_user_id})")
    result = mock_user_database.get(actual_user_id, {}).get("daily_summary", {})
    logger.info(f"Found result: {result}")
    return result

@tool
def get_weekly_summary(user_id: Union[str, Dict]) -> Dict[str, Any]:
    """Returns the weekly activity summary for a given user."""
    actual_user_id = _extract_user_id(user_id)
    logger.info(f"Getting weekly summary for user (raw input: {user_id}, extracted: {actual_user_id})")
    result = mock_user_database.get(actual_user_id, {}).get("weekly_summary", {})
    logger.info(f"Found result: {result}")
    return result

@tool
def get_user_goals(user_id: Union[str, Dict]) -> Dict[str, Any]:
    """Returns the user's health and fitness goals."""
    actual_user_id = _extract_user_id(user_id)
    logger.info(f"Getting goals for user (raw input: {user_id}, extracted: {actual_user_id})")
    result = mock_user_database.get(actual_user_id, {}).get("goals", {})
    logger.info(f"Found result: {result}")
    return result

@tool
def suggest_breathing_exercise(user_id: str) -> str:
    """Use this tool to suggest a breathing exercise to the user, typically when their data indicates stress or poor sleep."""
    logger.info(f"Tool 'suggest_breathing_exercise' called for user: {user_id}")
    return "Suggesting a 2-minute mindful breathing exercise to help the user relax and wind down."

available_tools = [get_daily_summary, get_weekly_summary, get_user_goals, suggest_breathing_exercise]
