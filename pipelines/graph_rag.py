import os
import time
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GraphRAGPipeline:
    def __init__(self, graphname=None):
        self.host = os.getenv("TIGERGRAPH_HOST", "").rstrip("/")
        # Using the FRESH secret provided by the user
        self.secret = "0uf9o0m918jphv7h3535mhla2o8rf84d" 
        self.graphname = graphname or os.getenv("TIGERGRAPH_GRAPHNAME", "MyGraphRAG")
        self.query_name = os.getenv("TIGERGRAPH_QUERY", "runGraphRAG")
        self.api_url = f"{self.host}/restpp/query/{self.graphname}/{self.query_name}"
        
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def run(self, query):
        start_time = time.time()
        
        try:
            params = {"p_query": query, "top_k": 3}
            
            # Step 1: Try the direct GSQL-Secret header (The "Alternative" simpler way)
            # This is the most reliable way to use a secret directly without exchange
            headers = {"Authorization": f"GSQL-Secret {self.secret}"}
            
            tg_response = requests.get(self.api_url, params=params, headers=headers, timeout=20)
            
            # Step 2: If 403, try the Token Exchange Flow (The "Official" way)
            if tg_response.status_code == 403:
                token_res = requests.post(
                    f"{self.host}/restpp/requesttoken",
                    json={"secret": self.secret, "lifetime": "2592000"},
                    timeout=10
                )
                if token_res.status_code == 200:
                    token = token_res.json().get("token")
                    headers = {"Authorization": f"Bearer {token}"}
                    tg_response = requests.get(self.api_url, params=params, headers=headers, timeout=20)

            tg_response.raise_for_status()
            tg_data = tg_response.json()
            
            # Extract content from the result set
            graph_results = tg_data.get("results", [{}])[0].get("results", [])
            context = "\n".join([r.get("attributes", {}).get("content", "") for r in graph_results])
            
            if not context:
                context = "No relevant graph relationships found for this query."

            # 2. Synthesize Answer
            prompt = f"""
            You are a GraphRAG specialized AI. Answer the question using the provided Graph Context.
            Graph Context is highly structured and contains multi-hop relationships.
            
            Question: {query}
            Graph Context: {context}
            
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
                "context": context[:200] + "..."
            }

        except Exception as e:
            return {
                "error": str(e),
                "answer": f"GraphRAG Connection Error: {str(e)}",
                "latency": 0,
                "tokens": 0,
                "cost": 0
            }
