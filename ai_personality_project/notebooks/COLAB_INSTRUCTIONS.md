# Инструкция по тестированию в Google Colab

## Способ 1: Загрузка .ipynb файла (РЕКОМЕНДУЕТСЯ)

1. **Откройте Google Colab**: https://colab.research.google.com/

2. **Загрузите ноутбук**:
   - Нажмите "Файл" → "Загрузить блокнот"
   - Выберите файл `notebooks/phase1_testing.ipynb`
   - Или перетащите файл в окно Colab

3. **Выполните ячейки по порядку**:
   - Нажимайте ▶️ на каждой ячейке
   - Или "Среда выполнения" → "Выполнить все"

## Способ 2: Использование Python скрипта

1. **Создайте новый ноутбук** в Colab

2. **Загрузите файлы проекта**:
   ```python
   # В первой ячейке выполните:
   !git clone https://github.com/your-username/ai-personality-project.git
   %cd ai-personality-project
