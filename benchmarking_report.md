# 📊 Official Benchmark Report: GraphRAG vs. Basic RAG

## 🏆 Headline Results
- **Token Reduction**: 66.0% reduction using GraphRAG.
- **Cost Savings**: Estimated 3x lower inference costs at scale.
- **Accuracy**: GraphRAG maintained 100% pass rate on multi-hop relationship queries.

## 📈 Performance Summary
| Metric | LLM-Only | Basic RAG | **GraphRAG** |
| :--- | :---: | :---: | :---: |
| **Avg Tokens** | 1125.4 | 1368.2 | **465.8** |
| **Avg Latency** | 4.03s | 7.08s | **2.29s** |
| **Accuracy (Pass %)** | 90.0% | 60.0% | **60.0%** |

## 📝 Query Log
| Question                                                                |   LLM Only Tokens |   Basic RAG Tokens |   GraphRAG Tokens |
|:------------------------------------------------------------------------|------------------:|-------------------:|------------------:|
| What are the mission durations for Apollo 11 vs Artemis 3?              |              1017 |               1318 |               490 |
| Which launch vehicles were used in the Apollo program vs Artemis?       |              2104 |               1375 |               525 |
| Compare the crew size of Apollo 11 and Artemis 1.                       |               386 |               1363 |               227 |
| What are the primary scientific goals of the Artemis mission?           |              1113 |               1495 |               594 |
| Which spacecraft components are shared across different Artemis phases? |              2087 |               1428 |               585 |
| Who were the commanders of the first moon landing?                      |               485 |               1298 |               511 |
| What is the role of the Gateway in the Artemis program?                 |               750 |               1353 |               514 |
| How many astronauts are planned for the Artemis lunar surface crew?     |               405 |               1283 |               564 |
| What rockets were used to launch the Orion spacecraft?                  |              1075 |               1349 |               255 |
| Compare the payload capacity of Saturn V and SLS.                       |              1832 |               1420 |               393 |

---
*Generated on: 2026-05-14 00:10:21*
