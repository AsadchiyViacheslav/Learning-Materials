# Yandex GO Scooters ML 🛴

Ноутбуки с обучением моделей, загрузкой и разделением данных, агументацией, конвертацией моделей и их оценкой в рамках проекта на студкемпе от Яндекса, ФКН ВШЭ и Неймарка. Тема кемпа - Компьютерное зрение и автономный транспорт.

🔗 **[Репозиторий с готовым приложение]**(https://github.com/AsadchiyViacheslav/Yandex_GO_scooters)

---

## 📂 Структура репозитория

| Раздел | Описание |
|--------|----------|
| [data_split.ipynb](./data_split.ipynb) | Разделение данных для разметки |
| [load_data.ipynb](./load_data.ipynb) | Загрузка датасета в Yandex Cloud |
| [MobileNetV3_scooter_classification.ipynb](./MobileNetV3_scooter_classification.ipynb) | Обучение small и large MobileNetV3 для определения находится ли самокат на фото |
| [EfficientNetB1_scooter_classification.ipynb](./EfficientNetB1_scooter_classification.ipynb) | Обучение EfficientNetV2 B1 для определения находится ли самокат на фото |
| [model_convert.ipynb](./model_convert.ipynb) | Конвертация модели из .pth в .onnx |
| [model_check.ipynb](./model_check.ipynb) | Оценка модели в формате .onnx |
| [task.docx](./task.docx) | Описание и задача проекта |
| [data](./data/) | Папка с разметкой |


