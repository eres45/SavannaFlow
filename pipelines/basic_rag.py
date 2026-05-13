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
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        
        self.vectorstore = Chroma.from_texts(
            texts=chunks, 
            embedding=self.embeddings,
            persist_directory="./data/chroma_db"
        )
        print("Ingestion complete.", flush=True)

    def run(self, query):
        if not self.vectorstore:
            # Try to load from disk if exists
            if os.path.exists("./data/chroma_db"):
                self.vectorstore = Chroma(persist_directory="./data/chroma_db", embedding_function=self.embeddings)
            else:
                return {"error": "Vector store not initialized. Run ingest() first."}

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
