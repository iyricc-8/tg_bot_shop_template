# 🗄️ ПОЛНАЯ SQL ДОКУМЕНТАЦИЯ

## 📋 ТАБЛИЦЫ И СТРУКТУРА

### 1️⃣ ТАБЛИЦА КАТЕГОРИЙ (categories)

```sql
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_uz VARCHAR(100) NOT NULL UNIQUE,      -- Название на узбекском
    description LONGTEXT NULL,                  -- Описание
    image_url VARCHAR(500) NULL,               -- URL изображения
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Пример:**
```sql
SELECT * FROM categories;
```

**Результат:**
```
id | name_uz              | description | image_url | created_at
1  | 📱 Смартфонлар      | Смартфоны   | NULL      | 2026-02-24...
2  | 💻 Компютерлар      | Компютеры   | NULL      | 2026-02-24...
5  | 🔌 Батериялар       | Батереи    | NULL      | 2026-02-24...
```

---

### 2️⃣ ТАБЛИЦА ТОВАРОВ (products)

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_uz VARCHAR(150) NOT NULL,              -- Название товара
    description_uz LONGTEXT NULL,               -- Описание
    price DECIMAL(12, 2) NOT NULL,             -- Цена
    image_url VARCHAR(500) NULL,               -- URL изображения
    category_id INT NOT NULL,                  -- ID категории
    stock INT DEFAULT 100,                     -- Количество в наличии
    is_active BOOLEAN DEFAULT TRUE,            -- Активен ли товар
    sales_count INT DEFAULT 0,                 -- Количество продаж
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

**Пример:**
```sql
SELECT * FROM products WHERE category_id = 1 LIMIT 3;
```

**Результат:**
```
id | name_uz          | price    | stock | sales_count | category_id
1  | iPhone 15 Pro    | 1200000  | 15    | 5           | 1
2  | Samsung Galaxy   | 900000   | 20    | 8           | 1
3  | Xiaomi 14 Ultra  | 600000   | 25    | 12          | 1
```

---

### 3️⃣ ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ (users)

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,        -- ID в Telegram
    first_name VARCHAR(100) NULL,              -- Имя
    last_name VARCHAR(100) NULL,               -- Фамилия
    phone_number VARCHAR(20) NULL,             -- Телефон
    address LONGTEXT NULL,                     -- Адрес
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Пример:**
```sql
SELECT * FROM users WHERE telegram_id = 123456789;
```

**Результат:**
```
id | telegram_id | first_name | last_name | phone_number | address
1  | 123456789   | Baxrom     | Qodirov   | +998901234567| Toshkent
```

---

### 4️⃣ ТАБЛИЦА КОРЗИН (carts)

```sql
CREATE TABLE carts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                      -- ID пользователя
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Пример:**
```sql
SELECT * FROM carts WHERE user_id = 1;
```

---

### 5️⃣ ТАБЛИЦА ТОВАРОВ В КОРЗИНЕ (cart_items)

```sql
CREATE TABLE cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,                      -- ID корзины
    product_id INT NOT NULL,                   -- ID товара
    quantity INT DEFAULT 1,                    -- Количество
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Пример:**
```sql
SELECT ci.id, p.name_uz, ci.quantity, p.price, (p.price * ci.quantity) as total
FROM cart_items ci
JOIN products p ON ci.product_id = p.id
WHERE ci.cart_id = 1;
```

---

### 6️⃣ ТАБЛИЦА ЗАКАЗОВ (orders)

```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,                      -- ID пользователя
    status VARCHAR(50) DEFAULT 'yangi',        -- Статус заказа
    item_count INT DEFAULT 0,                  -- Количество товаров
    total_price DECIMAL(12, 2) DEFAULT 0.00,  -- Общая сумма
    delivery_address LONGTEXT NULL,            -- Адрес доставки
    notes LONGTEXT NULL,                       -- Примечания
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Статусы заказа:**
- `yangi` - Новый заказ
- `tasdiqlandi` - Подтвержден
- `yuborildi` - Отправлен
- `yetkazildi` - Доставлен
- `bekor qilingan` - Отменен

**Пример:**
```sql
SELECT * FROM orders WHERE user_id = 1 ORDER BY created_at DESC;
```

---

### 7️⃣ ТАБЛИЦА ТОВАРОВ В ЗАКАЗЕ (order_items)

```sql
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,                     -- ID заказа
    product_id INT NOT NULL,                   -- ID товара
    quantity INT NOT NULL,                     -- Количество
    price_at_purchase DECIMAL(12, 2) NOT NULL,-- Цена при покупке
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Пример:**
```sql
SELECT oi.id, p.name_uz, oi.quantity, oi.price_at_purchase, 
       (oi.price_at_purchase * oi.quantity) as total
