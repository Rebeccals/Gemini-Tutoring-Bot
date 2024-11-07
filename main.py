import sqlite3  # Import SQLite for storing user's information
import bcrypt  # For password hashing

# Quiz management

# Define example quiz questions directly within main.py
calculus_questions = [
    {"question": "What is the derivative of sin(x)?", "answer": "cos(x)"},
    {"question": "What is the integral of 1/x dx?", "answer": "ln|x| + C"},
    {"question": "What is the limit of (1 + 1/n)^n as n approaches infinity?", "answer": "e"},
]

linear_algebra_questions = [
    {"question": "What is the determinant of a 2x2 matrix [[a, b], [c, d]]?", "answer": "ad - bc"},
    {"question": "What is the inverse of matrix [[1, 2], [3, 4]]?", "answer": "[[-2, 1], [1.5, -0.5]]"},
    {"question": "What is the rank of a matrix?", "answer": "The maximum number of linearly independent rows or columns."},
]

statistics_questions = [
    {"question": "What is the mean of the dataset [2, 4, 6, 8, 10]?", "answer": "6"},
    {"question": "What does the p-value represent in hypothesis testing?", "answer": "The probability of obtaining test results at least as extreme as the observed results, assuming that the null hypothesis is true."},
    {"question": "What is the standard deviation a measure of?", "answer": "The amount of variation or dispersion in a set of values."},
]

def get_quiz(topic):
    if topic == "calculus":
        return calculus_questions
    elif topic == "linear_algebra":
        return linear_algebra_questions
    elif topic == "statistics":
        return statistics_questions
    else:
        return []

def ask_question(question_data):
    print("Question:", question_data["question"])
    user_answer = input("Your answer: ").strip().lower()
    correct_answer = question_data["answer"].strip().lower()
    is_correct = user_answer == correct_answer
    if is_correct:
        print("Correct!\n")
    else:
        print(f"Incorrect. The correct answer is: {question_data['answer']}\n")
    return is_correct

def quiz(user_id, topic, db_cursor, db_conn):
    questions = get_quiz(topic)
    if not questions:
        print("No questions available for this topic.\n")
        return
    score = 0
    for q in questions:
        if ask_question(q):
            score += 1
    print(f"Your score: {score} out of {len(questions)}\n")
    
    # Update progress in the database
    db_cursor.execute('''
        INSERT INTO progress (username, topic, score)
        VALUES (?, ?, ?)
    ''', (user_id, topic, score))
    
    # Update streak
    db_cursor.execute('''
        SELECT streak FROM users WHERE username = ?
    ''', (user_id,))
    result = db_cursor.fetchone()
    if result:
        current_streak = result[0] if result[0] else 0
    else:
        current_streak = 0
    
    # Assuming a score >= 2 out of 3 is considered successful
    if score >= 2:
        new_streak = current_streak + 1
    else:
        new_streak = 0
    
    db_cursor.execute('''
        UPDATE users
        SET streak = ?
        WHERE username = ?
    ''', (new_streak, user_id))
    
    db_conn.commit()
    print("Your progress has been saved.\n")
    print(f"Current Streak: {new_streak}\n")

