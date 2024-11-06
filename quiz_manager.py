# Quiz management

from chatbot import calculus_questions, linear_algebra_questions

def get_quiz(topic):
    if topic == "calculus":
        return calculus_questions
    elif topic == "linear_algebra":
        return linear_algebra_questions

def ask_question(question_data):
    print("Question:", question_data["question"])
    return input("Your answer: ") == question_data["answer"]

def quiz(user_id, topic):
    questions = get_quiz(topic)
    score = sum(ask_question(q) for q in questions)
    print(f"Your score: {score} out of {len(questions)}")
