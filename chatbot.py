import os
import random
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])

#import firebase_admin
#from firebase_admin import credentials, firestore

#cred = credentials.Certificate("firebase_key.json")
#firebase_admin.initialize_app(cred)

# Define a dictionary to hold questions by topic
all_questions = {
    "calculus": [],
    "linear_algebra": [],
    "statistics": []
}

def generate_question(topic, difficulty="medium"):
    """
    Generates a college-level math question using Gemini AI for a specified topic and difficulty.

    Args:
        topic: The topic of the question.
        difficulty: The difficulty level (default: "medium").

    Returns:
        A dictionary containing the question, hint, answer, and explanation.
    """
    # Define a prompt to get a question, answer, hint, and explanation
    prompt = f"""
    Create a college-level math question on the topic of {topic}, with {difficulty} difficulty.
    Please include:
    - A question.
    - A hint.
    - The correct answer.
    - A detailed explanation.

    Format it as:
    Question: <question text>
    Hint: <hint text>
    Answer: <correct answer>
    Explanation: <detailed explanation>



    """
    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=generation_config,
)
    response = model.generate_content([prompt])
   # print(response.text)
    question_data = {}

    try:
        lines = response.text.strip().split('\n')
        for line in lines:
            if line.startswith("## Question:"):
                question_data["question"] = line[len("## Question:"):].strip()
            elif line.startswith("## Hint:"):
                question_data["hint"] = line[len("## Hint:"):].strip()
            elif line.startswith("## Answer:"):
                question_data["answer"] = line[len("## Answer:"):].strip()
            elif line.startswith("## Explanation:"):
                question_data["explanation"] = line[len("## Explanation:"):].strip()

        # Check if all required fields are present
        required_fields = ["question", "hint", "answer", "explanation"]
        missing_fields = [field for field in required_fields if field not in question_data]
        
        if missing_fields:
            print(f"Warning: Missing fields in response - {missing_fields}")
            raise ValueError(f"Failed to parse question data: {missing_fields} not found.")

        if not question_data:
            raise ValueError("Failed to parse question data from API response.")

        return question_data

    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Response content: {response.text}")
        return {"error": str(e)}

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
