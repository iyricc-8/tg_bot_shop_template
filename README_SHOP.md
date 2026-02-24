# 🛍️ Telegram Дюкан Бота - Уз Лотин

Полноценный онлайн-магазин для Telegram с поддержкой узбекского языка.

## 📋 Функции

- ✅ Каталог товаров с категориями
- ✅ Система корзины
- ✅ Оформление заказов
- ✅ Ввод данных покупателя (имя, фамилия, телефон, адрес)
- ✅ Топ продаж
- ✅ История заказов
- ✅ Автоматическое создание чеков/счетов
- ✅ Управление профилем
- ✅ Отслеживание остатков товаров
- ✅ Расчет продаж

## 🚀 Начало работы

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Инициализация БД с примерами

```bash
python init_shop_db.py
```

Этот скрипт создаст:
- 5 категорий товаров
- 15+ примеров товаров на узбекском языке
- Все необходимые таблицы в БД

### 3. Запуск бота

```bash
python main.py
```

## 📁 Структура проекта

```
.
├── main.py                    # Главный файл
├── requirements.txt           # Зависимости
├── init_shop_db.py            # Инициализация БД
├── bot_shop.db                # База данных (создается автоматически)
├── config/
│   └── config.py              # Конфигурация
├── db/
│   ├── models.py              # Модели БД (SQLAlchemy)
│   ├── database.py            # Подключение к БД
│   └── repositories.py        # Операции с БД
├── handlers/
│   └── shop.py                # Основной роутер магазина
├── keyboards/
│   └── shop.py                # Инлайн и обычные клавиатуры
├── services/
│   └── invoice_generator.py   # Генератор чеков
└── states/
    └── shop_states.py         # FSM состояния
```

## 🎮 Использование

### Нормальный пользователь

1. Нажать `/start` - получить главное меню
2. 🛍️ **Магазин** - просмотр категорий и товаров
3. 🔥 **Топ продажи** - самые популярные товары
4. 🛒 **Корзина** - просмотр добавленных товаров
5. 📦 **Мои заказы** - история заказов
6. 👤 **Аккаунт** - данные профиля

### Процесс заказа

1. Выбрать товары и добавить в корзину
2. Перейти в корзину
3. Нажать "Оформить"
4. Ввести данные:
   - Имя
   - Фамилия
   - Номер телефона
   - Адрес доставки
5. Подтвердить заказ
6. Получить чек

## 🗄️ База данных

### Таблицы

- **categories** - категории товаров
- **products** - товары с ценой и остатком
- **users** - пользователи Telegram
- **carts** - корзины пользователей
- **cart_items** - товары в корзине
- **orders** - заказы
- **order_items** - товары в заказах

### Модели

Все модели определены в `db/models.py` на SQLAlchemy.

## 🔧 API Repositories

### CategoryRepository

```python
await CategoryRepository.get_all(session)
await CategoryRepository.get_by_id(session, id)
await CategoryRepository.create(session, name_uz, description, image_url)
```

### ProductRepository

```python
await ProductRepository.get_all(session)
await ProductRepository.get_by_id(session, id)
await ProductRepository.get_by_category(session, category_id)
await ProductRepository.get_top_sales(session, limit=10)
await ProductRepository.create(session, name_uz, price, category_id, ...)
await ProductRepository.update_stock(session, product_id, quantity)
await ProductRepository.increase_sales(session, product_id, quantity)
```

### CartRepository

```python
await CartRepository.get_or_create(session, user_id)
await CartRepository.add_item(session, user_id, product_id, quantity)
await CartRepository.remove_item(session, cart_item_id)
await CartRepository.clear(session, user_id)
```

### OrderRepository

```python
await OrderRepository.create(session, user_id, delivery_address, notes)
await OrderRepository.get_by_id(session, order_id)
await OrderRepository.get_user_orders(session, user_id)
await OrderRepository.add_item(session, order_id, product_id, quantity, price)
await OrderRepository.update_status(session, order_id, status)
```

## 📝 Модификация товаров

Вы можете добавить новые товары прямо в код:

```python
async with AsyncSessionLocal() as session:
    product = await ProductRepository.create(
        session,
        name_uz="Мой товар",
        price=100000,
        category_id=1,
        description_uz="Описание на узбекском",
        stock=50
    )
```

## 🌐 Интеграция с внешней БД

Для использования PostgreSQL или другой БД, измените `DATABASE_URL` в `db/database.py`:

```python
# PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/shop_db"

# MySQL
DATABASE_URL = "mysql+aiomysql://user:password@localhost/shop_db"
```

## 🛠️ Статусы заказов

- `yangi` - Новый заказ
- `tasdiqlandi` - Подтвержден
- `yuborildi` - Отправлен
- `yetkazildi` - Доставлен
- `bekor qilingan` - Отменен

## 💡 Советы

1. **Добавить изображения товаров** - укажите `image_url` при создании товара
2. **Кастомизировать язык** - измените текст в `keyboards/shop.py` и `handlers/shop.py`
3. **Расширить функционал** - добавьте новые методы в `repositories.py`
4. **Администраторское панель** - создайте отдельный роутер для админов

## 📞 Поддержка

Этот бот готов к продакшену. Все данные безопасно хранятся в SQLite БД.

## 📄 Лицензия

Свободный код. Используйте как угодно!

---

**Создано на:** aiogram 3.7+
**язык:** Узбекский (O'zbek Lotin)
**БД:** SQLite + SQLAlchemy