FROM order_items oi
JOIN products p ON oi.product_id = p.id
WHERE oi.order_id = 1;
```

---

## 🔍 ПОЛЕЗНЫЕ SQL ЗАПРОСЫ

### 1. Показать все категории

```sql
SELECT * FROM categories;
```

### 2. Показать товары в категории

```sql
SELECT * FROM products WHERE category_id = 1;
```

### 3. Показать самые популярные товары

```sql
SELECT * FROM products ORDER BY sales_count DESC LIMIT 10;
```

### 4. Посчитать товары по категориям

```sql
SELECT c.name_uz, COUNT(p.id) as product_count
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.name_uz;
```

### 5. Показать все заказы пользователя

```sql
SELECT * FROM orders WHERE user_id = 1 ORDER BY created_at DESC;
```

### 6. Показать деталь заказа

```sql
SELECT o.id, o.total_price, o.status, o.created_at,
       u.first_name, u.last_name, u.phone_number
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.id = 1;
```

### 7. Показать товары в заказе

```sql
SELECT oi.id, p.name_uz, oi.quantity, oi.price_at_purchase,
       (oi.price_at_purchase * oi.quantity) as total
FROM order_items oi
JOIN products p ON oi.product_id = p.id
WHERE oi.order_id = 1;
```

### 8. Посчитать выручку по дням

```sql
SELECT DATE(created_at) as day, COUNT(*) as orders, SUM(total_price) as revenue
FROM orders
WHERE status IN ('tasdiqlandi', 'yuborildi', 'yetkazildi')
GROUP BY DATE(created_at)
ORDER BY day DESC;
```

### 9. Обновить статус заказа

```sql
UPDATE orders SET status = 'yuborildi' WHERE id = 1;
```

### 10. Добавить товар в наличие

```sql
UPDATE products SET stock = stock + 50 WHERE id = 1;
```

### 11. Увеличить счетчик продаж

```sql
UPDATE products SET sales_count = sales_count + 1 WHERE id = 1;
```

### 12. Удалить товар

```sql
DELETE FROM products WHERE id = 1;
```

### 13. Показать статистику продаж по товарам

```sql
SELECT name_uz, price, sales_count, (price * sales_count) as total_revenue
FROM products
ORDER BY sales_count DESC
LIMIT 20;
```

### 14. Показать активных пользователей

```sql
SELECT u.id, u.first_name, u.last_name, u.phone_number,
       COUNT(o.id) as order_count, SUM(o.total_price) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
ORDER BY total_spent DESC;
```

### 15. Показать товары с низким остатком

```sql
SELECT id, name_uz, price, stock
FROM products
WHERE stock < 10 AND is_active = TRUE
ORDER BY stock ASC;
```

---

## ➕ ДОБАВЛЕНИЕ ДАННЫХ

### Добавить новую категорию

```sql
INSERT INTO categories (name_uz, description)
VALUES ('🖥️ Мониторлар', 'Компютер мониторлари');
```

### Добавить новый товар

```sql
INSERT INTO products (name_uz, description_uz, price, category_id, stock)
VALUES ('LG Monitor 24"', 'Чоролик 24 дюймли монитор', 450000, 6, 20);
```

### Добавить нового пользователя

```sql
INSERT INTO users (telegram_id, first_name, last_name, phone_number, address)
VALUES (987654321, 'Ali', 'Aliyev', '+998901234567', 'Toshkent, Mirzo Ulugbek');
```

---

## 🔗 СЛОЖНЫЕ ЗАПРОСЫ

### Полная информация о заказе с товарами

```sql
SELECT 
    o.id as order_id,
    o.status,
    o.total_price,
    o.created_at,
    u.first_name,
    u.last_name,
    u.phone_number,
    o.delivery_address,
    p.name_uz,
    oi.quantity,
    oi.price_at_purchase
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.id = 1
ORDER BY oi.id;
```

### Средний чек

```sql
SELECT 
    ROUND(AVG(total_price), 2) as avg_order,
    MIN(total_price) as min_order,
    MAX(total_price) as max_order,
    COUNT(*) as total_orders
FROM orders;
```

### Товары которые никогда не продавались

```sql
SELECT id, name_uz, price, stock
FROM products
WHERE sales_count = 0
ORDER BY created_at DESC;
```

---

## 📊 ИНДЕКСЫ

Индексы уже созданы для оптимизации:

```sql
-- Четыре основные индексы:
INDEX idx_name (name_uz)          -- Поиск по имени
INDEX idx_category (category_id)  -- Фильтр по категории
INDEX idx_price (price)           -- Сортировка по цене
INDEX idx_sales (sales_count)     -- Сортировка по продажам
```

---

## 🔐 БЕЗОПАСНОСТЬ

### Создать пользователя только для чтения

```sql
CREATE USER 'shop_readonly'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT ON shop_db.* TO 'shop_readonly'@'localhost';
```

### Создать пользователя для приложения

```sql
CREATE USER 'shop_app'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON shop_db.* TO 'shop_app'@'localhost';
FLUSH PRIVILEGES;
```

---

## 📈 РЕЗЕРВНЫЕ КОПИИ

### Создать backup

```bash
mysqldump -u root -p shop_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Восстановить backup

```bash
mysql -u root -p shop_db < backup_20260224_143000.sql
```

---

**Все SQL запросы готовы к использованию!** ✅
