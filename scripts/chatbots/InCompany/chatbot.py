from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import sys
import os
from dotenv import load_dotenv


# Get the absolute path of the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# Add the project root to the system path
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from scripts.langChainTools.query import run_mysql_query

load_dotenv()


model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", 
                               temperature=0, 
                               google_api_key=os.getenv("API_KEY"))

# Define the tools available to the model
tools = [run_mysql_query]

# Create a prompt template for the model
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a helpful assistant that answers user questions by using a database.
         Your job is to use the provided tools to retrieve information from the database and provide a clear answer.
         You must use accurate table and column names in your queries.
         """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

# Create an agent that knows how to use the tools
agent = create_tool_calling_agent(model, tools, prompt)

# Create an executor to run the agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

#user input
user_text = input("Enter what you want from ai: ")

# Now, invoke the agent with a user question that requires a database query
response = agent_executor.invoke(
    {
        "input": user_text
    }
)

print("\n--- Final Model Response ---")
print(response["output"])