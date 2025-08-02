import unittest
from src.fitbit_agent.tools import get_user_goals

class TestTools(unittest.TestCase):

    def test_get_user_goals_success(self):
        """Test that goals are retrieved correctly for a known user."""
        user_id = "alex_fitbit"
        expected_goals = {"steps": 10000, "weekly_active_days": 5}
        result = get_user_goals.invoke(user_id)
        self.assertEqual(result, expected_goals)

    def test_get_user_goals_failure(self):
        """Test that an empty dict is returned for an unknown user."""
        user_id = "unknown_user"
        result = get_user_goals.invoke(user_id)
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()