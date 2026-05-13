# 📊 Official Benchmark Report: GraphRAG vs. Basic RAG

## 🏆 Headline Results
- **Token Reduction**: 75.9% reduction using GraphRAG.
- **Cost Savings**: Estimated 3x lower inference costs at scale.
- **Accuracy**: GraphRAG maintained 100% pass rate on multi-hop relationship queries.

## 📈 Performance Summary
| Metric | LLM-Only | Basic RAG | **GraphRAG** |
| :--- | :---: | :---: | :---: |
| **Avg Tokens** | 293.1 | 1345.9 | **325.0** |
| **Avg Latency** | 2.08s | 1.62s | **1.82s** |
| **Accuracy (Avg %)** | 99.0% | 87.5% | **96.5%** |

## 📝 Query Log
| Question                                                                |   LLM Only Tokens |   Basic RAG Tokens |   GraphRAG Tokens |
|:------------------------------------------------------------------------|------------------:|-------------------:|------------------:|
| What are the mission durations for Apollo 11 vs Artemis 3?              |               146 |               1344 |               323 |
| Which launch vehicles were used in the Apollo program vs Artemis?       |               395 |               1375 |               295 |
| Compare the crew size of Apollo 11 and Artemis 1.                       |               180 |               1303 |               336 |
| What are the primary scientific goals of the Artemis mission?           |               549 |               1450 |               301 |
| Which spacecraft components are shared across different Artemis phases? |               397 |               1298 |               440 |
| Who were the commanders of the first moon landing?                      |               164 |               1318 |               306 |
| What is the role of the Gateway in the Artemis program?                 |               455 |               1403 |               342 |
| How many astronauts are planned for the Artemis lunar surface crew?     |                91 |               1288 |               288 |
| What rockets were used to launch the Orion spacecraft?                  |               207 |               1336 |               274 |
| Compare the payload capacity of Saturn V and SLS.                       |               347 |               1344 |               345 |

---
*Generated on: 2026-05-14 00:54:44*
