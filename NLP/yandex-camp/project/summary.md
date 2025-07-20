# SemEval2025 Task - 8 

## Solution

### Основная идея

Основная идея — существенно уменьшить табличный контекст, сначала выбрав релевантные столбцы, а затем использовать LLM для генерации ответа только на основе этих столбцов. Это решает проблему слишком больших таблиц, которые нельзя напрямую вставить в prompt.

Схема: вопрос -> LLM -> столбцы -> LLM -> pandas code -> ответ

### Column-Augmented Generation (CAG)

Структурированные представления каждого столбца (включая имя, тип, мин/макс значения и наиболее частые значения)

Промпт вида
```
Given a table contains columns with names <list of column names>, I want to answer a question:
<question>.

Please select a few column names from the list <list of column names>, the values of which will
help answer the question.

Please provide a list of column names in the list format without any additional explanations.
```

```
Given a table contains columns with names <list of column names>, I want to answer a question:
<question>.

Please select a few column names from the list <list of column names>, the values of which will
help answer the question.

Please provide a list of column names in the list format without any additional explanations.
```

Ответ LLM: `["column_1", "column_2", "column_3"]`

### Генерация pandas code

```
# Examples:
# Example 1:
# Question: <question>
# Answer: <answer>
# Example 2: . . .
—–
# Instructions:
# Implement the following function in one line.
# Answer with the function only with no additional explanations.
# The function must return one of these types: bool, int, str, list[int], or list[str].
# Formatting rules:
# 1) Answer with the function only. No comments, no additional explanations.
# 2) Your answer should start with: def answer
# 3) The function should be implemented in one line
# Your task: complete the following function in one line. It should give the answer to: {question}
def answer(df: pd.DataFrame):
df.columns = {list_columns}
return
```

| Проблема                              | Решение                                               |
| ------------------------------------- | ----------------------------------------------------- |
| ❗ LLM может ошибаться в синтаксисе    | Использовать `try/except`, перегенерацию, self-refine |
| ❗ Ответ может быть не в коде          | Жёстко требовать: “верни только `python` код”         |

 Если при выполнении возникала ошибка, применялся метод self-refine с передачей исключения в промпт.

### Reasoning Prompting Techniques
Чтобы повысить надёжность и точность, применяются несколько техник:

- 📍 Chain-of-Thought (CoT)
Заставляет модель думать пошагово: "Let’s think step by step".

- 📍 Self-Consistency
Модель вызывается несколько раз (3–10).
 Все ответы агрегируются → выбирается наиболее частый.

- 📍 Self-Refine
Модель проверяет себя: оценивает правильность ответа и при необходимости сама перегенерирует его.

| Подход                        | EM (точность) |
| ----------------------------- | ------------- |
| Llama-3.1-8B-Instruct         | 27.78%        |
| + CAG                         | 37.93%        |
| + CAG + CoT                   | 64.87%        |
| + CAG + CoT + Consistency(10) | **81.99%**    |
| DeepSeek-R1-32B + CAG         | **83.52%**    |

---

Кроме того, подходы к построению QA-систем на табличных данных могут быть дополнительно усилены за счёт использования графов знаний

## Basic solution - как поместить контекст 100 т. строк

CAG +:

-  **Ранжирование строк (row retrieval)**  
Идея: как ты выбрал релевантные столбцы, теперь выбери   релевантные строки.   
Алгоритмы:  
Dense retrieval (например, с BGE, ColBERT)   
BM25 (если ты хочешь быстро и по ключевым словам)  
Hybrid retrieval (BGE + BM25)  

- **LLM-assisted row filtering**  
Промптируешь LLM: «вот названия колонок, вот вопрос — какие строки релевантны?»

- **Pre-aggregation**  
 Выполнить агрегацию средствами Pandas

---

## Способы дообучения LLM

| Вид обучения                         | Суть                                                                 | Плюсы                                                                 | Минусы                                                                 |
|-------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------|------------------------------------------------------------------------|
| **Few-shot prompting**              | Примеры в prompt без обучения                                        | - Без затрат<br>- Быстро тестировать<br>- Гибкий prompt               | - Не обучает модель<br>- Ограничен контекстом<br>- Не стабильно       |
| **Zero-shot prompting**             | Один prompt без примеров                                             | - Вообще без данных<br>- Просто                                        | - Часто низкое качество                                                |
| **Supervised Fine-Tuning (SFT)**    | Дообучение на (инструкция → ответ)                                   | -Управляемость<br>- Улучшает качество<br>- Хорошо для кастомизации   | - Требует данных<br>- Затратно<br>- Риск забывания                     |
| **LoRA / QLoRA**                    | Обучение части параметров модели (адаптеры)                          | - Лёгкое обучение<br>- Эффективно<br>- Можно отключать адаптацию      | - Немного хуже SFT<br>- Требует PEFT-фреймворки                        |
| **Full fine-tuning**                | Обучение всех весов модели                                           | - Макс. контроль<br>- Лучшая адаптация                               | - Очень ресурсоёмко<br>- Сложно масштабировать                         |
| **RLHF / DPO**                      | Дообучение по предпочтениям (A > B)                                  | - Лучше слушает пользователя<br>- Улучшает тон и стиль ответов        | - Трудно собрать предпочтения<br>- Сложное обучение                    |
| **Retrieval fine-tuning**           | Дообучение retriever'а на парах (вопрос, релевантный документ)       | - Лучше поиск<br>- Увеличивает качество RAG                           | - Требует разметки<br>- Отдельный процесс обучения                     |
| **End-to-end RAG tuning**           | Совместное обучение retriever + generator                            | - Оптимизация всей цепочки<br>- Лучшая связка компонентов             | - Сложно реализовать<br>- Требует архитектурной поддержки              |
