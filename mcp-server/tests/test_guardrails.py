import unittest

from tools import assistant_agent, is_skill_related


class GuardrailTests(unittest.TestCase):
    def test_skill_related_prompt_is_allowed(self):
        self.assertTrue(is_skill_related("Please review this Python code for bugs"))

    def test_non_skill_prompt_is_rejected(self):
        self.assertFalse(is_skill_related("What is the weather in London today?"))

    def test_assistant_rejects_off_topic_prompt(self):
        result = assistant_agent("Tell me a joke")
        self.assertEqual(result["tool"], "assistant_agent")
        self.assertIn("guardrail", result["summary"].lower())
        self.assertIn("skill", result["assistant_response"].lower())


if __name__ == "__main__":
    unittest.main()
