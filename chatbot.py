# chatbot.py
import google.generativeai as genai
import os


# Configure the API key
api_key = os.environ["AIzaSyAXBow7M4oTkCJs-BXo6ojNp86ZfeRcP6I"]
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# Function for Visual Learning Style
def VisualLearningStyle(user_input):
    prompt = "You are a learning tutor who excels at helping users who are visual learners. " \
            "Use diagrams, mind maps, flowcharts, and visual aids to explain concepts in a way " \
            "that would appeal to someone who learns best by seeing information. Here's the user's query: {}".format(user_input)
    response = model.generate_response(prompt)
    return response

# Function for Aural Learning Style
def AuralLearningStyle(user_input):
    prompt = "You are a learning tutor who excels at helping users who are auditory learners. " \
            "Use explanations, storytelling, discussions, and verbal instructions to help the user " \
            "understand concepts. Focus on providing detailed and engaging verbal information. Here's the user's query: {}".format(user_input)
    response = model.generate_response(prompt)
    return response

# Function for Read/Write Learning Style
def ReadWriteLearningStyle(user_input):
    prompt = "You are a learning tutor who excels at helping users who are read/write learners. " \
            "Use written explanations, lists, articles, definitions, and text-heavy resources " \
            "to help the user understand concepts. Here's the user's query: {}".format(user_input)
    response = model.generate_response(prompt)
    return response

# Function for Kinesthetic Learning Style
def KinestheticLearningStyle(user_input):
    prompt = "You are a learning tutor who excels at helping users who are kinesthetic learners. " \
            "Use real-life examples, simulations, physical activities, and interactive tasks to explain " \
            "concepts in a practical and hands-on manner. Here's the user's query: {}".format(user_input)
    response = model.generate_response(prompt)
    return response

