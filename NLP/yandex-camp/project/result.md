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
| Metric    | Run 1  | Run 2  | Run 3  | Avg        |
| --------- | ------ | ------ | ------ | ---------- |
| Accuracy  | 0.8400 | 0.8000 | 0.8700 | **0.8367** |
| Precision | 0.9012 | 0.8696 | 0.8961 | **0.8890** |
| Recall    | 0.9241 | 0.9396 | 0.9517 | **0.9385** |
| F1 Score  | 0.9125 | 0.9032 | 0.9231 | **0.9129** |

  
**CoT + Few-shot** 
| Metric    | Run 1  | Run 2  | Run 3  | Avg        |
| --------- | ------ | ------ | ------ | ---------- |
| Accuracy  | 0.8200 | 0.8700 | 0.8400 | **0.8433** |
| Precision | 0.8824 | 0.8947 | 0.8774 | **0.8848** |
| Recall    | 0.9643 | 0.9315 | 0.9444 | **0.9467** |
| F1 Score  | 0.9215 | 0.9128 | 0.9097 | **0.9146** |

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
| Accuracy 1 | 0.6650 |
| Accuracy 2 | 0.7700 |
| Accuracy 3 |   -    |


**Llama + Qwen**

| Metric    | Value  |
| --------- | ------ |
| Accuracy 1 | 0.6100 |