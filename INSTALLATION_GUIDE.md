# 🛍️ Telegram Bot Online Magazin - Qo'llanma

## 📋 Mundarija
1. [O'rnatish](#o%CC%BBrnatish)
2. [Baza Konfiguratsiyasi](#baza-konfiguratsiyasi)
3. [SQL Jadvallari](#sql-jadvallari)
4. [API da'volar](#api-davolar)
5. [Foydalanish](#foydalanish)
6. [Masalalarni Hal Qilish](#masalolarni-hal-qilish)

---

## 🚀 O'rnatish

### 1. Requirements o'rnatish
```bash
pip install -r requirements.txt
```

### 2. .env faylini sozlash
```env
# BOT SOZLAMALARI
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ADMINS=12345678,98765432

# DATABASE SOZLAMALARI
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=shop_db

TIMEZONE=Asia/Tashkent
```

---

## 🗄️ Baza Konfiguratsiyasi

### MySQL Bazasini Yaratish

```sql
-- MySQL bazasini ochish
mysql -u root -p

-- Bazani yaratish
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Foydalanuvchini yaratish (ixtiyoriy)
CREATE USER 'shop_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON shop_db.* TO 'shop_user'@'localhost';
FLUSH PRIVILEGES;

-- Bazaga kiritish
USE shop_db;

-- database/shop_db_mysql.sql faylidan SQL jadvallari yuklashtirish
SOURCE path/to/shop_db_mysql.sql;
```

### Baza Struktura

```
┌─────────────────────────────────────────┐
│           MAGASIN DATABASE              │
├─────────────────────────────────────────┤
│ • categories (Kategoriyalar)            │
│ • products (Mahsulotlar)                │
│ • users (Foydalanuvchilar)              │
│ • carts (Savat)                         │
│ • cart_items (Savat predmatlari)        │
│ • orders (Buyurtmalar)                  │
│ • order_items (Buyurtma predmatlari)    │
│ • reviews (Sharhlar)                    │
│ • payments (To'lovlar)                  │
└─────────────────────────────────────────┘
```

---

## 📊 SQL Jadvallari

### 1. KATEGORIYALAR
```sql
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name_uz VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. MAHSULOTLAR
```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name_uz VARCHAR(150) NOT NULL,
    description_uz TEXT,
    price FLOAT NOT NULL,
    image_url VARCHAR(500),
    category_id INT NOT NULL,
    stock INT DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    sales_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### 3. FOYDALANUVCHILAR
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    telegram_id BIGINT UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 4. SAVAT
```sql
CREATE TABLE carts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE cart_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_cart_product (cart_id, product_id)
);
```

### 5. BUYURTMALAR
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'yangi',
    -- Statuslar: yangi, tasdiqlandi, yuborildi, yetkazildi, bekor_qilingan
    item_count INT DEFAULT 0,
    total_price FLOAT DEFAULT 0,
    delivery_address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_status (status)
);

CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### 6. SHARHLAR VA REYTING
```sql
CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,  -- 1-5 yulduzlar
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_rating (rating)
);
```

### 7. TO'LOVLAR
```sql
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL UNIQUE,
    user_id INT NOT NULL,
    amount FLOAT NOT NULL,
    currency VARCHAR(10) DEFAULT 'UZS',
    payment_method VARCHAR(50) NOT NULL,
    -- payment_method: click, payme, card, cash, transfer
    status VARCHAR(50) DEFAULT 'kutilmoqda',
    -- Status: kutilmoqda, to'landi, bekor_qilingan
    transaction_id VARCHAR(200),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_status (status)
);
```

---

## 🔍 API da'volar va Sorashlar

### KATEGORIYALAR

```sql
-- Barcha kategoriyalarni olish
SELECT * FROM categories ORDER BY name_uz;

-- Kategoriyani ID bo'yicha olish
SELECT * FROM categories WHERE id = 1;

-- Yangi kategoriya qo'shish
INSERT INTO categories (name_uz, description, image_url) VALUES
('Elektronika', 'Zamonaviy elektronik mahsulotlar', 'url_link');
```

### MAHSULOTLAR

```sql
-- Kategoriya bo'yicha mahsulotlar
SELECT p.*, c.name_uz as category_name 
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.category_id = 1
ORDER BY p.name_uz;

-- Eng ko'p sotilgan mahsulotlar
SELECT id, name_uz, price, sales_count 
FROM products 
WHERE is_active = TRUE
ORDER BY sales_count DESC 
LIMIT 10;

-- Narx oralig'iga ko'ra mahsulotlar
SELECT * FROM products 
WHERE price BETWEEN 1000000 AND 5000000 
AND is_active = TRUE;

-- Mahsulot izlash
SELECT * FROM products 
WHERE name_uz LIKE '%Samsung%' 
AND is_active = TRUE;

-- Yangi mahsulot qo'shish
INSERT INTO products (name_uz, description_uz, price, category_id, stock) VALUES
('Samsung Galaxy A14', 'Yuqori sifatli smartphone', 3500000, 1, 50);

-- Mahsulot stokini yangilash
UPDATE products SET stock = stock - 1 WHERE id = 1;

-- Mahsulot sotilgan sonini yangilash
UPDATE products SET sales_count = sales_count + 1 WHERE id = 1;
```

### FOYDALANUVCHILAR

```sql
-- Barcha foydalanuvchilar
SELECT * FROM users ORDER BY created_at DESC;

-- Telegram ID bo'yicha foydalanuvchi
SELECT * FROM users WHERE telegram_id = 123456789;

-- Yangi foydalanuvchi ro'yxatdan o'tkazish
INSERT INTO users (telegram_id, first_name, last_name) VALUES
(123456789, 'Ahmad', 'Qodirov');

-- Foydalanuvchi ma'lumotlarini yangilash
UPDATE users 
SET first_name = 'Ahmad', last_name = 'Qodirov', 
    phone_number = '+998901234567', address = 'Tashkent'
WHERE telegram_id = 123456789;

-- Foydalanuvchi statistikasi
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(DISTINCT user_id) as active_users FROM orders;
```

### SAVAT

```sql
-- Foydalanuvchining savatini olish
SELECT ci.id, p.name_uz, p.price, ci.quantity, (p.price * ci.quantity) as total
FROM cart_items ci
JOIN products p ON ci.product_id = p.id
WHERE ci.cart_id = (SELECT id FROM carts WHERE user_id = 1);

-- Savat umumiy narxi
SELECT SUM(p.price * ci.quantity) as total_price, 
       SUM(ci.quantity) as total_items
FROM cart_items ci
JOIN products p ON ci.product_id = p.id
WHERE ci.cart_id = (SELECT id FROM carts WHERE user_id = 1);

-- Mahsulotni savatdan chiqarish
DELETE FROM cart_items WHERE id = 1;

-- Savatni bo'shash
DELETE FROM cart_items WHERE cart_id = 1;
```

### BUYURTMALAR

```sql
-- Foydalanuvchining buyurtmalari
SELECT * FROM orders 
WHERE user_id = 1 
ORDER BY created_at DESC;

-- Buyurtma detalyalari
SELECT o.id, o.total_price, o.status, o.created_at,
       oi.product_id, p.name_uz, oi.quantity, oi.price_at_purchase
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.id = 1;

-- Buyurtmaning statusini o'zgartirish
UPDATE orders SET status = 'yuborildi' WHERE id = 1;

-- Jami buyurtmalar soni
SELECT COUNT(*) as total_orders FROM orders;

-- Jami daromad
SELECT SUM(total_price) as total_revenue FROM orders WHERE status = 'yetkazildi';

-- T undirilmagan buyurtmalar
SELECT COUNT(*) as pending_orders 
FROM orders 
WHERE status IN ('yangi', 'tasdiqlandi');
```

### SHARHLAR VA REYTING

```sql
-- Mahsulotning sharhlarini olish
SELECT r.id, u.first_name, r.rating, r.comment, r.created_at
FROM reviews r
JOIN users u ON r.user_id = u.id
WHERE r.product_id = 1
ORDER BY r.created_at DESC;

-- Mahsulotning o'rtacha reytingi
SELECT product_id, ROUND(AVG(rating), 1) as avg_rating, COUNT(*) as review_count
FROM reviews
WHERE product_id = 1
GROUP BY product_id;

-- Yangi sharh qo'shish
INSERT INTO reviews (product_id, user_id, rating, comment) VALUES
(1, 1, 5, 'Juda yaxshi mahsulot, tavsiya qilaman!');

-- Eng ko'p sharh qo'yilgan mahsulotlar
SELECT p.id, p.name_uz, COUNT(r.id) as review_count
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id
GROUP BY p.id
ORDER BY review_count DESC
LIMIT 10;
```

### TO'LOVLAR

```sql
-- Buyurtmaning to'lovi
SELECT * FROM payments WHERE order_id = 1;

-- Tasdiqlanmagan to'lovlar
SELECT * FROM payments WHERE status = 'kutilmoqda';

-- To'lov statusini yangilash
UPDATE payments 
SET status = 'to'landi', transaction_id = 'TXN123456'
WHERE order_id = 1;

-- Jami to'langan summa
SELECT SUM(amount) as total_paid 
FROM payments 
WHERE status = 'to'landi';
```

### STATISTIKA

```sql
-- Jami mahsulotlar
SELECT COUNT(*) as total_products FROM products;

-- Jami foydalanuvchilar
SELECT COUNT(*) as total_users FROM users;

-- Jami buyurtmalar
SELECT COUNT(*) as total_orders FROM orders;

-- Jami daromad
SELECT SUM(total_price) as total_revenue FROM orders WHERE status != 'bekor_qilingan';

-- Kunlik daromad
SELECT DATE(created_at) as date, SUM(total_price) as daily_revenue
FROM orders
WHERE status != 'bekor_qilingan'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Eng ko'p sotilgan mahsulotlar
SELECT name_uz, price, sales_count
FROM products
ORDER BY sales_count DESC
LIMIT 10;

-- Eng ko'p buyurtma bergan foydalanuvchilar
SELECT u.id, u.first_name, u.last_name, COUNT(o.id) as order_count, SUM(o.total_price) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
ORDER BY total_spent DESC
LIMIT 10;
```

---

## 💻 Foydalanish

### Botni Boshlash
```bash
python main.py
```

### Telegram da Foydalanish

1. **/start** - Botni boshlash
2. **🛍️ Do'konga kirish** - Kategoriyalarni ko'rish
3. **⭐ Eng ko'p sotilganlar** - Top mahsulotlar
4. **🛒 Savatni ko'rish** - Savat bilan ishlash
5. **📦 Buyurtmalarim** - Mening buyurtmalarim
6. **👤 Profilim** - Profil ma'lumotlari

---

## 🔧 Masalolarni Hal Qilish

### Masala: "Database connection error"
```bash
# MySQL ishlayotganini tekshiring
mysql -u root -p

# .env faylida DB_HOST, DB_USER, DB_PASSWORD to'g'riligini tekshiring
```

### Masala: "Table was not found"
```sql
-- Jadvallari yana yaratishing
SOURCE database/shop_db_mysql.sql;
```

### Masala: "Encoding issues - Uzbek tilida muammo"
```sql
-- Bazani UTF-8 bilan o'zgartiring
ALTER DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Masala: Bot buyurtmalarni saqlamayapti
```python
# db/database.py faylida DATABASE_URL to'g'ri ekanligini tekshiring
# Ayniqsa DB_NAME parametri
```

---

## 📧 Qo'llab-Quvvatlash

Agar savollar bo'lsa, [GitHub Issues](https://github.com) orqali yozing.

---

## 📝 Lisenziya

MIT License - Bepul foydalanish

---

**Yaratuvchi:** Telegram Bot Development Team  
**Tarih:** 2024  
**Til:** Uzbek Latin
