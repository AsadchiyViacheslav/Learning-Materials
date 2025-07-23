import os
import json
import ast
import openai
import re
import emoji
import random
from typing import List, Tuple, Dict, Optional
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from data_utils import load_datasets, get_table_schema

from llm_backend import *


class ColumnAwareGeneration:
    def __init__(self, llm_backend: Optional[LLMBackend] = None):
        load_dotenv()
        self.datasets, qa_df = load_datasets()
        self.train_df, self.val_df = train_test_split(
            qa_df,
            test_size=0.3,
            random_state=42,
            shuffle=True
        )
        
        if llm_backend is None:
            folder_id = os.getenv("YANDEX_CLOUD_FOLDER")
            api_key = os.getenv("YANDEX_CLOUD_API_KEY")
            if not folder_id or not api_key:
                raise ValueError("Missing Yandex Cloud credentials in environment variables")
            self.llm = YandexGPTBackend(folder_id, api_key)
        else:
            self.llm = llm_backend

    @classmethod
    def from_yandex_gpt(cls, folder_id: str, api_key: str, **kwargs) -> 'ColumnAwareGeneration':
        return cls(YandexGPTBackend(folder_id, api_key, **kwargs))

    @classmethod
    def from_vllm(cls, **kwargs) -> 'ColumnAwareGeneration':
        return cls(VLLMBackend(**kwargs))
    
    
    def build_few_shot_messages(self, question: str, schema: str) -> List[Dict[str, str]]:
        num_examples = max(2, len(self.train_df) // 10)
        few_shot_df = self.train_df.sample(n=num_examples, random_state=random.randint(0, 9999)).reset_index(drop=True)
        examples = random.sample(list(few_shot_df.itertuples(index=False)), k=2)

        messages = []

        for ex in examples:
            schema_example = get_table_schema(self.datasets[ex.dataset])
            true_cols = self._fix_and_parse(ex.columns_used)
            prompt = self._construct_prompt(ex.question, schema_example)
            messages.append({"role": "user", "content": prompt})
            messages.append({"role": "assistant", "content": json.dumps(true_cols, ensure_ascii=False)})

        final_prompt = self._construct_prompt(question, schema)
        messages.append({"role": "user", "content": final_prompt})

        return messages


    def forward(self, question: str, schema: str) -> List[str]:
        prompt = self._construct_prompt(question, schema)
        response = self.llm.generate(prompt)
        return self._parse_response(response)
    
    
    def few_shot_forward(self, question: str, schema: str) -> List[str]:
        messages = self.build_few_shot_messages(question, schema)
        response = self.llm.generate(messages=messages)
        return self._parse_response(response)
    
    
    def predict(self, question: str, schema: str) -> List[str]:
        try:
            schema_dict = json.loads(schema)
            schema_keys = set(schema_dict.keys())

            prompt = self._construct_prompt(question, schema)
            response = self.llm.generate(prompt)
            predicted_cols = self._parse_response(response)

            if not predicted_cols:
                return schema

            if all(col in schema_keys for col in predicted_cols):
                filtered_schema = {col: schema_dict[col] for col in predicted_cols}
                return json.dumps(filtered_schema, ensure_ascii=False)
            else:
                return schema
        except Exception as e:
            print(f"Predict error: {e}")
            return schema
        
        
    def _construct_prompt(self, question: str, schema: str) -> str:
        return f"""You are an expert data extraction assistant specialized in schema analysis. 
Given a table schema and a user question, your task is to precisely identify the minimal set of columns needed to answer the question.

Input:
- Table Schema: {schema}
- User Question: "{question}"

IMPORTANT INSTRUCTIONS:
- USE THE COLUMN NAMES EXACTLY AS GIVEN IN THE SCHEMA. Do not rephrase, rename, or alter them in any way.
- DO NOT invent new column names. ONLY use what exists in the schema.
- DO NOT generalize or infer information that is not directly mappable to specific schema columns.

Reasoning process:
1. Identify the key concepts or filters in the user question.
2. Match these concepts precisely to column names from the schema.
3. If several columns could apply, choose only the most directly relevant ones.
4. Ensure the final list of columns is minimal but sufficient to answer the question.

Example:
Question: "Who is the oldest billionaire with a philanthropy score of 5?"
• Step 1: Key Concepts in the Question → "oldest billionaire", "philanthropy score of 5", "who"
• Step 2: Schema match → columns related to "oldest", "philanthropy score of 5", "who"
• Step 3: Most relevant columns → "age", "philanthropyScore", "name"
• Step 4: Final output → ["name", "age", "philanthropyScore"]

Output Format:
1. Perform all reasoning internally - DO NOT show working steps
2. Output ONLY the final result as a Python list on the last line
3. Ensure the list contains ONLY exact schema column names
4. Format the output precisely as: ["column1", "column2"]
"""

    def _parse_response(self, response: str) -> List[str]:
        
        result = "<no response>"
        
        try:

            content = response
            if content is None:
                raise ValueError("No content in response")

            result = content.strip()
            
            lines = [line.strip() for line in result.splitlines() if line.strip()]
            if len(lines) < 1:
                raise ValueError("Response doesn't contain enough lines for columns and types.")

            columns_line = lines[-1]
            
            columns = ast.literal_eval(columns_line)

            return columns
        except Exception as e:
            print(f"Error parsing response: {e}\nRaw response: {response}")
            return []

        
    def _fix_and_parse(self, lst: str) -> List[str]:
        try:
            if isinstance(lst, list):
                result = lst
            else:
                try:
                    result = ast.literal_eval(lst)
                except Exception:
                    stripped = lst.strip()
                    if stripped.startswith("[") and stripped.endswith("]"):
                        content = stripped[1:-1].replace("'", "").replace('"', '')
                        items = [x.strip() for x in content.split(",") if x.strip()]
                        fixed = "[" + ", ".join(f"'{x}'" for x in items) + "]"
                        try:
                            result = ast.literal_eval(fixed)
                        except Exception:
                            print(f"_fix_and_parse: failed to fix list-like string: {lst}")
                            return []
                        
            def clean_value(x: str) -> str:
                x = str(x)

                x = re.sub(r"<[^>]*>", "", x)

                x = ''.join(c for c in x if not emoji.is_emoji(c))

                return x.strip()

            cleaned = [clean_value(x) for x in result]
            return cleaned
        
        except Exception as e:
            print(f"_fix_and_parse failed: {e}, answer {lst} {type(lst)}")
            return []
    
    
    def eval(self, size: int = None, log: bool = False, val: bool = False):
        if size is None:
            size = len(self.val_df) if val else len(self.train_df)

        random.seed(42)
        sample_df = self.val_df.sample(n=size).reset_index(drop=True) if val else self.train_df.sample(n=size).reset_index(drop=True)

        y_true = []  
        y_pred = []  
        correct_matches = 0

        for i in tqdm(range(len(sample_df)), desc="Evaluating"):
            question = sample_df.loc[i, "question"]
            dataset_name = sample_df.loc[i, "dataset"]
            schema = get_table_schema(self.datasets[dataset_name])

            true_cols = sample_df.loc[i, "columns_used"]
            true_cols = self._fix_and_parse(true_cols)

            predicted_cols = self.few_shot_forward(question, schema)
            if log:
                print(f"Pred {predicted_cols} Answer {true_cols}")
                
            sorted_true = sorted(true_cols)
            sorted_pred = sorted(predicted_cols)

            y_true.append(sorted_true)
            y_pred.append(sorted_pred)

            if sorted_pred == sorted_true:
                correct_matches += 1 

        mlb = MultiLabelBinarizer()
        mlb.fit(y_true + y_pred)
        y_true_bin = mlb.transform(y_true)
        y_pred_bin = mlb.transform(y_pred)  

        precision = precision_score(y_true_bin, y_pred_bin, average="micro")
        recall = recall_score(y_true_bin, y_pred_bin, average="micro")
        f1 = f1_score(y_true_bin, y_pred_bin, average="micro")
        accuracy = correct_matches / len(sample_df)

        print("\n=== Evaluation ===")
        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")