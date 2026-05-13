# 🏗️ SavannaFlow // GraphRAG Inference Engine: Architecture

The following diagram illustrates the high-performance inference pipeline designed for the TigerGraph Savanna Hackathon.

```mermaid
graph TD
    User([User Query]) --> API[FastAPI Backend]
    
    subgraph "Inference Strategies"
        API --> P1[Pipeline 1: LLM-Only]
        API --> P2[Pipeline 2: Basic RAG]
        API --> P3[Pipeline 3: GraphRAG]
    end
    
    subgraph "Retrieval Layer"
        P2 --> VectorDB[(FAISS Vector Store)]
        P3 --> TigerGraph[(TigerGraph Cloud)]
    end
    
    subgraph "Knowledge Processing"
        TigerGraph --> GSQL[runGraphRAG GSQL Query]
        GSQL --> Traversal[Multi-hop Relationship Traversal]
        Traversal --> GraphContext[Targeted Context]
    end
    
    subgraph "Synthesis & Evaluation"
        P1 --> Groq[Groq Llama 3.3 70B]
        P2 --> Groq
        P3 --> Groq
        Groq --> Dashboard[Live Dashboard]
        Dashboard --> Scorer[LLM-as-a-Judge Scorer]
    end
    
    style P3 fill:#f96,stroke:#333,stroke-width:4px
    style TigerGraph fill:#f96,stroke:#333,stroke-width:2px
```

## 🛠️ Components Detail

### **1. GraphRAG Strategy (TigerGraph)**
- **Auth**: Implements the Savanna 4.x `GSQL-Secret` handshake to securely bridge external Python clients with the graph cluster.
- **Traversal**: Instead of simple keyword matching, it follows edges between `Mission`, `Spacecraft`, and `Crew` nodes to answer complex multi-hop questions.

### **2. LLM Synthesis (Groq)**
- Uses the `llama-3.3-70b-versatile` model on Groq's LPUs for sub-second response generation.

### **3. Accuracy Scoring**
- **LLM-as-a-Judge**: Uses an independent LLM to evaluate if the answer matches the retrieved context.
- **Performance Tracking**: Calculates real-time token cost and latency to prove the "3x Efficiency" of GraphRAG.
