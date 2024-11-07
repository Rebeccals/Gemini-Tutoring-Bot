# Main entry point

from quiz_manager import quiz
from firebase_service import load_progress
from learning_style import get_learning_style

def main():
    user_id = input("Enter your user ID: ")
    print("Choose a topic for your quiz:")
    print("1. Calculus\n2. Linear Algebra\n3. Statistics")
    choice = input("Your choice: ")
    
    # Map user choice to topic and start quiz
    if choice == '1':
        topic = "calculus"
    elif choice == '2':
        topic = "linear_algebra"
    elif choice == '3':
        topic = "statistics"
    else:
        print("Invalid choice")
        return
    
    # Start quiz and display updated progress
    quiz(user_id, topic)
    progress = load_progress(user_id)
    print("Progress:", progress)
    learning_style = get_learning_style(user_id)
    print("Learning Style:", learning_style)

if __name__ == "__main__":
    main()

