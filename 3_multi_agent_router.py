
'''
Build 3: Multi-Agent Router

This script demonstrates a simple multi-agent system where a "router" or
"dispatcher" agent decides which specialist agent is best suited to handle a query.

Key Concepts:
- Specialist Agents: We define two agents with distinct roles:
  - MathAgent: Good at calculations (using our manual ReAct agent).
  - ResearchAgent: Good at answering questions from a knowledge base (using our RAG script).
- Router Agent: A top-level agent whose only job is to classify the user's query
  and delegate it to the correct specialist.
- Prompt Engineering: The router's prompt is engineered to force a choice between the available specialists.
'''
import os
import json
from openai import OpenAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS

# --- 1. Configure the API ---
client = OpenAI()

# --- 2. Define Specialist Agent 1: ResearchAgent (Simplified RAG) ---
def run_research_agent(query: str) -> str:
    """Answers questions based on the knowledge_base.txt file."""
    print("\n\033[1;32m--- Delegating to ResearchAgent ---\033[0m")
    with open("knowledge_base.txt", 'r') as f:
        text = f.read()
    
    vector_store = FAISS.from_texts([text], SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"))
    retriever = vector_store.as_retriever()
    context = retriever.invoke(query)[0].page_content

    system_prompt = "You are a research assistant. Answer the user's query based ONLY on the provided context."
    completion = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
        ],
        temperature=0.0,
    )
    return completion.choices[0].message.content

# --- 3. Define Specialist Agent 2: MathAgent (Manual ReAct) ---
# (We'll reuse the core logic from 2_manual_react_agent.py as a function)
def run_math_agent(query: str) -> str:
    """Handles mathematical calculations using a tool."""
    print("\n\033[1;33m--- Delegating to MathAgent ---\033[0m")
    # This is a simplified version of the loop from the previous script
    # For brevity, we'll just simulate the final answer
    if "multiplied" in query:
        return "The result of 250 multiplied by 12.5 is 3125.0."
    if "spend" in query:
        return "After spending 13.5% of $5000, you have $4325.0 left."
    return "The MathAgent could not solve this."

# --- 4. The Router Agent ---
def run_router(query: str):
    """Classifies the user's query and routes it to the correct specialist agent."""
    print(f"\n\033[1;34mUser Query:\033[0m {query}")
    print("\n\033[1;35m> Router thinking... Which agent is best for this?\033[0m")

    router_prompt = f"""
You are a dispatcher. Your job is to route a user's query to the best-suited specialist agent.

You have two agents available:
1.  **MathAgent**: Best for any questions involving numbers, calculations, or mathematical reasoning.
2.  **ResearchAgent**: Best for questions about AI concepts, definitions, and history from a knowledge base.

Based on the user's query, which agent should you choose?

User Query: "{query}"

Respond with ONLY the name of the agent: "MathAgent" or "ResearchAgent".
"""

    completion = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role": "user", "content": router_prompt}],
        temperature=0.0,
    )
    chosen_agent = completion.choices[0].message.content.strip()
    print(f"\033[1;36m> Router decided: {chosen_agent}\033[0m")

    # --- 5. Delegate to the Chosen Specialist ---
    if "MathAgent" in chosen_agent:
        final_answer = run_math_agent(query)
    elif "ResearchAgent" in chosen_agent:
        final_answer = run_research_agent(query)
    else:
        final_answer = "The router could not decide which agent to use."

    print(f"\n\033[1;32m>>> Final Answer from Specialist: {final_answer}\033[0m\n")

# --- Main Execution ---
if __name__ == "__main__":
    print("\n--- Running Multi-Agent Router System ---")
    
    # Query 1: Should go to the ResearchAgent
    run_router("What is a multi-agent system?")
    
    # Query 2: Should go to the MathAgent
    run_router("What is 50 plus 50?")
    
    # Query 3: A more complex one for the ResearchAgent
    run_router("Explain the ReAct framework.")
