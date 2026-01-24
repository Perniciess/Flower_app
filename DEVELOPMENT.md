docker compose --env-file .env -f docker/docker-compose.yaml up -d

fastapi dev app/main.py

alembic revision --autogenerate -m "your message"
alembic upgrade head



## Регистрация с верификацией номера через Telegram

### Со стороны пользователя

**Шаг 1: Регистрация на сайте**
1. Пользователь заполняет форму: номер телефона, имя, пароль
2. Нажимает "Зарегистрироваться"

**Шаг 2: Переход в Telegram**
3. Сайт показывает кнопку "Подтвердить номер в Telegram" (ссылка действует 5 минут)
4. Пользователь нажимает кнопку → открывается бот

**Шаг 3: Подтверждение номера в боте**
5. Бот просит нажать кнопку "Отправить номер телефона"
6. Пользователь нажимает → Telegram отправляет верифицированный номер
7. Бот сравнивает номер с сайта и номер из Telegram
8. Если совпадают → "Номер подтверждён! Вернитесь на сайт"

**Шаг 4: Завершение на сайте**
9. Сайт автоматически определяет успешную верификацию
10. Пользователь авторизован и перенаправлен в личный кабинет

---

### Техническая реализация

#### Шаг 1: POST /auth/register

```
Frontend → Backend:
POST /auth/register
{
    "phone_number": "+79991234567",
    "name": "Иван",
    "password": "SecurePass123!"
}
```

Backend (FastAPI):
1. Валидирует данные
2. Проверяет, не занят ли номер в БД
3. Генерирует код верификации
4. Сохраняет в Redis:
```
Key: "verification:{code}"
Value: {
    "phone_number": "+79991234567",
    "name": "Иван",
    "password_hash": "...",
    "telegram_chat_id": null
}
TTL: 300 сек
```
5. Возвращает:
```json
{
    "verification_code": "ABC123XYZ456",
    "telegram_link": "https://t.me/flowershop_bot?start=ABC123XYZ456",
    "expires_in": 300
}
```

---

#### Шаг 2: Frontend начинает polling

```
GET /auth/check-verification/{code}
```

Ответ (пока не подтверждено):
```json
{
    "status": "pending",
    "expires_in": 287
}
```

---

#### Шаг 3: Пользователь переходит в бот

Telegram отправляет боту: `/start ABC123XYZ456`

---

#### Шаг 4: Бот запрашивает номер телефона

Telegram Bot (aiogram):
1. Извлекает код из команды `/start`
2. Проверяет код в Redis
3. Если код валиден → показывает кнопку "Отправить номер телефона"
4. Если код не найден → "Код недействителен или истёк"

```python
kb_phone = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отправить номер", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
```

---

#### Шаг 5: Бот получает контакт и верифицирует

Telegram Bot:
1. Получает контакт от пользователя (верифицированный Telegram номер)
2. Проверяет `contact.user_id == message.from_user.id` (защита от чужих номеров)
3. Сравнивает `contact.phone_number` с `phone_number` из Redis
4. Если совпадают:
   - Вызывает FastAPI: `POST /auth/complete-registration`
   - Отправляет: "Номер подтверждён! Вернитесь на сайт"
5. Если не совпадают:
   - "Номер не совпадает с указанным при регистрации"

---

#### Шаг 6: POST /auth/complete-registration

```
Bot → Backend:
POST /auth/complete-registration
{
    "verification_code": "ABC123XYZ456",
    "telegram_phone": "+79991234567",
    "telegram_chat_id": 123456789
}
```

Backend (FastAPI):
1. Получает данные из Redis
2. Сравнивает номера (дополнительная проверка)
3. Создаёт пользователя в PostgreSQL
4. Удаляет код из Redis
5. Возвращает:
```json
{
    "status": "success",
    "user_id": 123
}
```

---

#### Шаг 7: Frontend получает подтверждение

```
GET /auth/check-verification/{code}
```

Ответ:
```json
{
    "status": "verified",
    "user_id": 123
}
```

Frontend:
- Запрашивает токены: `POST /auth/login`
- Перенаправляет в личный кабинет

---

### Дополнительные сценарии

**Код истёк (5 минут):**
- Redis автоматически удаляет запись
- Бот: "Код недействителен. Повторите регистрацию"
- Frontend: "Время истекло. Попробуйте снова"

**Номера не совпадают:**
- Бот: "Номер +7XXX не совпадает с указанным при регистрации (+7YYY)"
- Пользователь должен зарегистрироваться с правильным номером

**Номер уже занят:**
- Backend возвращает ошибку на этапе /auth/register
- Код верификации не создаётся
