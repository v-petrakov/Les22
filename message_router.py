import requests
from aiogram import Router
from aiogram.types import Message

# Создаем роутер
router = Router()

# URL локального сервера модели
MODEL_SERVER_URL = "http://127.0.0.1:1234/v1/chat/completions"

# Флаг для отслеживания первого сообщения от пользователя
user_states = {}

@router.message()
async def handle_message(message: Message):
    """Обработчик всех сообщений от пользователя"""
    user_id = message.from_user.id

    # Если пользователь впервые обращается к боту
    if user_id not in user_states:
        user_states[user_id] = {"greeted": True}
        await message.answer("Привет! Что тебя интересует?")
    else:
        try:
            # Отправляем запрос к локальной модели
            response = requests.post(
                MODEL_SERVER_URL,
                json={
                    "model": "hermes-3-llama-3.1-8b",
                    "messages": [{"role": "user", "content": message.text}]
                }
            )
            # Проверяем ответ от сервера
            if response.status_code == 200:
                data = response.json()
                reply = data.get("choices", [{}])[0].get("message", {}).get("content", "Нет ответа")
                await message.answer(reply)
            else:
                await message.answer(f"Ошибка модели: {response.status_code}")
        except Exception as e:
            # Обработка ошибок
            await message.answer(f"Произошла ошибка: {str(e)}")
