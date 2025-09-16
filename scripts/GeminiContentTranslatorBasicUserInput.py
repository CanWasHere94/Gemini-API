import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the API key. The library automatically picks up from the environment variable.
genai.configure(api_key=os.getenv("API_KEY"))

user_text = input("Enter the text you wanted to be translated: ")
user_language = input("Enter target language: ")

model = genai.GenerativeModel('models/gemini-2.5-flash')

# The prompt you want to send to the model.
prompt = f"Translate the given content into '{user_language}'. Content: '{user_text}'"

# Send the request and get the response.
try:
    response = model.generate_content(prompt)
    
    # Print the text content from the response.
    print(f"\nSource text: '{user_text}'")
    print(f"Result: {response.text}")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please check your API key and network connection.")