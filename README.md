# Sport & Nutrition Assistant
ИИ-агент, который помогает с вопросами о питании и тренировках.

# Описание
Агент принимает запросы от пользователя, определяет их категорию (питание, спорт или общий вопрос), при необходимости обращается к внешним API для получения актуальных данных и формирует ответ с помощью GigaChat. Состояние диалога сохраняется между вызовами.

# Реализованные требования
- GigaChat: модель `GigaChat-3-Pro` (API Cloud.ru).
- LangGraph: граф из 4 узлов (router, food, sport, response).
- 2 внешних API:
  - `Open Food Facts` (калории и БЖУ продуктов).
  - `wger` (база упражнений).
- Память: сохранение истории диалога через `InMemorySaver` и `thread_id`.
- Роутинг: 3 динамических пути (`food`, `sport`, `general`).
- FastAPI: эндпоинты `POST /chat` и `GET /history/{thread_id}`.

# Запуск
1. `pip install -r requirements.txt`
2. Добавить ключ в `.env`: `GIGACHAT_KEY=ваш_ключ`
3. Запустить сервер: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. Перейти в Swagger UI: `http://localhost:8000/docs`

# Пример запроса
**POST** `/chat`
```json
{"message": "Сколько калорий в банане?", "thread_id": "user-1"}

В папке demo/demo.ipynb находится ноутбук с наглядной демонстрацией работы графа