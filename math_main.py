# main.py
from chatbot import (
    populate_topic_questions,
    get_randomized_questions,
    check_answer,
    get_hint,
    get_explanation,
    all_questions
)

def main():
    # Ask for the user ID
    user_id = input("Enter your user ID: ")
    print(f"Welcome, User {user_id}!")
    
    # Display topic options
    print("\nChoose a topic for your quiz:")
    print("1. Calculus\n2. Linear Algebra\n3. Statistics")
    choice = input("Your choice: ")

    # Map user choice to topic
    if choice == '1':
        topic = "calculus"
    elif choice == '2':
        topic = "linear_algebra"
    elif choice == '3':
        topic = "statistics"
    else:
        print("Invalid choice. Please restart and select a valid option.")
        return

    # Generate and display questions
    print(f"\nGenerating questions for {topic.capitalize()}...")
    populate_topic_questions(topic, num_questions=5)
    questions = get_randomized_questions(topic)

    # Loop through questions
    for question_data in questions:
        print("\n" + question_data["question"])
        user_action = input("Type 'answer' to answer, 'hint' for a hint, or 'explanation' to view the explanation: ").strip().lower()

        if user_action == "hint":
            print("Hint:", get_hint(question_data))
            user_action = input("Now, type 'answer' to answer or 'explanation' to view the explanation: ").strip().lower()

        if user_action == "answer":
            user_answer = input("Enter your answer: ").strip()
            if check_answer(question_data, user_answer):
                print("Correct!")
            else:
                print("Incorrect. The correct answer is:", question_data["answer"])

        if user_action == "explanation":
            print("Explanation:", get_explanation(question_data))

    print("\nQuiz complete! Thank you for participating!")

if __name__ == "__main__":
    main()
