import unittest
from unittest.mock import patch
from chatbot import (
    generate_question,
    populate_topic_questions,
    get_randomized_questions,
    check_answer,
    get_hint,
    get_explanation,
    all_questions
)

class TestChatbot(unittest.TestCase):

    @patch('chatbot.generate_question')
    def test_generate_question(self, mock_generate_question):
        # Set up mock response
        mock_generate_question.return_value = {
            "question": "What is the derivative of f(x) = x^2?",
            "answer": "2x",
            "hint": "Use the power rule.",
            "explanation": "The derivative of x^2 is 2x."
        }

        result = generate_question("calculus")
        self.assertIn("question", result)
        self.assertIn("answer", result)
        self.assertIn("hint", result)
        self.assertIn("explanation", result)
        self.assertEqual(result["answer"], "2x")
    
    @patch('chatbot.generate_question')
    def test_populate_topic_questions(self, mock_generate_question):
        # Mock response for generating questions
        mock_generate_question.return_value = {
            "question": "What is the integral of x dx?",
            "answer": "x^2/2 + C",
            "hint": "Use the power rule for integration.",
            "explanation": "The integral of x is x^2/2 + C."
        }

        # Clear all_questions before test
        all_questions["calculus"] = []
        populate_topic_questions("calculus", difficulty_levels=["easy"], num_questions=3)

        # Check if questions are populated
        self.assertEqual(len(all_questions["calculus"]), 3)
        for question_data in all_questions["calculus"]:
            self.assertIn("question", question_data)
            self.assertIn("answer", question_data)
            self.assertIn("hint", question_data)
            self.assertIn("explanation", question_data)

    def test_get_randomized_questions(self):
        # Populate with sample data
        all_questions["calculus"] = [
            {"question": "Q1", "answer": "A1", "hint": "H1", "explanation": "E1"},
            {"question": "Q2", "answer": "A2", "hint": "H2", "explanation": "E2"},
        ]
        questions = get_randomized_questions("calculus")
        self.assertEqual(len(questions), 2)
        self.assertTrue(all(isinstance(q, dict) for q in questions))

    def test_check_answer(self):
        question_data = {"question": "What is 2 + 2?", "answer": "4"}
        self.assertTrue(check_answer(question_data, "4"))
        self.assertTrue(check_answer(question_data, " 4 "))  # Test with whitespace
        self.assertFalse(check_answer(question_data, "5"))

    def test_get_hint(self):
        question_data = {"question": "What is 2 + 2?", "answer": "4", "hint": "Think of pairs."}
        self.assertEqual(get_hint(question_data), "Think of pairs.")
        
        # Test when hint is missing
        question_data_no_hint = {"question": "What is 2 + 2?", "answer": "4"}
        self.assertEqual(get_hint(question_data_no_hint), "No hint available.")

    def test_get_explanation(self):
        question_data = {
            "question": "What is 2 + 2?",
            "answer": "4",
            "explanation": "Adding 2 and 2 gives 4."
        }
        self.assertEqual(get_explanation(question_data), "Adding 2 and 2 gives 4.")
        
        # Test when explanation is missing
        question_data_no_explanation = {"question": "What is 2 + 2?", "answer": "4"}
        self.assertEqual(get_explanation(question_data_no_explanation), "No explanation available.")

if __name__ == "__main__":
    unittest.main()
