from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# MySQL connection details from environment variables
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}

@tool
def run_mysql_query(query: str) -> str:
    """
    Executes a read-only SQL query against the MySQL database and returns a summary.
    This tool should only be used for SELECT and DESCRIBE queries to retrieve data.
    """
    if not query.lower().strip().startswith(("select", "describe")):
        return "Only SELECT and DESCRIBE queries are allowed."

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(query)
        # Fetch column names to make the output more readable
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()

        # Format the results into a more concise string
        formatted_result = f"Query executed successfully. Found {len(result)} rows.\n"
        formatted_result += f"Columns: {', '.join(columns)}\n"
        
        # Add the data for each row
        if result:
            for i, row in enumerate(result):
                row_str = ", ".join(f"{col}: {val}" for col, val in zip(columns, row))
                formatted_result += f"Row {i+1}: ({row_str})\n"
        else:
            formatted_result += "Query returned an empty result."

        return formatted_result

    except mysql.connector.Error as err:
        return f"An error occurred during the query: {err}"
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()