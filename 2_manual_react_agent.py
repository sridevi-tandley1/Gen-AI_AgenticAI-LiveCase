'''
Build 2: Manual ReAct (Reason + Act) Agent

This script implements an agent loop from scratch to demonstrate the core logic
of how agentic systems work, avoiding the complexities of libraries like LangChain.

Key Concepts:
- ReAct Loop: A cycle of Thought -> Action -> Observation -> Thought...
- Tool Definition: A simple Python function for the agent to call.
- Prompt Engineering: A carefully crafted prompt that forces the LLM to decide
  between calling a tool or providing a final answer.
- Manual Parsing: We parse the LLM's output to trigger the correct tool call.
'''
import os
import json
from openai import OpenAI

# --- 1. Configure the API ---
client = OpenAI()

# --- 2. Define Tools ---
def calculator(a: float, b: float, operation: str) -> str:
    "Performs a calculation on two numbers. Available operations are: 'add', 'subtract', 'multiply', 'divide'."
    print(f"\n\033[1;33m> TOOL EXECUTED: Calculator with a={a}, b={b}, op='{operation}'\033[0m")
    if operation == "add": return str(a + b)
    if operation == "subtract": return str(a - b)
    if operation == "multiply": return str(a * b)
    if operation == "divide":
        if b == 0: return "Error: Cannot divide by zero."
        return str(a / b)
    return "Error: Invalid operation."

tool_registry = {
    "calculator": calculator
}

# --- 3. The Manual ReAct Agent Loop ---
def run_agent_loop(query: str):
    print(f"\n\033[1;34mUser Query:\033[0m {query}")

    system_prompt = '''
You are a helpful assistant that can use a calculator tool.

To answer the user's query, you must follow a strict loop:
1.  **Thought**: First, think about the user's query and decide if you need to use a tool. If you can answer directly, provide the final answer.
2.  **Action**: If you need a tool, you MUST output a single JSON object with two keys: `{"tool": "tool_name", "args": {"a": float, "b": float, "operation": "str"}}`. The only available tool is `calculator`.
3.  **Final Answer**: After you get a tool's result, or if you didn't need a tool, provide the final answer to the user as a plain, complete sentence.

Respond with ONLY the JSON for an action or ONLY the final answer string. Do not provide explanations for your actions.
'''

    history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    for _ in range(5): # Limit to 5 turns
        print("\n\033[1;36m--- Agent Turn --- \033[0m")
        print(f"\033[1;35m> Thinking...\033[0m")

        completion = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=history,
            temperature=0.0,
        )
        response_text = completion.choices[0].message.content.strip()

        try:
            action = json.loads(response_text)
            tool_name = action.get("tool")
            tool_args = action.get("args")
            if not tool_name or not tool_args or tool_name not in tool_registry:
                raise ValueError("Invalid tool action")

            print(f"\033[1;33m> Decided to take Action: Call `{tool_name}`\033[0m")
            tool_function = tool_registry[tool_name]
            observation = tool_function(**tool_args)
            print(f"\033[1;32m> Observation: {observation}\033[0m")

            history.append({"role": "assistant", "content": response_text})
            history.append({"role": "user", "content": f"Tool Result: {observation}"})

        except (json.JSONDecodeError, ValueError, TypeError):
            print(f"\033[1;32m> Final Answer: {response_text}\033[0m\n")
            return

# --- Main Execution ---
if __name__ == "__main__":
    print("\n--- Running Manual ReAct Agent ---")
    run_agent_loop("What is 250 multiplied by 12.5?")
    run_agent_loop("If I have 5000 dollars and I spend 13.5% of it, how much is left?")
