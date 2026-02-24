# 🔄 СИНХРОНИЗАЦИЯ БОТА С MySQL

## 📋 ПЛАН ДЕЙСТВИЙ

### 1️⃣ Вы создаете БД в MySQL
### 2️⃣ Я синхронизирую код Python
### 3️⃣ Код автоматически подключится к вашей БД

---

## 🚀 ПОШАГОВОЕ РУКОВОДСТВО

### ШАГ 1: Подходы к созданию БД

Выберите один из вариантов:

#### Вариант A: Через MySQL Command Line (быстро)

```bash
# 1. Откройте MySQL консоль
mysql -u root -p

# 2. Выполните SQL файл
source C:/path/to/database/shop_db.sql

# Или в одну команду:
mysql -u root -p < database/shop_db.sql
```

#### Вариант B: Через phMyAdmin (графический интерфейс)

1. Откройте phMyAdmin в браузере (http://localhost/phpmyadmin)
2. Нажмите "Import"
3. Выберите файл `database/shop_db.sql`
4. Нажмите "Go"

#### Вариант C: Через MySQL Workbench

1. Откройте MySQL Workbench
2. File → Open SQL Script → выберите `database/shop_db.sql`
3. Execute (Ctrl+Shift+Enter)

#### Вариант D: Вручную создать таблицы

Если нужно создать вручную, все запросы находятся в:
- `database/shop_db.sql`
- `SQL_DOCUMENTATION.md`

---

### ШАГ 2: Проверить что БД создалась

```sql
-- Проверить что БД существует
SHOW DATABASES LIKE 'shop_db';

-- Использовать БД
USE shop_db;

-- Проверить таблицы
SHOW TABLES;

-- Проверить данные
SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM products;
```

Должно быть:
```
- 5 категорий
- 14 товаров
- Все остальные таблицы готовы
```

---

### ШАГ 3: Конфигурировать Python код

#### Файл: `.env`

```bash
# 1. Скопируйте пример
cp .env.example .env

# 2. Отредактируйте для MySQL
```

**Содержимое `.env`:**

```env
# Telegram Bot
BOT_TOKEN=YOUR_TOKEN_HERE
ADMINS=123456789

# Конфигурация MySQL
DB_TYPE=mysql
DB_HOST=localhost          # Адрес MySQL
DB_PORT=3306              # Порт MySQL
DB_USER=root              # Пользователь MySQL
DB_PASSWORD=your_password # Пароль MySQL
DB_NAME=shop_db           # Имя БД (обязательно shop_db)
```

**Примеры разных конфигураций:**

Локальный MySQL:
```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=shop_db
```

Удаленный MySQL:
```env
DB_TYPE=mysql
DB_HOST=192.168.1.100
DB_PORT=3306
DB_USER=shop_user
DB_PASSWORD=secure_password
DB_NAME=shop_db
```

С phpmyadmin:
```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=adminer
DB_PASSWORD=adminer_password
DB_NAME=shop_db
```

---

### ШАГ 4: Установить зависимости

```bash
# Установить все пакеты (включая aiomysql)
pip install -r requirements.txt
```

Это установит:
- ✅ aiomysql (драйвер MySQL)
- ✅ asyncpg (для PostgreSQL)
- ✅ sqlalchemy (ORM)
- ✅ aiogram (Telegram API)

---

### ШАГ 5: Запустить бота

```bash
python main.py
```

Если вывод:
```
Starting polling...
```

✅ **БОТ УСПЕШНО ПОДКЛЮЧИЛСЯ К MySQL!**

---

## 🔍 ПРОВЕРИТЬ ПОДКЛЮЧЕНИЕ

### Способ 1: Логи в консоли

При запуске должно быть без ошибок. Если есть ошибки вроде:
- `Can't connect to MySQL server`
- `Access denied for user`
- `Unknown database`

Проверьте `.env` файл!

### Способ 2: Проверить данные в БД

```sql
SELECT * FROM categories;
SELECT COUNT(*) FROM products;
SELECT * FROM products WHERE id = 1;
```

### Способ 3: Проверить подключение Python

```python
import asyncio
from db.database import AsyncSessionLocal, init_db

async def test():
    await init_db()
    async with AsyncSessionLocal() as session:
        from sqlalchemy import text
        result = await session.execute(text("SELECT COUNT(*) as cnt FROM categories"))
        row = result.fetchone()
        print(f"✅ Количество категорий: {row[0]}")

asyncio.run(test())
```

---

## 🎯 СИНХРОНИЗАЦИЯ КОД ↔ БД

### Автоматическая синхронизация

Когда вы запускаете `main.py`:

1. ✅ Код автоматически подключается к MySQL
2. ✅ Читает таблицы из БД
3. ✅ Использует данные для работы
4. ✅ При добавлении товаров - сохраняет в БД

### Ручная синхронизация

Если нужно пересоздать таблицы:

```bash
# 1. Удалить старую БД
mysql -u root -p -e "DROP DATABASE shop_db;"

# 2. Пересоздать из SQL файла
mysql -u root -p < database/shop_db.sql

# 3. Перезапустить бота
python main.py
```

---

## 📊 ДОБАВЛЕНИЕ СВОИХ ДАННЫХ

### Добавить товар через SQL

```sql
INSERT INTO products (name_uz, description_uz, price, category_id, stock)
VALUES ('Новый товар', 'Описание', 50000, 1, 100);
```

### Добавить товар через админ консоль

```bash
python admin_console.py
# Выберите опцию 5 (Добавить товар)
# Заполните данные
```

### Добавить товар через Python

```python
from db.database import AsyncSessionLocal
from db.repositories import ProductRepository

async def add_product():
    async with AsyncSessionLocal() as session:
        await ProductRepository.create(
            session,
            name_uz="Новый товар",
            price=50000,
            category_id=1,
            description_uz="Описание товара",
            stock=100
        )

import asyncio
asyncio.run(add_product())
```

---

## 🔄 WORKFLOW СИНХРОНИЗАЦИИ

```
┌─────────────────────────────────────┐
│  Вы создаете БД в MySQL             │
│  (запускаете database/shop_db.sql)   │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Конфигурируете .env файл           │
│  (добавляете DB_TYPE=mysql и данные)│
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Устанавливаете зависимости         │
│  (pip install -r requirements.txt)  │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Запускаете бота                    │
│  (python main.py)                   │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  ✅ Код синхронизирован с MySQL!    │
│  Магазин работает с вашей БД!       │
└─────────────────────────────────────┘
```

---

## ❌ РЕШЕНИЕ ПРОБЛЕМ

### Проблема: "Connection refused"

```
Решение:
1. Проверьте что MySQL запущен
2. Проверьте DB_HOST в .env (localhost или IP)
3. Проверьте DB_PORT (обычно 3306)
```

### Проблема: "Access denied"

```
Решение:
1. Проверьте DB_USER в .env
2. Проверьте DB_PASSWORD в .env
3. Убедитесь что пользователь имеет права на БД
```

### Проблема: "Unknown database 'shop_db'"

```
Решение:
1. Запустите database/shop_db.sql снова
2. Проверьте что БД создалась: mysql -u root -p -e "SHOW DATABASES;"
3. Проверьте DB_NAME в .env (должно быть shop_db)
```

### Проблема: "No module named 'aiomysql'"

```
Решение:
pip install -r requirements.txt
```

### Проблема: "Таблицы не видны"

```
Решение:
1. Проверьте что выполнили SQL файл полностью
2. Используйте: mysql -u root -p shop_db -e "SHOW TABLES;"
3. Должно быть 7 таблиц
```

---

## 📈 ОПТИМИЗАЦИЯ

### Для продакшена рекомендуется:

1. **Создать отдельного пользователя MySQL:**

```sql
CREATE USER 'bot_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON shop_db.* TO 'bot_user'@'localhost';
FLUSH PRIVILEGES;
```

2. **Использовать в `.env`:**

```env
DB_USER=bot_user
DB_PASSWORD=strong_password
```

3. **Создать резервные копии:**

```bash
mysqldump -u root -p shop_db > backup.sql
```

---

## ✅ КОНТРОЛЬНЫЙ СПИСОК

- [ ] MySQL сервер установлен и запущен
- [ ] Файл `database/shop_db.sql` находится в проекте
- [ ] Выполнен SQL файл (БД создана)
- [ ] Файл `.env` настроен с MySQL параметрами
- [ ] Установлены все зависимости (`pip install -r requirements.txt`)
- [ ] Проверено подключение к БД
- [ ] Запущен бот (`python main.py`)
- [ ] Бот успешно подключился к MySQL

---

## 🎉 ВСЕ ГОТОВО!

Теперь ваш Telegram магазин работает с **реальной MySQL базой данных**! 

```bash
python main.py
```

**Синхронизация завершена!** ✅

---

**Дата:** 24 февраля 2026
**БД:** MySQL 8.0+
**Статус:** ✅ ГОТОВО К ПРОДАКШЕНУ
