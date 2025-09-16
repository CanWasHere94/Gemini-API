import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the API key. The library automatically picks up from the environment variable.
genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel('models/gemini-2.5-flash')

# The prompt you want to send to the model.
prompt = "Analyze the content given below in terms of content moderation and return '1' if it's suitable to be released in a website or return '0'. " \
"Content: 'I love you'"

# Send the request and get the response.
try:
    response = model.generate_content(prompt)
    
    # Print the text content from the response.
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please check your API key and network connection.")