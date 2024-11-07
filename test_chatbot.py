# In test_question_generator.py (your test file)

import unittest
from unittest.mock import patch, MagicMock
from chatbot import (
    generate_question,
    populate_topic_questions,
    get_randomized_questions,
    check_answer,
    get_hint,
    get_explanation,
    all_questions  # Make sure this is accessible if modified in tests
)

class TestMathQuestionGenerator(unittest.TestCase):

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_generate_question(self, mock_generate_content):
        # Mocking the API response
        mock_response = MagicMock()
        mock_response.text = """
        ## Question: What is the derivative of f(x) = x^2?
        ## Hint: Use the power rule.
        ## Answer: 2x
        ## Explanation: The power rule states that d/dx of x^n = n * x^(n-1). Here, n = 2.
        """
        mock_generate_content.return_value = mock_response
        
        # Call generate_question and validate response structure
        question_data = generate_question("calculus", "medium")
        self.assertIn("question", question_data)
        self.assertIn("hint", question_data)
        self.assertIn("answer", question_data)
        self.assertIn("explanation", question_data)
        self.assertEqual(question_data["question"], "What is the derivative of f(x) = x^2?")
        self.assertEqual(question_data["answer"], "2x")

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_populate_topic_questions(self, mock_generate_content):
        # Mocking a basic response
        mock_response = MagicMock()
        mock_response.text = """
        ## Question: What is the integral of x?
        ## Hint: Think of the reverse of differentiation.
        ## Answer: (1/2)x^2 + C
        ## Explanation: The integral of x is (1/2)x^2 + C, where C is the constant of integration.
        """
        mock_generate_content.return_value = mock_response
        
        # Populate topic questions
        populate_topic_questions("calculus", num_questions=2)
        self.assertEqual(len(all_questions["calculus"]), 2)
        for question_data in all_questions["calculus"]:
            self.assertIn("question", question_data)
            self.assertIn("hint", question_data)
            self.assertIn("answer", question_data)
            self.assertIn("explanation", question_data)

    def test_get_randomized_questions(self):
        # Populate all_questions with mock data for testing
        all_questions["linear_algebra"] = [
            {"question": "What is a matrix?", "answer": "A rectangular array of numbers.", "hint": "It has rows and columns.", "explanation": "A matrix is a rectangular array..."},
            {"question": "What is a vector?", "answer": "A quantity with magnitude and direction.", "hint": "Think of arrows.", "explanation": "A vector has both..."}
        ]
        
        questions = get_randomized_questions("linear_algebra")
        self.assertEqual(len(questions), 2)
        self.assertNotEqual(questions, all_questions["linear_algebra"])  # Ensure it's shuffled

    def test_check_answer(self):
        question_data = {"answer": "2x"}
        self.assertTrue(check_answer(question_data, "2x"))
        self.assertTrue(check_answer(question_data, "2X"))  # Test case-insensitivity
        self.assertFalse(check_answer(question_data, "x^2"))

    def test_get_hint(self):
        question_data = {"hint": "Use the power rule."}
        self.assertEqual(get_hint(question_data), "Use the power rule.")
        self.assertEqual(get_hint({}), "No hint available.")

    def test_get_explanation(self):
        question_data = {"explanation": "The power rule states that..."}
        self.assertEqual(get_explanation(question_data), "The power rule states that...")
        self.assertEqual(get_explanation({}), "No explanation available.")

if __name__ == '__main__':
    unittest.main()
