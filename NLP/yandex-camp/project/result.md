# CAG

## Metrics API   

### Llama   
**base:**
| Metric    | Value  |
| --------- | ------ |
| Accuracy  | 0.7700 |
| Precision | 0.8200 |
| Recall    | 0.8425 |
| F1 Score  | 0.8311 |
  
  
**CoT:**  
| Metric    | Avg        |
| --------- | ---------- |
| Accuracy  | **0.8367** |
| Precision | **0.8890** |
| Recall    | **0.9385** |
| F1 Score  | **0.9129** |

  
**CoT + Few-shot** 
| Metric     | Avg        |
| ---------  | ---------- |
| Accuracy   | **0.8433** |
| Precision  | **0.8848** |
| Recall     | **0.9467** |
| F1 Score   | **0.9146** |

---

### Qwen

**base:**
| Metric    | Run 1  | Run 2 |
| --------- | ------ | ----- |
| Accuracy  | 0.8700 | 0.8700 |
| Precision | 0.9245 | 0.9050 |
| Recall    | 0.9071 | 0.9062 |
| F1 Score  | 0.9442 | 0.9152 | 

  
**Few-shot** 
| Metric    | Run 1  | Run 2  | Run 3  | Avg        |
| --------- | ------ | ------ | ------ | ---------- |
| Accuracy  | 0.8700 | 0.9000 | 0.8600 | **0.8767** |
| Precision | 0.9847 | 0.9714 | 0.9701 | **0.9754** |
| Recall    | 0.8658 | 0.9315 | 0.8609 | **0.8861** |
| F1 Score  | 0.9214 | 0.9510 | 0.9123 | **0.9282** |

## Metrics local models with vLLM  

### DeepSeek-R1-Distill-Qwen-32B-quantized.w4a16

**Base:**  
| Metric    | Value  |
| --------- | ------ |
| Accuracy  | 0.7300 |
| Precision | 0.8409 |
| Recall    | 0.9427 |
| F1 Score  | 0.8889 |

**Few-shot:** 
| Metric    | Value  |
| --------- | ------ |
| Accuracy  | 0.7400 |
| Precision | 0.8198 |
| Recall    | 0.8981 |
| F1 Score  | 0.8571 |

# Code generation

## Metrics API  

**Llama + Llama**

| Metric    | Value  |
| --------- | ------ |
| Accuracy 1 | 0.7600 |
| Accuracy 2 + CoT |   0.7300    |

**Llama without CAG**
| Metric    | Value  |
| --------- | ------ |
| Accuracy 1 | 0.69 |

**Llama + Qwen**

| Metric    | Value  |
| --------- | ------ |
| Accuracy 1 | 0.6100 |



# Competition metrics

| Model    | EM  |
| --------- | ------ |
| LLlama + Llama full | 69.5 |
| LLlama + Llama without cag | 65.43 |
| LLlama + Llama without cag and fsp | 14.94 |
| DeepSeek-R1-Distill-Qwen-32B-quantized.w4a16 + Llama full| 68.58 |
| Llama full + DeepSeek-R1-Distill-Qwen-32B-quantized.w4a16 | 45.79 |
| Llama full + Qwen/Qwen2.5-Coder-32B-Instruct | 73.37 |

