from chatbot import *

# Testing out the Gemini API
response = chat_session.send_message("What's the most popular apple?")
print(response.text)