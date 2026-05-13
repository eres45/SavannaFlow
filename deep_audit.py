import os
from pipelines.graph_rag import GraphRAGPipeline
from evaluation.scorer import RAGScorer
from dotenv import load_dotenv

load_dotenv()

def deep_audit():
    pipe = GraphRAGPipeline()
    scorer = RAGScorer()
    
    # We test the hardest comparison question
    q = "Compare the payload capacity of Saturn V and SLS."
    
    print(f"AUDIT START: Testing Query - {q}")
    res = pipe.run(q)
    
    context = res.get("context", "N/A")
    answer = res.get("answer", "N/A")
    
    eval_res = scorer.evaluate_pipeline(q, answer, context)
    
    print("\n--- [1] GRAPH CONTEXT RETRIEVED ---")
    print(context)
    
    print("\n--- [2] AI GENERATED ANSWER ---")
    print(answer)
    
    print("\n--- [3] JUDGE DECISION ---")
    print(eval_res["judge"])
    
    # Cross-reference Check
    if "262,000" in context and "262,000" in answer:
        print("\n✅ DATA INTEGRITY VERIFIED: Exact payload numbers matched between Graph and Answer.")
    else:
        print("\n⚠️ DATA MISMATCH: Numbers don't align.")

if __name__ == "__main__":
    deep_audit()
