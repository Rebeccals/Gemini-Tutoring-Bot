"""
from chatbot import *

# Testing out the Gemini API
response = chat_session.send_message("What's the most popular apple?",stream=True)
for chunk in response:
    print(chunk.text)
    print("_" * 80)
>>>>>>> fd777f6fb0aa1f6e848dfc8733849fccf4859975

"""




import sqlite3 # Import SQLite for storing user's information

# Class to handle user registration and VARK assessment 
# User's style will be determined and added to their profile using scores +
class UserAssessment:
    def __init__(self, username, password):
        """
        Initialize the UserAssessment with username and password.
        Connects to the SQLite database and creates the users table if it doesn't exist.
        """
        self.username = username
        self.password = password
        self.conn = sqlite3.connect('vark_assessment.db')  # Connect to SQLite database
        self.cursor = self.conn.cursor()
        self.create_users_table()
        self.insert_user()

        # Define the assessment questions
        self.questions = [
            {
                "question": "When studying a new topic, I prefer:",
                "options": {
                    "A": "Diagrams or charts",
                    "B": "Listening to lectures or discussions",
                    "C": "Reading articles or textbooks",
                    "D": "Hands-on activities or experiments"
                }
            },
            {
                "question": "I find it easiest to remember information when:",
                "options": {
                    "A": "I can visualize it",
                    "B": "I hear it explained",
                    "C": "I write it down",
                    "D": "I can practice it myself"
                }
            },
            {
                "question": "In a group setting, I contribute by:",
                "options": {
                    "A": "Drawing or illustrating concepts",
                    "B": "Sharing ideas verbally",
                    "C": "Providing written notes or summaries",
                    "D": "Suggesting activities or demonstrations"
                }
            },
            {
                "question": "If I encounter a difficult problem, I:",
                "options": {
                    "A": "Try to visualize it or draw it out",
                    "B": "Talk it through with someone",
                    "C": "Read more about it",
                    "D": "Try different hands-on methods to solve it"
                }
            },
            {
                "question": "When learning something new, I prefer:",
                "options": {
                    "A": "Watching videos or presentations",
                    "B": "Listening to podcasts or audio materials",
                    "C": "Reading instructions or manuals",
                    "D": "Engaging in physical practice or role-playing"
                }
            },
            {
                "question": "My favorite study method is:",
                "options": {
                    "A": "Creating mind maps or charts",
                    "B": "Listening to recorded lectures",
                    "C": "Writing summaries or essays",
                    "D": "Doing lab work or physical projects"
                }
            },
            {
                "question": "I remember things best when I:",
                "options": {
                    "A": "Can visualize them",
                    "B": "Hear them repeated",
                    "C": "Write them down multiple times",
                    "D": "Practice or apply them directly"
                }
            }
        ]

    def create_users_table(self):
        """
        Create the users table in the database if it doesn't already exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_user(self):
        """
        Insert the new user into the users table.
        """
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                                (self.username, self.password))
            self.conn.commit()
            print(f"User '{self.username}' registered successfully.\n")
        except sqlite3.IntegrityError:
            print(f"Username '{self.username}' is already taken. Please choose a different username.\n")

    def administer_assessment(self):
        """
        Present the assessment questions to the user and collect responses.
        Returns a list of the user's answers.
        """
        print("Please answer the following questions to determine your learning style:\n")
        answers = []
        for index, q in enumerate(self.questions, 1):
            print(f"Q{index}: {q['question']}")
            for option, text in q['options'].items():
                print(f"  {option}) {text}")
            # Get user input and validate it
            while True:
                answer = input("Your answer (A/B/C/D): ").strip().upper()
                if answer in q['options']:
                    answers.append(answer)
                    print()  # Blank line for readability
                    break
                else:
                    print("Invalid input. Please enter A, B, C, or D.")
        return answers

    def score_answers(self, answers):
        """
        Score the user's answers based on the VARK method.
        Returns a dictionary with scores for each learning style.
        """
        scores = {"Visual": 0, "Auditory": 0, "Reading/Writing": 0, "Kinesthetic": 0}
        for answer in answers:
            if answer == "A":
                scores["Visual"] += 1
            elif answer == "B":
                scores["Auditory"] += 1
            elif answer == "C":
                scores["Reading/Writing"] += 1
            elif answer == "D":
                scores["Kinesthetic"] += 1
        return scores

    def determine_learning_style(self, scores):
        """
        Determine the user's dominant learning style based on the scores.
        Returns the learning style(s) with the highest score.
        """
        max_score = max(scores.values())
        styles = [style for style, score in scores.items() if score == max_score]
        return styles

    def run_assessment(self):
        """
        Run the complete assessment process: administer, score, and determine learning style.
        """
        answers = self.administer_assessment()
        scores = self.score_answers(answers)
        styles = self.determine_learning_style(scores)
        print("Assessment Completed!\n")
        print("Your Scores:")
        for style, score in scores.items():
            print(f"  {style}: {score}")
        print("\nYour dominant learning style(s): " + ", ".join(styles) + "\n")

    def __del__(self):
        """
        Close the database connection when the object is destroyed.
        """
        self.conn.close()

# Class to handle user login
class UserLogin:
    def __init__(self):
        """
        Initialize the UserLogin.
        Connects to the SQLite database.
        """
        self.conn = sqlite3.connect('vark_assessment.db')  # Connect to SQLite database
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        """
        Verify the user's credentials.
        Returns True if credentials are valid, else False.
        """
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        result = self.cursor.fetchone()
        if result:
            print(f"User '{username}' logged in successfully.\n")
            return True
        else:
            print("Invalid username or password.\n")
            return False

    def __del__(self):
        """
        Close the database connection when the object is destroyed.
        """
        self.conn.close()

# Example usage
if __name__ == "__main__":
    print("Welcome to the VARK Learning Style Assessment!\n")
    while True:
        print("Select an option:")
        print("1. Register and take assessment")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()
        print()
        
        if choice == "1":
            # Registration and Assessment
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            print()
            assessment = UserAssessment(username, password)
            assessment.run_assessment()
        
        elif choice == "2":
            # Login
            login = UserLogin()
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            print()
            if login.login(username, password):
                # After successful login, you can add more functionalities if needed
                pass
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select 1, 2, or 3.\n")


