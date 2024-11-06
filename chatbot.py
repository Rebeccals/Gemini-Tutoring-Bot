import os
import random
import google.generativeai as genai
from google.cloud import aiplatform
#from google.generativeai import GenerateText
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
# Configure the Gemini API client with the API key
# Must have a .env file in the root directory with "GEMINI_API_KEY=API_KEY_HERE" inside to work
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

# Define a dictionary to hold questions by topic
all_questions = {
    "calculus": [],
    "linear_algebra": [],
    "statistics": []
}

def generate_question(topic, difficulty="medium"):
    """
    Generate a college-level math question using Gemini AI for a specified topic and difficulty.
    Returns a dictionary with 'question', 'answer', 'hint', and 'explanation'.
    """
    # Define a prompt to get a question, answer, hint, and explanation
    prompt = f"""
    Create a college-level math question on the topic of {topic}, with {difficulty} difficulty.
    Please include:
    - A question.
    - The correct answer.
    - A hint.
    - A detailed explanation.

    Format it as:
    Question: <question text>
    Answer: <correct answer>
    Hint: <hint text>
    Explanation: <detailed explanation>
    """

    try:
        # Make API call to Gemini AI
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
}
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
       
      #  model = GenerateText(api_key=os.getenv("GEMINI_API_KEY"))
        response = model.generate_txt(prompt=prompt)

        if not response.predictions:
            print("Empty response from API.")
            return {}


        # Parse the response (assuming text is formatted as expected)
        question_data = response.text.strip().split("\n")
        parsed_data = {}
        for item in question_data:
            if item.startswith("Question:"):
                parsed_data["question"] = item[len("Question:"):].strip()
            elif item.startswith("Answer:"):
                parsed_data["answer"] = item[len("Answer:"):].strip()
            elif item.startswith("Hint:"):
                parsed_data["hint"] = item[len("Hint:"):].strip()
            elif item.startswith("Explanation:"):
                parsed_data["explanation"] = item[len("Explanation:"):].strip()

        return parsed_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def populate_topic_questions(topic, difficulty_levels=["easy", "medium", "hard"], num_questions=5):
    """
    Populate questions for a topic with specified difficulty levels and number of questions.
    """
    for level in difficulty_levels:
        for _ in range(num_questions):
            question_data = generate_question(topic, difficulty=level)
            all_questions[topic].append(question_data)

def get_randomized_questions(topic):
    """Retrieve and shuffle questions for a given topic."""
    if topic in all_questions:
        questions = all_questions[topic].copy()
        random.shuffle(questions)
        return questions
    else:
        raise ValueError(f"Topic '{topic}' not found.")

def check_answer(question_data, user_answer):
    """Check if the user's answer is correct."""
    correct_answer = question_data["answer"].strip().lower()
    return user_answer.strip().lower() == correct_answer

def get_hint(question_data):
    """Return a hint for the question if available."""
    return question_data.get("hint", "No hint available.")

def get_explanation(question_data):
    """Return an explanation for the question if available."""
    return question_data.get("explanation", "No explanation available.")

# Example usage:
# Populate questions for each topic (can be run once to set up question bank)
populate_topic_questions("calculus")
populate_topic_questions("linear_algebra")
populate_topic_questions("statistics")

# Get a shuffled list of questions for a specific topic
calculus_questions = get_randomized_questions("calculus")
print(calculus_questions)
