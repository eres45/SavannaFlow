# 🎬 SavannaFlow Demo Video Script

## 🕒 Duration: 3-4 Minutes
**Goal**: Demonstrate how GraphRAG kills the "Vector RAG Tax" (cost & latency).

---

### **0:00 - 0:30 | The Hook & The Problem**
*   **Visual**: Screen recording of the GitHub README or Project Branding.
*   **Speaker**: 
    "Hi everyone! I'm [Your Name] from Team SavannaFlow. Today, we're solving the biggest problem in AI: the 'Vector RAG Tax.' 
    Standard Vector RAG is slow and expensive because it pulls in massive, irrelevant text chunks. We built **SavannaFlow** to prove there’s a better way using TigerGraph."

### **0:30 - 1:15 | The "Wow" Demo (Side-by-Side)**
*   **Visual**: Switch to the **SavannaFlow Dashboard**.
*   **Action**: Type: *"Compare the payload capacity of Saturn V and SLS."* → Hit Search.
*   **Speaker**: 
    "Look at this side-by-side comparison. 
    On the left, **LLM-Only** is just guessing. 
    In the middle, **Basic RAG** is burning over 1,300 tokens because it’s pulling entire paragraphs of text. 
    But on the right, **SavannaFlow (GraphRAG)** is surgically retrieving just the facts from TigerGraph. 
    It used only **325 tokens**—that’s a 75% reduction in size and cost!"

### **1:15 - 2:00 | The Architecture**
*   **Visual**: Show the **Mermaid Architecture Diagram**.
*   **Speaker**: 
    "How does it work? We’re using TigerGraph Savanna 4.x as our Source of Truth. 
    Our engine performs multi-hop traversals to find connections that Vector databases miss. 
    We then pass that high-density context to Llama 3.3 via Groq for sub-2-second inference."

### **2:00 - 2:45 | The Benchmark (The Proof)**
*   **Visual**: Scroll through `benchmarking_report.md`.
*   **Speaker**: 
    "The numbers speak for themselves. We ran a 10-query 'Multi-Hop' benchmark:
    - **75.9% Token Reduction**.
    - **96.5% Factual Accuracy** verified by our AI-Judge.
    - **4x faster** than traditional methods. 
    SavannaFlow isn’t just smarter; it’s production-ready."

### **2:45 - 3:00 | Conclusion**
*   **Visual**: Dashboard showing "SYSTEM_STATUS: NOMINAL".
*   **Speaker**: 
    "SavannaFlow kills the Vector RAG Tax. By leveraging TigerGraph, we’ve made AI cheaper, faster, and more reliable. 
    Thanks for watching, and see you in the Top 10!"

---
## 🎥 Recording Tips
1. **Resolution**: Record in 1080p.
2. **Zoom**: Use `Ctrl +` to make the Dashboard text large.
3. **Audio**: Use a clear mic; background music should be low and "tech-style."
