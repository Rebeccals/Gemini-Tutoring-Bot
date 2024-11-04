import os
import google.generativeai as genai

# Configure the Gemini API client with the API key
# Must have a .env file in the root directory with "GEMINI_API_KEY=API_KEY_HERE" inside to work
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemnini API model configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)