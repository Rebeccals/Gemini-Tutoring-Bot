# Firebase interactions

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_progress(user_id, topic, score):
    db.collection("users").document(user_id).collection("progress").document(topic).set({
        "score": score
    })

def load_progress(user_id):
    progress_ref = db.collection("users").document(user_id).collection("progress")
    return {doc.id: doc.to_dict() for doc in progress_ref.stream()}
