# 🗄️ ИНСТРУКЦИИ ПО ИСПОЛЬЗОВАНИЮ MySQL

## 📋 Что вам нужно

- ✅ MySQL сервер (локальный или удаленный)
- ✅ Доступ к MySQL (пользователь и пароль)
- ✅ SQL файл `database/shop_db.sql`

---

## 🚀 ПОШАГОВОЕ ПОДКЛЮЧЕНИЕ

### ШАГ 1: Подготовить SQL файл

SQL запросы находятся в файле: `database/shop_db.sql`

Этот файл содержит:
- ✅ CREATE DATABASE shop_db
- ✅ CREATE TABLE для всех таблиц
- ✅ INSERT примеры данных

### ШАГ 2: Создать БД через MySQL

#### Способ 1: Через MySQL Client

```bash
# Подключиться к MySQL
mysql -u root -p

# Выполнить SQL файл
source /path/to/database/shop_db.sql

# Или импортировать:
mysql -u root -p < database/shop_db.sql
```

#### Способ 2: Через phMyAdmin (если установлен)

1. Откройте phMyAdmin
2. Выберите "Import"
3. Загрузите файл `database/shop_db.sql`
4. Нажмите "Go"

#### Способ 3: Через MySQL Workbench

1. Откройте MySQL Workbench
2. File → Open SQL Script
3. Выберите `database/shop_db.sql`
4. Нажмите Execute

### ШАГ 3: Обновить .env файл

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
DB_TYPE=mysql
DB_HOST=localhost      # Адрес сервера MySQL
DB_PORT=3306           # Порт (обычно 3306)
DB_USER=root           # Пользователь MySQL
DB_PASSWORD=password   # Пароль MySQL
DB_NAME=shop_db        # Имя БД (как в SQL файле)
```

### ШАГ 4: Установить Python пакеты

```bash
pip install -r requirements.txt
```

Это установит:
- ✅ aiomysql - драйвер для MySQL
- ✅ asyncpg - для PostgreSQL (если понадобится)

### ШАГ 5: Запустить бота

```bash
python main.py
```

---

## 🔧 ПРОВЕРКА ПОДКЛЮЧЕНИЯ

### Проверить что MySQL запущен

```bash
# Windows
netstat -an | find "3306"

# Linux/Mac
lsof -i :3306
```

### Проверить подключение с MySQL Client

```bash
mysql -h localhost -u root -p -D shop_db
```

Если успешно подключилось, выполните:

```sql
SHOW TABLES;
SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM products;
```

---

## 🌐 ПОДКЛЮЧЕНИЕ К УДАЛЕННОЙ MySQL

Если MySQL на другом сервере:

```env
DB_TYPE=mysql
DB_HOST=123.45.67.89      # IP сервера
DB_PORT=3306               # Порт MySQL
DB_USER=shop_user          # Пользователь
DB_PASSWORD=secure_pass    # Пароль
DB_NAME=shop_db            # Имя БД
```

---

## 📊 СОДЕРЖИМОЕ SQL ФАЙЛА

### Таблицы которые создаются:

1. **categories** (5 записей)
   - ID категории
   - Название на узбекском
   - Описание
   - Изображение URL
   - Дата создания

2. **products** (15 записей)
   - Товары с ценой
   - Остаток товара
   - Категория
   - Количество продаж
   - Описание

3. **users**
   - Пользователи Telegram
   - Имя, фамилия, телефон, адрес

4. **carts** и **cart_items**
   - Корзины пользователей
   - Товары в корзине

5. **orders** и **order_items**
   - Заказы
   - Товары в заказах

### Примеры данных:

- 📱 Смартфоны (3 товара)
- 💻 Компьютеры (2 товара)
- ⌚ Аксессуары (3 товара)
- 🎧 Наушники (3 товара)
- 🔌 Батереи (3 товара)

---

## ⚙️ ПЕРЕКЛЮЧЕНИЕ МЕЖДУ БД

### Использовать SQLite (по умолчанию)

```env
DB_TYPE=sqlite
```

### Использовать MySQL

```env
DB_TYPE=mysql
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=shop_db
```

### Использовать PostgreSQL

```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=shop_db
```

---

## 🔒 БЕЗОПАСНОСТЬ

### Защита паролей

**НИКОГДА** не коммитьте `.env` файл!

Добавьте в `.gitignore`:

```
.env
.env.local
.DS_Store
__pycache__
*.pyc
bot_shop.db
```

### Защита MySQL

```sql
-- Создать пользователя для приложения
CREATE USER 'shop_user'@'localhost' IDENTIFIED BY 'strong_password';

-- Дать права
GRANT ALL PRIVILEGES ON shop_db.* TO 'shop_user'@'localhost';

-- Применить
FLUSH PRIVILEGES;
```

---

## ❓ РЕШЕНИЕ ПРОБЛЕМ

### Ошибка: "Connection refused"

```
Решение: Убедитесь что MySQL запущен
- Windows: Start > Services > MySQL
- Linux: sudo systemctl start mysql
```

### Ошибка: "Access denied for user"

```
Решение: Проверьте пароль в .env
- Пароль не должен быть пустым
- Проверьте правильность пользователя
```

### Ошибка: "Unknown database 'shop_db'"

```
Решение: Запустите SQL файл
mysql -u root -p < database/shop_db.sql
```

### Ошибка: "No module named 'aiomysql'"

```
Решение: Установите пакеты
pip install -r requirements.txt
```

---

## 📈 МИГРАЦИЯ ДАННЫХ

### Из SQLite в MySQL

```bash
# 1. Экспортировать из SQLite
sqlite3 bot_shop.db .dump > backup.sql

# 2. Преобразовать для MySQL
# (отредактируйте синтаксис)

# 3. Импортировать в MySQL
mysql -u root -p shop_db < backup.sql
```

### Резервная копия MySQL

```bash
# Создать backup
mysqldump -u root -p shop_db > backup.sql

# Восстановить
mysql -u root -p shop_db < backup.sql
```

---

## 🎯 СОВЕТЫ И ТРЮКИ

### 1. Проверить версию MySQL

```sql
SELECT VERSION();
```

### 2. Показать все БД

```sql
SHOW DATABASES;
```

### 3. Показать все таблицы

```sql
USE shop_db;
SHOW TABLES;
```

### 4. Проверить структуру таблицы

```sql
DESCRIBE products;
```

### 5. Посчитать все товары

```sql
SELECT COUNT(*) as total_products FROM products;
```

### 6. Отключить safe mode

```sql
SET SQL_SAFE_UPDATES=0;
```

---

## 📞 ПОДДЕРЖКА

Если есть проблемы:

1. Проверьте что MySQL запущен
2. Проверьте файл `.env`
3. Проверьте что SQL файл выполнен
4. Проверьте логи в консоли

---

## ✅ ВСЕ ГОТОВО!

Теперь ваш магазин работает с MySQL! 🎉

```bash
python main.py
```

---

**Создано:** 24 февраля 2026
**БД:** MySQL 8.0+
**Поддержка:** SQLite, MySQL, PostgreSQL
