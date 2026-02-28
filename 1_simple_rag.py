
import os
from openai import OpenAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS

# --- 1. Configure the API --- 
# IMPORTANT: Set your API key in an environment variable named OPENAI_API_KEY
# You can get a free key from Google AI Studio: https://aistudio.google.com/app/apikey
client = OpenAI()

# --- 2. Load and Chunk the Knowledge Base ---
def load_knowledge_base(file_path="knowledge_base.txt"):
    """Loads a text file and splits it into manageable chunks."""
    with open(file_path, 'r') as f:
        text = f.read()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    print(f"Loaded and split the knowledge base into {len(chunks)} chunks.")
    return chunks

# --- 3. Create Embeddings and Vector Store ---
def create_vector_store(chunks):
    """Creates a FAISS vector store from text chunks."""
    # Use a powerful but free open-source embedding model
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(chunks, embedding_model)
    print("Created FAISS vector store.")
    return vector_store

# --- 4. The RAG Chain ---
def query_rag(query: str, vector_store):
    """Queries the RAG system to get an answer."""
    print(f"\n\033[1;34mQuery:\033[0m {query}")

    # Retrieve the most relevant documents from the vector store
    retriever = vector_store.as_retriever()
    relevant_docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    print("\n\033[1;33m> Retrieving context...\033[0m")
    # print(f"\n--- Retrieved Context ---\n{context}\n-------------------------")

    # --- 5. Generate the Answer with Gemini ---
    system_prompt = """
    You are a helpful assistant. Answer the user's query based ONLY on the provided context.
    If the information is not in the context, say 'I do not have enough information to answer that.'
    """

    completion = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
        ],
        temperature=0.1,
    )

    print("\n\033[1;32m> Generating answer...\033[0m")
    answer = completion.choices[0].message.content
    print(f"\n\033[1;32mAnswer:\033[0m {answer}")
    return answer

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Building Simple RAG System ---")
    knowledge_chunks = load_knowledge_base()
    vector_db = create_vector_store(knowledge_chunks)
    
    # --- Ask a question ---
    query_rag("What is the ReAct framework?", vector_db)
    query_rag("How do multi-agent systems work?", vector_db)
    query_rag("What is the capital of France?", vector_db) # This should fail gracefully
