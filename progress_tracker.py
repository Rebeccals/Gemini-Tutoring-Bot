# Progress tracking and reporting

from firebase_service import db

def get_user_progress(user_id):
    """Retrieve all progress data for a specific user from Firestore."""
    progress_ref = db.collection("users").document(user_id).collection("progress")
    progress_data = {doc.id: doc.to_dict() for doc in progress_ref.stream()}
    return progress_data


def calculate_accuracy(user_id):
    """Calculate the accuracy for each topic based on user progress."""
    progress = get_user_progress(user_id)
    accuracy = {}
    
    for topic, data in progress.items():
        score = data.get("score", 0)
        total_questions = data.get("total_questions", 1)  # Avoid division by zero
        accuracy[topic] = (score / total_questions) * 100
    
    return accuracy

def generate_feedback(user_id):
    """Generate feedback for the user based on their accuracy in each topic."""
    accuracy = calculate_accuracy(user_id)
    feedback = {}

    for topic, acc in accuracy.items():
        if acc >= 90:
            feedback[topic] = "Excellent! Keep up the great work."
        elif 70 <= acc < 90:
            feedback[topic] = "Good job! A little more practice could get you to the top."
        elif 50 <= acc < 70:
            feedback[topic] = "You're doing okay, but more review on this topic is recommended."
        else:
            feedback[topic] = "Consider revisiting fundamental concepts in this area."

    return feedback


def track_topic_progress(user_id, topic, score, total_questions):
    """Track and update user progress for a specific topic."""
    db.collection("users").document(user_id).collection("progress").document(topic).set({
        "score": score,
        "total_questions": total_questions
    })
    print(f"Updated progress for {user_id} in topic {topic}.")


def summarize_overall_progress(user_id):
    """Summarize the user's overall progress across all topics."""
    accuracy = calculate_accuracy(user_id)
    total_accuracy = sum(accuracy.values()) / len(accuracy) if accuracy else 0
    strengths = [topic for topic, acc in accuracy.items() if acc >= 80]
    weaknesses = [topic for topic, acc in accuracy.items() if acc < 50]
    
    summary = {
        "average_accuracy": total_accuracy,
        "strengths": strengths,
        "weaknesses": weaknesses
    }
    
    return summary
