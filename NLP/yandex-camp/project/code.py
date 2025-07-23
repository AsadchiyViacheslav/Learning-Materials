import os
import json
import ast
import openai
import re
import difflib
import pandas as pd
import numpy as np
import random
from typing import List, Dict, Optional, Any, Union
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from data_utils import load_datasets, get_table_schema, load_submission_dataset

from cag_utils import *
from llm_backend import *


class PandasCodeGeneration:
    def __init__(self, llm_backend: Optional[LLMBackend] = None):
        load_dotenv()
        self.datasets, qa_df = load_datasets()
        self.test_datasets, self.test_lite_datasets, self.test_df = load_submission_dataset()
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
            self.llm = YandexGPTBackend(folder_id, api_key, model = 'llama')
        else:
            self.llm = llm_backend

    @classmethod
    def from_yandex_gpt(cls, folder_id: str, api_key: str, **kwargs) -> 'PandasCodeGeneration':
        return cls(YandexGPTBackend(folder_id, api_key, **kwargs))

    @classmethod
    def from_vllm(cls, **kwargs) -> 'PandasCodeGeneration':
        return cls(VLLMBackend(**kwargs))
    

    def forward(self, question: str, filtered_schema: str, dataset_name: str) -> str:
        try:
            prompt = self._construct_prompt(question, filtered_schema, dataset_name)
            response = self.llm.generate(prompt)
            code = self._parse_response(response)
            
            if self._validate_code(code, filtered_schema):
                return code
            else:
                return "df.iloc[0, 0]"
                
        except Exception as e:
            print(f"Code generation error: {e}")
            return "df.iloc[0, 0]"  
    
        
    def execute_code(self, code: str, dataset_name: str, flag_submit: bool = False, use_lite: bool = False) -> Any:
        try:

            if flag_submit and use_lite:
                df = self.test_lite_datasets[dataset_name]
            elif flag_submit and not(use_lite):
                df = self.test_datasets[dataset_name]
            else:
                df = self.datasets[dataset_name]

            result = eval(code, globals(), locals())

            if isinstance(result, pd.Series) and result.dtype == bool:
                result = result.any()

            if isinstance(result, list) and len(result) == 1:
                result = result[0]

            if isinstance(result, list) and all(isinstance(x, (bool, np.bool_)) for x in result):
                result = any(result)

            formatted = self._format_result(result)
            return formatted

        except Exception as e:
            print(f"Code execution error: {e} - {use_lite} \nModel code: {code}\n")
            return None
    
    
    def _format_result(self, result: Any) -> Union[bool, str, int, float, List]:
        if isinstance(result, (bool, int, float)):
            return result
        elif isinstance(result, str):
            return result
        elif isinstance(result, (list, pd.Series)):
            if isinstance(result, pd.Series):
                result = result.tolist()
            cleaned = [self._clean_value(x) for x in result]
            if len(cleaned) == 1:
                return cleaned[0]
            return cleaned
        elif pd.isna(result):
            return None
        elif isinstance(result, (pd.Timestamp, np.datetime64)):
            return str(result.date())
        else:
            return str(result)
    
    
    def _clean_value(self, value: Any) -> Any:
        if pd.isna(value):
            return None
        elif isinstance(value, str):
            return value.strip()
        else:
            return value
        
        
    def _construct_prompt(self, question: str, filtered_schema: str, dataset_name: str) -> str:
        return f"""You are an expert pandas code generator. Given a question and a table schema, generate precise pandas code to answer the question.

Schema: {filtered_schema}
Question: "{question}"

IMPORTANT INSTRUCTIONS:
1. The DataFrame variable is named 'df'
2. Use ONLY the columns provided in the schema
3. Generate code that returns the final answer directly (not intermediate DataFrames)
4. Handle different answer types correctly:
   - Boolean: Return True/False.
   - Category: Return a single string value
   - Number: Return a numerical value (int/float)
   - List[category]: Return a list of strings (use .tolist() for Series)
   - List[number]: Return a list of numbers

EXAMPLES:

Question: "Who is the oldest billionaire?"
Schema: {{"name": "str", "age": "int"}}
Code: df.nlargest(1, 'age')['name'].iloc[0]

Question: "What is the average net worth?"
Schema: {{"netWorth": "float"}}
Code: df['netWorth'].mean()

Question: "How many billionaires are from the USA?"
Schema: {{"country": "category"}}
Code: len(df[df['country'] == 'USA'])

Question: "List all unique industries"
Schema: {{"industry": "category"}}
Code: df['industry'].unique().tolist()

Question: "Is there a billionaire over the age of 90 with a salary of more than 100?"
Schema: {{"age": "int", "salary": "int"}}
Code: ((df['age'] > 90) & (df['salary'] > 100)).any()

Question: "What are the top 3 net worth values?"
Schema: {{"netWorth": "float"}}
Code: df.nlargest(3, 'netWorth')['netWorth'].tolist()

COMMON PATTERNS:
- For "oldest/youngest": use nlargest()/nsmallest() with iloc[0]
- For "maximum/minimum": use max()/min() or nlargest()/nsmallest(). Don't use nlargest or nsmallest on non-numeric columns!
- For "average/mean": use .mean()
- For "count/how many": use len() with filtering
- For "all/list": use .unique().tolist() or .tolist()
- For filtering: use boolean indexing df[df['column'] == value]
- For existence questions: use .any() or .sum() > 0
- For string matching: use .str.contains() for partial matches
- Handle case sensitivity with .str.lower() if needed
- For Boolean questions like "Is there any ...", return a single True/False using .any() or .all


Output Format:
Generate ONLY the pandas code. Do not include explanations or comments.
The code should be executable and return the answer directly.
Output ONLY the final result as a Pandas code on the last line
"""

    
    def _parse_response(self, response: str) -> str:
        try:
            content = response.strip()
            if not content:
                raise ValueError("Empty response")

            lines = [line.strip() for line in content.splitlines() if line.strip()]
            if not lines:
                raise ValueError("No valid lines in response")

            code_line = lines[-1]
            
            if code_line.startswith('Code:'):
                code_line = code_line[5:].strip()
            code_line = re.sub(r'^```(python)?|```$', '', code_line).strip()
            code_line = re.sub(r'^\d+\.\s*', '', code_line)
            
            return code_line.strip()

        except Exception as e:
            print(f"Error parsing response: {e}\nRaw response: {response}")
            return "df.iloc[0, 0]"
    
    
    def _validate_code(self, code: str, schema: str) -> bool:
        try:
            if not code or not isinstance(code, str):
                return False

            dangerous_ops = ['exec', 'eval', '__', 'import', 'open', 'file']
            if any(op in code for op in dangerous_ops):
                return False

            if 'df' not in code:
                return False

            try:
                schema_dict = json.loads(schema)
                schema_columns = set(schema_dict.keys())

                # Здесь ищем строки вида df['col'] или df["col"]
                used_columns = set(re.findall(r"df\[['\"](.*?)['\"]\]", code))

                for col in used_columns:
                    if col not in schema_columns:
                        # Найти самое похожее название
                        closest = difflib.get_close_matches(col, schema_columns, n=1, cutoff=0.6)
                        if not closest:
                            return False 
                        code = code.replace(f"df['{col}']", f"df['{closest[0]}']")
                        code = code.replace(f'df["{col}"]', f'df["{closest[0]}"]')
            except:
                return False 

            return True

        except Exception:
            return False
    
    
    def make_submit(self, column_generator=None):
        size = len(self.test_df)

        random.seed(42)
        
        all_predictions_full = []
        all_predictions_lite = []
    
        sample_df = self.test_df
        

        for i in tqdm(range(size), desc="Making submission"):
            question = sample_df.loc[i, "question"]
            dataset_name = sample_df.loc[i, "dataset"]
            
            if column_generator:
                full_schema = get_table_schema(self.test_datasets[dataset_name])
                filtered_schema = column_generator.predict(question, full_schema)
            else:
                filtered_schema = get_table_schema(self.test_datasets[dataset_name])

            generated_code = self.forward(question, filtered_schema, dataset_name)
            
            answer_full = self.execute_code(generated_code, dataset_name, flag_submit = True, use_lite=False)
            answer_lite = self.execute_code(generated_code, dataset_name, flag_submit = True, use_lite=True)
            
            if answer_full is None:
                answer_full = "None"
            if answer_lite is None:
                answer_lite = "None"
                
            all_predictions_full.append(str(answer_full))
            all_predictions_lite.append(str(answer_lite))
            
            with open("predictions.txt", "w", encoding="utf-8") as f_pred:
                for pred in all_predictions_full:
                    f_pred.write(pred.strip() + "\n")

            with open("predictions_lite.txt", "w", encoding="utf-8") as f_lite:
                for pred in all_predictions_lite:
                    f_lite.write(pred.strip() + "\n")

        print("------------------SUBMIT READY------------------")
    
    
    def eval(self, size: int = None, log: bool = False, val: bool = False, column_generator=None):
        if size is None:
            size = len(self.val_df) if val else len(self.train_df)

        random.seed(42)
        sample_df = self.val_df.sample(n=size).reset_index(drop=True) if val else self.train_df.sample(n=size).reset_index(drop=True)

        correct_answers = 0
        total_questions = len(sample_df)

        for i in tqdm(range(len(sample_df)), desc="Evaluating Pandas Code Generation"):
            question = sample_df.loc[i, "question"]
            dataset_name = sample_df.loc[i, "dataset"]
            true_answer = sample_df.loc[i, "answer"]
            
            if column_generator:
                full_schema = get_table_schema(self.datasets[dataset_name])
                filtered_schema = column_generator.predict(question, full_schema)
            else:
                filtered_schema = get_table_schema(self.datasets[dataset_name])

            generated_code = self.forward(question, filtered_schema, dataset_name)
            predicted_answer = self.execute_code(generated_code, dataset_name)
            
            is_correct = self._compare_answers(predicted_answer, true_answer)
            if is_correct:
                correct_answers += 1
                
            if log:
                print(f"Generated code: {generated_code} ---- Predicted: {predicted_answer} ---- Answer: {true_answer}")

        accuracy = correct_answers / total_questions
        print(f"\n=== Pandas Code Generation Evaluation ===")
        print(f"Total questions: {total_questions}")
        print(f"Correct answers: {correct_answers}")
        print(f"Accuracy: {accuracy:.4f}")
    
    
    def _compare_answers(self, predicted: Any, true: Any) -> bool:
        try:
            if predicted is None and true is None:
                return True
            if predicted is None or true is None:
                return False
                
            if isinstance(true, bool) or str(true).lower() in ['true', 'false']:
                pred_bool = self._parse_bool(predicted)
                true_bool = self._parse_bool(true)
                return pred_bool == true_bool
            
            if isinstance(true, (list, str)) and (isinstance(predicted, list) or str(predicted).startswith('[')):
                pred_list = self._parse_list(predicted)
                true_list = self._parse_list(true)
                if pred_list is not None and true_list is not None:
                    pred_sorted = sorted([str(x).strip().lower() for x in pred_list])
                    true_sorted = sorted([str(x).strip().lower() for x in true_list])
                    return pred_sorted == true_sorted
            
            try:
                pred_num = float(predicted)
                true_num = float(true)
                return abs(pred_num - true_num) < 1e-6
            except (ValueError, TypeError):
                pass
            
            try:
                pred_date = str(pd.to_datetime(predicted).date())
                true_date = str(pd.to_datetime(true).date())
                return pred_date == true_date
            except (ValueError, TypeError):
                pass
            

            pred_str = str(predicted).strip().lower()
            true_str = str(true).strip().lower()
            return pred_str == true_str
            
        except Exception as e:
            print(f"Error comparing answers: {e}")
            return False
    
    
    def _parse_bool(self, value: Any) -> Optional[bool]:
        if isinstance(value, (bool, np.bool_)):
            return bool(value)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            val_lower = value.strip().lower()
            if val_lower in ['true', 'y', 'yes']:
                return True
            elif val_lower in ['false', 'n', 'no']:
                return False
        print(f"Strange bool type {value}, {type(value)}")
        return None
    
    
    def _parse_list(self, value: Any) -> Optional[List]:
        if isinstance(value, list):
            return value

        if isinstance(value, str):
            value = value.strip()
            if value.startswith('[') and value.endswith(']'):
                try:
                    parsed = ast.literal_eval(value)
                    if isinstance(parsed, list):
                        return parsed
                except (ValueError, SyntaxError):
                    pass

                inner = value[1:-1]
                raw_items = [item.strip() for item in inner.split(',')]

                def try_cast(val):
                    try:
                        if '.' in val:
                            return float(val)
                        else:
                            return int(val)
                    except ValueError:
                        return val 

                return [try_cast(x) for x in raw_items]

        return None