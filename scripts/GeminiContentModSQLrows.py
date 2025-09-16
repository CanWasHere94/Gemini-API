import google.generativeai as genai
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# plase write your environment variables in .env file before using the script.

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel('models/gemini-2.5-flash')


try:
    # Establish the connection to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    #this will take a random row with lang=en, you can change this according to your DB
    sql_query = "SELECT * FROM langs WHERE lang = %s ORDER BY RAND() LIMIT 3"

    #Don't forget to tweak this too.
    language = "en"

    # Execute the query with the language parameter
    cursor.execute(sql_query, (language,))
    
    all_rows = cursor.fetchall()

    if all_rows:
        print("Successfully retrieved rows. Now processing each one:")
        for row in all_rows:

            print(row)
            content = row[2]
            prompt = f"Analyze the content given below in terms of content moderation and return '1' if it's suitable to be released in a website or return '0'. Content: '{content}'"

            # Send the request and get the response.
            try:
                response = model.generate_content(prompt)
                
                print(response.text)

            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please check your API key and network connection.")

    else:
        print(f"No rows found with lang='{language}'")

except mysql.connector.Error as err:
    print(f"Error: {err}")
    print("Please check your database connection details and ensure the database is running.")

finally:
    # Close the cursor and connection to free up resources
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("\nMySQL connection is closed.")