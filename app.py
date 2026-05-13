from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pipelines.llm_only import LLMOnlyPipeline
from pipelines.basic_rag import BasicRAGPipeline
from pipelines.graph_rag import GraphRAGPipeline
from evaluation.scorer import RAGScorer
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for the dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipelines
llm_pipeline = LLMOnlyPipeline()
basic_rag_pipeline = BasicRAGPipeline()
graph_rag_pipeline = GraphRAGPipeline()
scorer = RAGScorer()

@app.post("/query")
async def query_pipelines(request: Request):
    data = await request.json()
    query = data.get("query")
    if not query:
        return {"error": "No query provided"}
    
    # Pipeline 1: LLM Only
    try:
        llm_res = llm_pipeline.run(query)
    except Exception as e:
        llm_res = {"error": str(e), "answer": "LLM Error", "metrics": []}

    # Pipeline 2: Basic RAG
    try:
        basic_res = basic_rag_pipeline.run(query)
    except Exception as e:
        basic_res = {"error": str(e), "answer": "Basic RAG Error (Database might be empty)", "metrics": []}

    # Pipeline 3: GraphRAG
    try:
        graph_res = graph_rag_pipeline.run(query)
    except Exception as e:
        graph_res = {"error": str(e), "answer": "GraphRAG Error (TigerGraph might be offline)", "metrics": []}

    # Real-time Scoring (LLM-as-a-Judge)
    # For a live demo without ground truth, we evaluate how well the answer matches the retrieved context.
    llm_eval = scorer.evaluate_pipeline(query, llm_res.get("answer", ""), "N/A (No Context)")
    basic_eval = scorer.evaluate_pipeline(query, basic_res.get("answer", ""), basic_res.get("context", ""))
    graph_eval = scorer.evaluate_pipeline(query, graph_res.get("answer", ""), graph_res.get("context", ""))

    def format_accuracy(eval_res):
        score = eval_res.get("judge", 0)
        return f"{score}%"

    # Format results for the dashboard
    return {
        "results": [
            {
                "name": "LLM Only",
                "answer": llm_res.get("answer", "Error"),
                "metrics": [
                    {"label": "Tokens", "value": str(llm_res.get("tokens", "---"))},
                    {"label": "Latency", "value": f"{llm_res.get('latency', 0):.2f}s"},
                    {"label": "Cost", "value": f"${llm_res.get('cost', 0):.6f}"},
                    {"label": "Accuracy", "value": format_accuracy(llm_eval)},
                ]
            },
            {
                "name": "Basic RAG",
                "answer": basic_res.get("answer", "Error"),
                "metrics": [
                    {"label": "Tokens", "value": str(basic_res.get("tokens", "---"))},
                    {"label": "Latency", "value": f"{basic_res.get('latency', 0):.2f}s"},
                    {"label": "Cost", "value": f"${basic_res.get('cost', 0):.6f}"},
                    {"label": "Accuracy", "value": format_accuracy(basic_eval)},
                ]
            },
            {
                "name": "GraphRAG",
                "answer": graph_res.get("answer", "Error"),
                "metrics": [
                    {"label": "Tokens", "value": str(graph_res.get("tokens", "---"))},
                    {"label": "Latency", "value": f"{graph_res.get('latency', 0):.2f}s"},
                    {"label": "Cost", "value": f"${graph_res.get('cost', 0):.6f}"},
                    {"label": "Accuracy", "value": format_accuracy(graph_eval)},
                ]
            }
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "online"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
