# 🎬 SavannaFlow: The GraphRAG Precision Engine
## **Demo Video Script // TigerGraph Savanna Hackathon**

---

### **0:00 - 0:30 | The Hook (The "Vector RAG Tax")**
*   **Visual**: Open the SavannaFlow Dashboard (Vercel).
*   **Speaker**: 
    "Hi everyone! I'm Ronit, and today we're killing the 'Vector RAG Tax.' 
    Standard AI systems are slow, expensive, and noisy because they pull in massive, irrelevant text chunks. 
    We built **SavannaFlow**—a next-gen GraphRAG engine that proves TigerGraph is the key to 100% precise, low-cost AI."

---

### **0:30 - 1:15 | Scene 1: The 3.5x Efficiency Battle**
*   **Action**: Type the Query: *"Compare the payload capacity to LEO of the Saturn V and the SLS Block 1."*
*   **Visual**: Zoom in on the **TOKEN** and **COST** metrics for all three columns.
*   **Speaker**: 
    "Look at this. 
    On the left, the **LLM** is guessing. 
    In the middle, **Basic RAG** is struggling. It pulled over **1,200 tokens** of noisy text chunks just to find a few numbers. 
    But on the right, **SavannaFlow (GraphRAG)** is surgically precise. It retrieved only the specific attribute nodes from TigerGraph, using just **350 tokens**. 
    That’s a **3.5x reduction in cost** with zero loss in quality. That is the Graph Advantage."

---

### **1:15 - 2:00 | Scene 2: Solving Retrieval Failure**
*   **Action**: Type the Query: *"What are the primary differences between the F-1 and J-2 engines used in Apollo?"*
*   **Visual**: Highlight the **"I don't know"** answer in the Basic RAG column vs the **perfect table** in GraphRAG.
*   **Speaker**: 
    "Standard RAG often fails when questions get specific. 
    Notice how Basic RAG gave up because the keywords didn't match perfectly. 
    SavannaFlow didn't blink. Because our data is a structured Graph, we traversed the relationships between the Saturn V stages and their specific engines. 
    We don't just find text; we find the truth."

---

### **2:00 - 2:45 | Scene 3: The Architecture (The Secret Sauce)**
*   **Visual**: Show the **ARCHITECTURE.md** diagram or the Mermaid flow.
*   **Speaker**: 
    "How does it work? We use **TigerGraph Savanna 4.x** as our structural Source of Truth. 
    When a query hits our API, we perform multi-hop traversals to pull high-density context. 
    We then pass that clean context to **Llama 3.3 via Groq**, achieving sub-2-second inference speeds. 
    By bypassing the 'Vector Search' step, we eliminate noise and ensure every token you pay for is a token that matters."

---

### **2:45 - 3:00 | The Outro (The Call to Action)**
*   **Visual**: Show the "System Status: NOMINAL" and the GitHub repo.
*   **Speaker**: 
    "SavannaFlow isn't just a RAG system—it's the future of cost-effective, high-precision AI. 
    3.5x cheaper. 100% reliable. Powered by TigerGraph. 
    Check out the code on GitHub and join the flow. Thanks for watching!"

---

### **💡 Pro-Tips for Recording:**
1.  **Cursor Movement**: Use your mouse to point at the **Cost ($)** and **Tokens** counters while you speak.
2.  **Pacing**: Wait for the "Execute" animation to finish before speaking about the results.
3.  **The "Wow" Factor**: Emphasize the word **"Surgical"** when talking about GraphRAG—it’s our core brand! 🐯🥇🚀🏗️
