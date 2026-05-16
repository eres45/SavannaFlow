import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class BasicRAGPipeline:
    def __init__(self, data_path=None, model_name=None):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = model_name or "llama-3.3-70b-versatile"
        
        # Absolute Path Hardening
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.base_dir, "data", "chroma_db")
        print(f"Basic RAG: Vector DB Path set to {self.db_path}", flush=True)
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        # Using modern HuggingFace Endpoint for stability
        from langchain_huggingface import HuggingFaceEndpointEmbeddings
        self.embeddings = HuggingFaceEndpointEmbeddings(
            huggingfacehub_api_token=os.getenv("HF_TOKEN"), 
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.llm = ChatGroq(model_name=self.model_name, temperature=0)
        
        # Load vectorstore immediately if it exists
        if os.path.exists(self.db_path):
            from langchain_community.vectorstores import Chroma
            self.vectorstore = Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)
            print(f"Basic RAG: Vector store loaded successfully with {self.vectorstore._collection.count()} documents.", flush=True)
        else:
            self.vectorstore = None
            print("Basic RAG: Vector store not found on startup.", flush=True)
            
        self.data_path = data_path

    def ingest(self, file_path):
        print(f"Ingesting {file_path} into Basic RAG...", flush=True)
        if not os.path.exists(file_path):
            print(f"File {file_path} not found.")
            return
            
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        # Limit to first 1000 chunks for demo stability (avoiding API timeouts)
        chunks = chunks[:1000]
        
        # Batching for Cloud API stability (10 chunks at a time)
        print(f"Creating vector store with {len(chunks)} chunks in batches of 10...")
        batch_size = 10
        self.vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.db_path
        )
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            try:
                self.vectorstore.add_texts(texts=batch)
                print(f"Ingested batch {i//batch_size + 1}", flush=True)
                time.sleep(1) # More conservative pacing
            except Exception as e:
                print(f"Batch {i//batch_size + 1} failed: {e}. Skipping...")
        print("Ingestion complete.", flush=True)

    def run(self, query):
        if not self.vectorstore:
            # Auto-healing: Try to load from disk or re-ingest if raw data exists
            if os.path.exists(self.db_path):
                print(f"Basic RAG: Loading existing DB from {self.db_path}", flush=True)
                self.vectorstore = Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)
            elif os.path.exists("data/raw/space_data.txt"):
                print("Basic RAG: Vector store missing. Auto-ingesting raw data...", flush=True)
                self.ingest("data/raw/space_data.txt")
            else:
                return {"error": "Vector store and raw data missing. Please check your data folder."}

        start_time = time.time()
        
        # 1. Retrieve Context
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in docs)
        
        # 2. Generate Answer with Raw Client for Token Precision
        from groq import Groq
        client = Groq(api_key=self.api_key)
        
        prompt = f"""Answer the question based only on the following context:
{context}

Question: {query}
"""
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name,
            temperature=0
        )
        
        answer = chat_completion.choices[0].message.content
        end_time = time.time()
        
        # ACTUAL token counting from Groq response
        tokens_used = chat_completion.usage.total_tokens
        
        return {
            "answer": answer,
            "latency": end_time - start_time,
            "tokens": tokens_used,
            "cost": tokens_used * 0.00000070,
            "sources": [doc.metadata for doc in docs] 
        }

if __name__ == "__main__":
    pipeline = BasicRAGPipeline()
    # pipeline.ingest("data/raw/space_data.txt") 
    # result = pipeline.run("What is the goal of the Artemis program?")
    # print(result)
