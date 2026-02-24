# ⚡ Tezkor Boshlash - MySQL Bilan

## 🚀 1-bosqich: Database O'rnatish (Windows)

### MySQL o'rnatish
1. [mysql.com](https://mysql.com) dan MySQL Server 8.0+ ni yuklab oling
2. O'rnatuvchini ochinb setup qiling
3. Root parolini yodda saqlab qoling

### MySQL Workbench (GUI uchun)
```bash
# Yoki terminal orqali MySQL CLI dan foydalaning
mysql -u root -p
```

## 🗄️ 2-bosqich: Database va Jadvallari Yaratish

```sql
-- 1. Yangi database yaratish
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. Database'ni tanlash
USE shop_db;

-- 3. Jadvallari yaratish (SQL faylini import qiling)
-- database/shop_db_mysql.sql faylini MySQL Workbench'da ochinb palitrasini ishlating
-- Or use command line:
-- mysql -u root -p shop_db < database/shop_db_mysql.sql
```

## 🔧 3-bosqich: .env Faylini Sozlash

```env
# BOT SOZLAMALARI
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ADMINS=123456789,987654321

# DATABASE SOZLAMALARI
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=shop_db

TIMEZONE=Asia/Tashkent
```

## 📦 4-bosqich: Python Paketlarini O'rnatish

```bash
# Virtual environment yaratish (ixtiyoriy)
python -m venv venv

# Virtual environment'ni aktivlash
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Paketlarni o'rnatish
pip install -r requirements.txt
```

## ▶️ 5-bosqich: Botni Ishga Tushirish

```bash
# main.py faylini ishga tushirish
python main.py
```

## ✅ Database Tekshirish

```sql
-- Jadvallari ko'rish
SHOW TABLES;

-- Kategoriyalar
SELECT * FROM categories;

-- Mahsulotlar
SELECT * FROM products;

-- Foydalanuvchilar
SELECT * FROM users;
```

---

## 🆘 Tez Masalalarni Hal Qilish

### ❌ Xato: "Access denied for user 'root'@'localhost'"
```bash
# MySQL'ga qayta kirish
mysql -u root -p
# Parolingizni kiriting
```

### ❌ Xato: "Unknown database 'shop_db'"
```sql
-- Database yaratishni bilang
CREATE DATABASE shop_db;
USE shop_db;
SOURCE database/shop_db_mysql.sql;
```

### ❌ Xato: "Table 'shop_db.categories' doesn't exist"
```bash
# database/shop_db_mysql.sql faylini qayta ishga tushiring
mysql -u root -p shop_db < database/shop_db_mysql.sql
```

### ❌ Xato: Bot UTF-8 bilan muammo
```sql
-- SQL connection UTF-8 ho'latini tekshiring
SET NAMES utf8mb4;
SET CHARACTER_SET_CLIENT = utf8mb4;
```

---

## 📋 Test Ma'lumotlarni Yuklashtirish

```sql
-- Kategoriya qo'shish
INSERT INTO categories (name_uz, description) VALUES
('Elektronika', 'Zamonaviy elektronik mahsulotlar'),
('Kiyim-kechak', 'Erkak va ayol kiyim-kechagi'),
('Ovqat', 'Sog''a va mazali ovqatlalar');

-- Mahsulot qo'shish
INSERT INTO products (name_uz, description_uz, price, category_id, stock) VALUES
('Samsung Galaxy A14', 'Smartphone 128GB', 3500000, 1, 50),
('Xiaomi Redmi Note 12', 'Smartphone 256GB', 2800000, 1, 40),
('Fo''tbolka (XL)', 'Sutka 100% paxta', 450000, 2, 100);

-- Foydalanuvchi qo'shish
INSERT INTO users (telegram_id, first_name, last_name) VALUES
(123456789, 'Ahmad', 'Qodirov'),
(987654321, 'Sevara', 'Hasanova');
```

---

## 🎯 Keyingi Bosqichlar

1. Bot tokeni bilan Telegram'da test qiling: `/start`
2. Kategoriyalarni ko'ring: **🛍️ Do'konga kirish**
3. Mahsulot qo'shing: **⭐ Eng ko'p sotilganlar**
4. Savat bilan ishlang: **🛒 Savatni ko'rish**
5. Buyurtma qiling: **📦 Buyurtmalarim**

---

## 💡 Foydali Linklar

- [MySQL Documentation](https://mysql.com/doc)
- [Aiogram Documentation](https://aiogram.dev)
- [SQLAlchemy ORM](https://sqlalchemy.org)
- [Python TelegramBot](https://github.com/telegramdesktop/tdesktop)

---

**Omad!** 🎉
