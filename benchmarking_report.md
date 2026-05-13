# 📊 Official Benchmark Report: GraphRAG vs. Basic RAG

## 🏆 Headline Results
- **Token Reduction**: 69.2% reduction using GraphRAG.
- **Cost Savings**: Estimated 3x lower inference costs at scale.
- **Accuracy**: GraphRAG maintained 100% pass rate on multi-hop relationship queries.

## 📈 Performance Summary
| Metric | LLM-Only | Basic RAG | **GraphRAG** |
| :--- | :---: | :---: | :---: |
| **Avg Tokens** | 1302.6 | 1371.6 | **422.7** |
| **Avg Latency** | 3.52s | 5.71s | **2.07s** |
| **Accuracy (Pass %)** | 100.0% | 90.0% | **100.0%** |

## 📝 Query Log
| Question                                                                |   LLM Only Tokens |   Basic RAG Tokens |   GraphRAG Tokens |
|:------------------------------------------------------------------------|------------------:|-------------------:|------------------:|
| What are the mission durations for Apollo 11 vs Artemis 3?              |              1166 |               1325 |               584 |
| Which launch vehicles were used in the Apollo program vs Artemis?       |              2683 |               1375 |               438 |
| Compare the crew size of Apollo 11 and Artemis 1.                       |               453 |               1373 |               236 |
| What are the primary scientific goals of the Artemis mission?           |              1391 |               1476 |               536 |
| Which spacecraft components are shared across different Artemis phases? |              2119 |               1478 |               638 |
| Who were the commanders of the first moon landing?                      |               509 |               1281 |               473 |
| What is the role of the Gateway in the Artemis program?                 |               959 |               1355 |               535 |
| How many astronauts are planned for the Artemis lunar surface crew?     |               705 |               1283 |               199 |
| What rockets were used to launch the Orion spacecraft?                  |              1020 |               1350 |               259 |
| Compare the payload capacity of Saturn V and SLS.                       |              2021 |               1420 |               329 |

---
*Generated on: 2026-05-14 00:31:43*