# Class to handle user registration and VARK assessment 
# User's style will be determined and added to their profile using scores
class UserAssessment:
    def __init__(self, username, password, db_cursor, db_conn):
        """
        Initialize the UserAssessment with username and password.
        Connects to the SQLite database and creates the users table if it doesn't exist.
        """
        self.username = username
        self.password = password
        self.conn = db_conn
        self.cursor = db_cursor
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
        Includes columns for learning_style and streak.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                learning_style TEXT,
                streak INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def insert_user(self):
        """
        Insert the new user into the users table with hashed password.
        """
        try:
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            # Store hashed_password as bytes directly
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                                (self.username, hashed_password))
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
        Update the learning style in the users table.
        """
        answers = self.administer_assessment()
        scores = self.score_answers(answers)
        styles = self.determine_learning_style(scores)
        print("Assessment Completed!\n")
        print("Your Scores:")
        for style, score in scores.items():
            print(f"  {style}: {score}")
        print("\nYour dominant learning style(s): " + ", ".join(styles) + "\n")
        # Update learning style in the database
        self.cursor.execute('''
            UPDATE users
            SET learning_style = ?
            WHERE username = ?
        ''', (", ".join(styles), self.username))
        self.conn.commit()

# Class to handle user login
class UserLogin:
    def __init__(self, db_cursor, db_conn):
        """
        Initialize the UserLogin.
        Connects to the SQLite database.
        """
        self.conn = db_conn
        self.cursor = db_cursor

    def login(self, username, password):
        """
        Verify the user's credentials.
        Returns True if credentials are valid, else False.
        """
        self.cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        if result:
            stored_hashed_password = result[0]  # This is bytes
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                print(f"User '{username}' logged in successfully.\n")
                return True
            else:
                print("Invalid password.\n")
                return False
        else:
            print("Username not found.\n")
            return False

    def get_learning_style(self, username):
        """
        Retrieve the user's learning style from the database.
        """
        self.cursor.execute('SELECT learning_style FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return result[0]
        else:
            return "Not determined"

    def get_progress(self, username):
        """
        Retrieve the user's progress from the database.
        Returns a dictionary with topics as keys and scores as values.
        """
        self.cursor.execute('SELECT topic, score FROM progress WHERE username = ?', (username,))
        records = self.cursor.fetchall()
        progress = {}
        for topic, score in records:
            if topic in progress:
                progress[topic] += score
            else:
                progress[topic] = score
        return progress

    def get_streak(self, username):
        """
        Retrieve the user's current streak from the database.
        """
        self.cursor.execute('SELECT streak FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        if result and result[0] is not None:
            return result[0]
        else:
            return 0

# Main entry point

def main():
    # Connect to the SQLite database
    db_conn = sqlite3.connect('user_data.db')
    db_cursor = db_conn.cursor()

    # Create necessary tables
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            learning_style TEXT,
            streak INTEGER DEFAULT 0
        )
    ''')
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    db_conn.commit()

    print("Welcome to the VARK Learning Style Assessment and Quiz Platform!\n")
    while True:
        print("Select an option:")
        print("1. Register and take assessment")
        print("2. Login and take a quiz")
        print("3. View Progress and Learning Style")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ").strip()
        print()
        
        if choice == "1":
            # Registration and Assessment
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            print()
            assessment = UserAssessment(username, password, db_cursor, db_conn)
            assessment.run_assessment()
        
        elif choice == "2":
            # Login and take a quiz
            login = UserLogin(db_cursor, db_conn)
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            print()
            if login.login(username, password):
                user_id = username  # Assuming username is used as user_id
                print("Choose a topic for your quiz:")
                print("1. Calculus\n2. Linear Algebra\n3. Statistics")
                topic_choice = input("Your choice: ").strip()
                
                # Map user choice to topic
                if topic_choice == '1':
                    topic = "calculus"
                elif topic_choice == '2':
                    topic = "linear_algebra"
                elif topic_choice == '3':
                    topic = "statistics"
                else:
                    print("Invalid choice\n")
                    continue
                
                # Start quiz and display updated progress
                quiz(user_id, topic, db_cursor, db_conn)
                progress = login.get_progress(user_id)
                print("Progress:")
                if progress:
                    for topic, score in progress.items():
                        print(f"  {topic.capitalize()}: {score} points")
                else:
                    print("  No progress recorded yet.")
                
                streak = login.get_streak(user_id)
                print(f"\nCurrent Streak: {streak}\n")
                learning_style = login.get_learning_style(user_id)
                print("Learning Style:", learning_style, "\n")
        
        elif choice == "3":
            # View Progress and Learning Style
            login = UserLogin(db_cursor, db_conn)
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            print()
            if login.login(username, password):
                progress = login.get_progress(username)
                print("Your Progress:")
                if progress:
                    for topic, score in progress.items():
                        print(f"  {topic.capitalize()}: {score} points")
                else:
                    print("  No progress recorded yet.")
                
                streak = login.get_streak(username)
                print(f"\nCurrent Streak: {streak}\n")
                
                learning_style = login.get_learning_style(username)
                print("Your Learning Style:", learning_style, "\n")
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.\n")

    # Close the database connection before exiting
    db_conn.close()

if __name__ == "__main__":
    main()
