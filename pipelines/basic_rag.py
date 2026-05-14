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
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        # Using Cloud-based embeddings to save RAM on Render
        from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=os.getenv("HF_TOKEN"), 
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.llm = ChatGroq(model_name=self.model_name, temperature=0)
        self.vectorstore = None
        self.data_path = data_path

    def ingest(self, file_path):
        print(f"Ingesting {file_path} into Basic RAG...", flush=True)
        if not os.path.exists(file_path):
            print(f"File {file_path} not found.")
            return
            
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Limit to first 1000 chunks for demo stability (avoiding API timeouts)
        chunks = chunks[:1000]
        
        # Batching for Cloud API stability (10 chunks at a time)
        print(f"Creating vector store with {len(chunks)} chunks in batches of 10...")
        batch_size = 10
        self.vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory="./data/chroma_db"
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
            if os.path.exists("./data/chroma_db"):
                self.vectorstore = Chroma(persist_directory="./data/chroma_db", embedding_function=self.embeddings)
            elif os.path.exists("data/raw/space_data.txt"):
                print("Vector store missing on cloud. Auto-ingesting now...", flush=True)
                self.ingest("data/raw/space_data.txt")
            else:
                return {"error": "Vector store and raw data missing. Please check your data folder."}

        start_time = time.time()
        
        template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
        prompt = ChatPromptTemplate.from_template(template)
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        answer = rag_chain.invoke(query)
        
        end_time = time.time()
        latency = end_time - start_time
        
        # Token estimation
        approx_tokens = (len(query) + (5 * 1000) + len(answer)) // 4
        
        return {
            "answer": answer,
            "latency": latency,
            "tokens": int(approx_tokens),
            "cost": approx_tokens * 0.00000015,
            "sources": [] # Could be populated by running retriever separately
        }

if __name__ == "__main__":
    pipeline = BasicRAGPipeline()
    # pipeline.ingest("data/raw/space_data.txt") 
    # result = pipeline.run("What is the goal of the Artemis program?")
    # print(result)
