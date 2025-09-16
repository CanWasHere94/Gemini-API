import google.generativeai as genai
import os


# Configure the API key. The library automatically picks up from the environment variable.
genai.configure(api_key="YOURKEY")

model = genai.GenerativeModel('models/gemini-2.5-flash')

# The prompt you want to send to the model.
prompt = "Tell me a short, interesting fact about the universe."

# Send the request and get the response.
try:
    response = model.generate_content(prompt)
    
    # Print the text content from the response.
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please check your API key and network connection.")