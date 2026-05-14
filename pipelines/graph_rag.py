import os
import time
import requests
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GraphRAGPipeline:
    def __init__(self, graphname=None):
        self.host = os.getenv("TIGERGRAPH_HOST", "").rstrip("/")
        self.secret = os.getenv("TIGERGRAPH_TOKEN")
        self.graphname = graphname or os.getenv("TIGERGRAPH_GRAPHNAME", "MyGraphRAG")
        self.query_name = os.getenv("TIGERGRAPH_QUERY", "runGraphRAG")
        self.api_url = f"{self.host}/restpp/query/{self.graphname}/{self.query_name}"
        
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def run(self, query):
        start_time = time.time()
        
        # Aggressive cleaning for TigerGraph stability
        clean_query = "".join(e for e in query if e.isalnum() or e.isspace())
        clean_query = clean_query.strip().replace(" ", "+")
        
        try:
            params = {"p_query": clean_query, "top_k": 5}
            
            # Hybrid Auth: Try Bearer first, fallback to GSQL-Secret
            headers = {"Authorization": f"Bearer {self.secret}"}
            tg_response = requests.get(self.api_url, params=params, headers=headers, timeout=20)
            
            if tg_response.status_code in [401, 403]:
                headers = {"Authorization": f"GSQL-Secret {self.secret}"}
                tg_response = requests.get(self.api_url, params=params, headers=headers, timeout=20)

            tg_response.raise_for_status()
            tg_data = tg_response.json()
            
            # FLEXIBLE EXTRACTION: Catch 'Result.content', 'content', or any attribute
            extracted_texts = []
            results_block = tg_data.get("results", [{}])
            
            # Traverse the TigerGraph results format
            for block in results_block:
                inner_results = block.get("results", [])
                for node in inner_results:
                    attrs = node.get("attributes", {})
                    # Try common TigerGraph result keys
                    text = attrs.get("Result.content") or attrs.get("content") or attrs.get("text")
                    if not text:
                        # Fallback: just take the first string value we find
                        for val in attrs.values():
                            if isinstance(val, str) and len(val) > 10:
                                text = val
                                break
                    if text:
                        extracted_texts.append(text)

            context = "\n".join(list(set(extracted_texts))) # Remove duplicates
            
            if not context or len(context) < 20:
                context = "No specific graph nodes found for these keywords. Falling back to internal knowledge."

            # 2. Synthesize Answer
            prompt = f"""
            You are a GraphRAG specialized AI. Answer the question using the provided Graph Context.
            
            Question: {query}
            Graph Context: {context}
            
            Guidelines:
            - If the Context contains specific numbers (weights, dates, crew sizes), USE THEM.
            - If the Context is missing specific facts, use your internal knowledge but mention 'Based on general aerospace history'.
            
            Answer:
            """
            
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            
            answer = chat_completion.choices[0].message.content
            end_time = time.time()
            
            return {
                "answer": answer,
                "latency": end_time - start_time,
                "tokens": chat_completion.usage.total_tokens,
                "cost": chat_completion.usage.total_tokens * 0.00000015,
                "context": context[:300] + "..."
            }

        except Exception as e:
            return {
                "error": str(e),
                "answer": f"GraphRAG Connection Error: {str(e)}",
                "latency": 0,
                "tokens": 0,
                "cost": 0
            }
