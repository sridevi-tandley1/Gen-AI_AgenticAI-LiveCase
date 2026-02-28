'''
Build 2: Agentic Upgrade with a Tool

This script demonstrates the second step in our live build: upgrading the simple
LLM to an "agent" that can use tools to answer questions.

Key Concepts:
- @tool Decorator: A simple way to make any Python function available to an LLM.
- Agent: A system that uses an LLM to decide which actions to take (e.g., which tools to call).
- AgentExecutor: The runtime that executes the agent's decisions in a loop (Reason -> Act -> Observe).
'''
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent

# --- 1. Configure the API and Model ---
# The ChatOpenAI wrapper is used for LangChain agent compatibility.
# It automatically uses the OPENAI_API_KEY environment variable.
llm = ChatOpenAI(model="gemini-2.5-flash")

# --- 2. Define a Tool ---
# The @tool decorator exposes the function to the agent.
# The docstring is VERY important, as it tells the agent what the tool does.
@tool
def calculator(a: float, b: float, operation: str) -> str:
    """
    Performs a calculation on two numbers. 
    Available operations are: "add", "subtract", "multiply", "divide".
    """
    print(f"\n\033[1;33m> TOOL: Calling Calculator with a={a}, b={b}, operation='{operation}'\033[0m")
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Cannot divide by zero."
        result = a / b
    else:
        return "Error: Invalid operation specified."
    return f"The result is {result}"

tools = [calculator]

# --- 3. Create the Agent ---
def create_agent(llm, tools):
    """Creates an agent that can use the defined tools."""
    # The prompt template is crucial. It instructs the agent on how to behave.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. You have access to a calculator tool to answer math questions."),
        ("user", "{input}"),
        # The placeholder is where the agent's internal thoughts and actions will go.
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # The create_openai_tools_agent function binds the LLM, tools, and prompt together.
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # The AgentExecutor runs the agent's reasoning loop.
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    print("Agent created successfully.")
    return agent_executor

# --- 4. Run a Query ---
def run_query(agent_executor, query: str):
    """Runs a query through the agent executor and prints the result."""
    print(f"\n\033[1;34mUser Query:\033[0m {query}")
    # The .invoke() method starts the agent loop.
    response = agent_executor.invoke({"input": query})
    print(f"\n\033[1;32mFinal Answer:\033[0m {response['output']}\n")

# --- Main Execution ---
if __name__ == "__main__":
    print("\n--- Building Agent with a Tool ---")
    agent_executor = create_agent(llm, tools)
    
    # Query 1: A straightforward calculation
    run_query(agent_executor, "What is 250 multiplied by 12.5?")
    
    # Query 2: A multi-step problem requiring reasoning
    run_query(agent_executor, "If I have 5000 dollars and I spend 13.5% of it, how much is left?")
