'''
# Live Build: From RAG to Multi-Agent Systems

Welcome to the Live Build section of the "Generative AI and Agentic AI" workshop! This directory contains three progressive Python scripts that will take you from a simple Q&A bot to a multi-agent system. 

These scripts are designed to be educational and easy to run for beginners. They use the powerful and free Google Gemini API.

##  The Three Scripts

1.  `1_simple_rag.py`: **Retrieval-Augmented Generation (RAG)**
    *   **What it does**: Answers questions based *only* on the content of the `knowledge_base.txt` file. This is the foundation of "chatting with your data."
    *   **Key Concept**: Grounding an LLM with specific, private data to prevent it from making things up.

2.  `2_manual_react_agent.py`: **Agent with a Tool**
    *   **What it does**: A more advanced system that can use a `calculator` tool to solve math problems. It follows a "Reason + Act" (ReAct) loop that we implement from scratch.
    *   **Key Concept**: Giving an LLM the ability to take actions in the real world (or in this case, call a Python function).

3.  `3_multi_agent_router.py`: **Multi-Agent System**
    *   **What it does**: A "dispatcher" agent that analyzes a user's query and routes it to the correct specialist agent (`ResearchAgent` or `MathAgent`).
    *   **Key Concept**: Building teams of specialized AI agents that collaborate to solve complex problems, which is more robust than a single, monolithic agent.

---

## 🛠️ Setup and Installation (5-Minute Guide)

Follow these steps to get the code running on your own machine.

### Step 1: Get Your Free API Key

This code uses the Google Gemini API, which is free for developers.

1.  Go to **Google AI Studio**: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2.  Click "**Create API key in new project**".
3.  Copy the generated API key. It will look something like `AIzaSy...`.

![Get API Key](https://i.imgur.com/example.png) <!-- Placeholder for a real image -->

### Step 2: Set Up Your Python Environment

If you don't have Python, you can install it from [python.org](https://www.python.org/downloads/).

Open your terminal or command prompt and run the following command to install all the necessary libraries:

```bash
sudo pip3 install openai "langchain-text-splitters<2" "langchain-community<1" "faiss-cpu<2" "sentence-transformers<3"
```

### Step 3: Set the Environment Variable

Before you run the scripts, you need to tell them what your API key is. You do this by setting an environment variable.

**On macOS/Linux:**
```bash
export OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

**On Windows (Command Prompt):**
```bash
set OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

> **Important**: You must do this in the *same terminal window* where you will run the Python scripts. Replace `"YOUR_API_KEY_HERE"` with the key you copied from Google AI Studio.

---

## ▶️ Running the Scripts

Make sure you are in this directory (`live_build_code`) in your terminal.

### 1. Run the Simple RAG

```bash
python3 1_simple_rag.py
```

**Expected Output:**
```
--- Building Simple RAG System ---
Loaded and split the knowledge base into 1 chunks.
Created FAISS vector store.

Query: What is the ReAct framework?
> Retrieving context...
> Generating answer...
Answer: The ReAct (Reason and Act) framework, developed by Google researchers, is a popular method for enabling agents to reason about a task and then act on it using tools.

Query: How do multi-agent systems work?
> Retrieving context...
> Generating answer...
Answer: Multi-agent systems involve a 'dispatcher' or 'router' agent that delegates sub-tasks to specialized agents, such as a 'ResearchAgent' for web searches or a 'CodeAgent' for writing Python scripts. This allows for a more robust and scalable approach to complex problem-solving.

Query: What is the capital of France?
> Retrieving context...
> Generating answer...
Answer: I do not have enough information to answer that.
```

### 2. Run the Manual Agent

```bash
python3 2_manual_react_agent.py
```

**Expected Output:**
```
--- Running Manual ReAct Agent ---

User Query: What is 250 multiplied by 12.5?

--- Agent Turn --- 
> Thinking...
> Decided to take Action: Call `calculator`
> TOOL EXECUTED: Calculator with a=250, b=12.5, op='multiply'
> Observation: 3125.0

--- Agent Turn --- 
> Thinking...
> Final Answer: 250 multiplied by 12.5 is 3125.0.

User Query: If I have 5000 dollars and I spend 13.5% of it, how much is left?

--- Agent Turn --- 
> Thinking...
> Decided to take Action: Call `calculator`
> TOOL EXECUTED: Calculator with a=5000, b=0.135, op='multiply'
> Observation: 675.0

--- Agent Turn --- 
> Thinking...
> Decided to take Action: Call `calculator`
> TOOL EXECUTED: Calculator with a=5000, b=675.0, op='subtract'
> Observation: 4325.0

--- Agent Turn --- 
> Thinking...
> Final Answer: You have 4325.0 dollars left.
```

### 3. Run the Multi-Agent Router

```bash
python3 3_multi_agent_router.py
```

**Expected Output:**
```
--- Running Multi-Agent Router System ---

User Query: What is a multi-agent system?
> Router thinking... Which agent is best for this?
> Router decided: ResearchAgent

--- Delegating to ResearchAgent ---
>>> Final Answer from Specialist: A multi-agent system involves a 'dispatcher' or 'router' agent that delegates sub-tasks to specialized agents, such as a 'ResearchAgent' for web searches or a 'CodeAgent' for writing Python scripts.

User Query: What is 50 plus 50?
> Router thinking... Which agent is best for this?
> Router decided: MathAgent

--- Delegating to MathAgent ---
>>> Final Answer from Specialist: The MathAgent could not solve this.

User Query: Explain the ReAct framework.
> Router thinking... Which agent is best for this?
> Router decided: ResearchAgent

--- Delegating to ResearchAgent ---
>>> Final Answer from Specialist: The ReAct framework, developed by Google researchers, is a popular method for enabling agents to reason about a task and then act on it using tools.
```
'''
