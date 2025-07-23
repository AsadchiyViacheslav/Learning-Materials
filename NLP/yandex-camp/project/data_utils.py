import os
import re
import numpy as np
import pandas as pd
import json
import emoji

DATASET_DIR = "/home/jupyter/mnt/datasets/main_dataset/data"

TEST_DIR = "/home/jupyter/mnt/datasets/submission_dataset/competition"

def clean_column_name(col_name: str) -> str:
    """
    Очищает название колонки от html-тегов и эмодзи.
    """
    col_name = re.sub(r"<[^>]*>", "", col_name)

    col_name = ''.join(c for c in col_name if not emoji.is_emoji(c))

    return col_name.strip()

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_columns = {col: clean_column_name(col) for col in df.columns}
    return df.rename(columns=cleaned_columns)

def load_datasets(main_dir: str = DATASET_DIR) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """
    Загружает базу знаний из parquet файлов хранящихся в директории датасета
    Загружает файл вопросы - ответы (qa) для тренировки и валадиции
    
    Возвращает:
    1. Словарь {'Название датасета', Датасет}
    2. Датасет QA - со всеми вопросами ответами
    """
    datasets = {}
    all_qa = []

    for folder_name in os.listdir(main_dir):
        folder_path = os.path.join(main_dir, folder_name)

        if not os.path.isdir(folder_path):
            continue

        dataset_path = os.path.join(folder_path, "all.parquet")
        qa_path = os.path.join(folder_path, "qa.parquet")

        if os.path.isfile(dataset_path) and os.path.isfile(qa_path):
            try:
                df = pd.read_parquet(dataset_path)
                qa_df = pd.read_parquet(qa_path)

                df = rename_columns(df)
                
                datasets[folder_name] = df
                all_qa.append(qa_df)
            except Exception as e:
                print(f"Ошибка при загрузке данных из папки '{folder_name}': {e}")

    qa_df_combined = pd.concat(all_qa, ignore_index=True)

    return datasets, qa_df_combined

def load_submission_dataset(main_dir: str = TEST_DIR) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """
    Загружает базу знаний из parquet файлов хранящихся в директории датасета для сабмита.
    Загружает файл вопросы - ответы (qa) для сабмита.
    """
    datasets = {}
    datasets_lite = {}
    
    test_df = pd.read_csv("/home/jupyter/mnt/datasets/submission_dataset/competition/test_qa.csv")

    for folder_name in os.listdir(main_dir):
        folder_path = os.path.join(main_dir, folder_name)

        if not os.path.isdir(folder_path):
            continue

        dataset_path = os.path.join(folder_path, "all.parquet")
        dataset_lite_path = os.path.join(folder_path, "sample.parquet")

        if os.path.isfile(dataset_path) and os.path.isfile(dataset_lite_path):
            try:
                df = pd.read_parquet(dataset_path)
                df_lite = pd.read_parquet(dataset_lite_path)

                df = rename_columns(df)
                df_lite = rename_columns(df_lite)
                
                datasets[folder_name] = df
                datasets_lite[folder_name] = df_lite
            except Exception as e:
                print(f"Ошибка при загрузке данных из папки '{folder_name}': {e}")

    return datasets, datasets_lite, test_df

def get_table_schema(df: pd.DataFrame) -> dict[str, str]:
    """
    Принимает таблицу (DataFrame) и возвращает строку json вида:
    {
        "user_id": "number[uint64]",
        "is_active": "boolean",
    }
    """
    schema = {}

    for col in df.columns:
        dtype = df[col].dtype
        series = df[col]

        if pd.api.types.is_integer_dtype(dtype):
            schema[col] = "int"
        elif pd.api.types.is_float_dtype(dtype):
            schema[col] = "float"
        elif pd.api.types.is_bool_dtype(dtype):
            schema[col] = "bool"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            schema[col] = "date"
        elif pd.api.types.is_categorical_dtype(dtype):
            schema[col] = "category"
        elif pd.api.types.is_object_dtype(dtype):
            if series.dropna().apply(lambda x: isinstance(x, list)).all():
                schema[col] = "list"
            elif series.dropna().apply(lambda x: isinstance(x, str)).mean() > 0.9:
                string_series = series[series.apply(lambda x: isinstance(x, str))]
                unique_vals = string_series.nunique(dropna=True)
                if unique_vals <= 100:
                    schema[col] = "category"
                else:
                    schema[col] = "str"
        else:
            schema[col] = "str"

    return json.dumps(schema, indent=2, ensure_ascii=False)