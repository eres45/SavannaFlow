import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class LLMOnlyPipeline:
    def __init__(self, model_name=None):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = model_name or "llama-3.3-70b-versatile"
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        self.client = Groq(api_key=self.api_key)

    def run(self, query):
        start_time = time.time()
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
            model=self.model_name,
        )
        
        end_time = time.time()
        latency = end_time - start_time
        
        # Token counting from Groq response
        tokens_used = chat_completion.usage.total_tokens
            
        return {
            "answer": chat_completion.choices[0].message.content,
            "latency": latency,
            "tokens": tokens_used,
            "cost": tokens_used * 0.00000070 # Realistic Llama 3.3 70B pricing
        }

if __name__ == "__main__":
    pipeline = LLMOnlyPipeline()
    result = pipeline.run("Who founded SpaceX?")
    print(result)
