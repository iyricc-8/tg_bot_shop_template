# 🚀 TOLIQ O'RNATISH QOLANMASI - STEP BY STEP

**Ba'tafsil qo'llanma! O'rnatish 30 daqiqada bitib ketadi.**

---

## 📋 REJA

1. ✅ MySQL O'rnatish
2. ✅ Database va Jadvallari Yaratish
3. ✅ Python Environment Setup
4. ✅ Dependencies O'rnatish
5. ✅ .env Faylini Sozlash
6. ✅ Botni Ishga Tushirish
7. ✅ Test Qilish

---

## 🔧 STEP 1: MySQL O'rnatish

### Windows'da:
```bash
1. mysql.com/downloads'dan MySQL Community Server ni yuklab oling
   (Versiya: 8.0 yoki undan yangi)

2. O'rnatuvchini ishga tushiring (double-click)

3. Setup qadamlarini davom ettiring:
   ✓ Setup Type: Developer Default
   ✓ Installation: MySQL Server
   ✓ MySQL Server 8.0.29 - Port: 3306
   ✓ MySQL Server Configuration Type: Development Computer
   ✓ Authentication Method: MySQL 8.0 Compatible Authentication

4. Root parolini sozlash:
   Username: root
   Password: sizning_xohlaydigan_parol (yod tutuvchi be qiling!)

5. MySQL Service'ni Windows servisiga qo'shish
   ✓ Service istisno: MYSQL80
```

### Mac'da:
```bash
# Homebrew orqali
brew install mysql

# Boshlash
brew services start mysql

# Root parolini sozlash
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';
```

### Linux'da:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server

# Sozlash
sudo mysql_secure_installation
```

### MySQL'ga Ulanish
```bash
# Terminal/Command Prompt'ni oching
mysql -u root -p

# Parolni kiriting: YOUR_PASSWORD
# Welcome to MySQL'ni ko'rsatsa, tayyor!

# Chiqish: EXIT yoki quit
```

---

## 🗄️ STEP 2: Database Yaratish

### 2.1 Database Yaratish
```bash
# MySQL Command Line Client'ni oching
mysql -u root -p

# Parol kiritish
Enter password: ••••••••
```

### 2.2 SQL Commands
```sql
-- Database yaratish (UTF-8 bilan)
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Database'ni tanlash
USE shop_db;

-- Status ko'rish
SHOW TABLES;  # Qo'sh jadval bo'lishi kerak (hali qara)
```

### 2.3 SQL Jadvallari Yaratish

**Variant A: Command Line'dan**
```bash
# Database faylini import qiling
mysql -u root -p shop_db < path/to/database/shop_db_mysql.sql

# Tekshirish
mysql -u root -p shop_db
SHOW TABLES;
# 9 ta jadval ko'rinishi kerak
```

**Variant B: MySQL Workbench GUI'dan (Osonroq)**
```
1. MySQL Workbench'ni oching
2. File → Open SQL Script
3. database/shop_db_mysql.sql faylini tanlang
4. Execute Scripts (⚡️ tugmasi)
5. Jadvallari yaratildi!
```

### 2.4 Jadvallari Tekshirish
```sql
-- Terminal'da:
mysql -u root -p

USE shop_db;
SHOW TABLES;

# Javob:
# +-----------------------+
# | Tables_in_shop_db     |
# +-----------------------+
# | carts                 |
# | cart_items            |
# | categories            |
# | order_items           |
# | orders                |
# | payments              |
# | products              |
# | reviews               |
# | users                 |
# +-----------------------+

```

---

## 🐍 STEP 3: Python Environment

### 3.1 Python O'rnatish (Agar o'rnatilmagan bo'lsa)
```bash
# python.org'dan Python 3.9+ ni yuklab oling
# Installer'ni ishga tushiring
# ⚠️ "Add Python to PATH" ni TEKSHIRING!

# Tekshirish
python --version
# Output: Python 3.9.x yoki undan yangi
```

### 3.2 Virtual Environment Yaratish
```bash
# Proyekta katalogida terminal'ni oching

# Virtual environment yaratish
python -m venv venv

# Aktivlash
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Terminal prompt'i o'zgarishi kerak: (venv) C:\...>
```

---

## 📦 STEP 4: Dependencies O'rnatish

### 4.1 Requirements.txt Tekshirish
```bash
# Qo'llanma faylda mavjud: requirements.txt
cat requirements.txt

# Ko'rinishi:
# aiogram>=3.7,<4.0
# python-dotenv>=1.0
# sqlalchemy>=2.0
# ... va boshqa
```

### 4.2 Paketlarni O'rnatish
```bash
# Virtual environment aktiv bo'lsa, ishga tushiring:
pip install -r requirements.txt

# Wait for installation...
# Successfully installed ... (13 packages)
```

### 4.3 Paketlarni Tekshirish
```bash
pip list

# Bu paketlar bo'lishi kerak:
# - aiogram              3.7.0
# - SQLAlchemy           2.0.0
# - python-dotenv        1.0.0
# - mysql-connector      8.x.x
# ... va boshqalar
```

---

## ⚙️ STEP 5: .env Faylini Sozlash

### 5.1 .env.dist Nusxalash
```bash
# Windows (PowerShell):
Copy-Item .env.dist -Destination .env

# Mac/Linux (Terminal):
cp .env.dist .env

# Yoki qo'l bilan: .env.dist'ni text editorida ochinb "Save As" .env
```

### 5.2 .env Faylini Tahrirlash
```bash
# Text editor (Notepad++, VS Code, etc)'da .env'ni oching

# Quyida ko'rsatilgan kuzinishni to'ldiringi:
```

### 5.3 .env Tuzilishi
```env
# ========================
# BOT SOZLAMALARI
# ========================

# Telegram Bot Token (t.me/BotFather'dan oling)
BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh

# Admin Telegram ID'lari
# Bizning: t.me/your_username'dan oling: /id
ADMINS=123456789,987654321

# ========================
# MYSQL DATABASE SOZLAMALARI
# ========================

# Database Type (qo'llanma: mysql)
DB_TYPE=mysql

# MySQL Server Address
DB_HOST=localhost

# MySQL Port (standart: 3306)
DB_PORT=3306

# MySQL Username (standart: root)
DB_USER=root

# MySQL Parol (o'rnatish vaqtida siz sozlagan parol)
DB_PASSWORD=your_mysql_password

# Database Nomi (yuqorida yaratgan)
DB_NAME=shop_db

# ========================
# BOSHQA
# ========================

TIMEZONE=Asia/Tashkent
```

### 5.4 Tekshirish (Misollar)
```
BOT_TOKEN=7123495612:AAHkJ6RRSSHLOa8LKH3kS_yL7H8hH1a5hmk
ADMINS=123456789
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=mysql1234
```

---

## ▶️ STEP 6: Botni Ishga Tushirish

### 6.1 Starting Qo'mandasini Yazish

**Terminal/Command Prompt'ni Oching:**
```bash
# 1. Proyekta katalogida bo'lish
cd C:\Users\YourUsername\OneDrive\Desktop\Telegramm Bot\Homeworks\Shablon_8_homework

# 2. Virtual environment'ni aktivlash
venv\Scripts\activate

# 3. Bot'ni ishga tushirish
python main.py

# Javob: INFO:asyncio:server: asyncio event loop started
# ... Botning ready ekanligini ko'rsatadi
```

### 6.2 Console Output
```
2024-02-24 10:15:30,123 - INFO - Bot started successfully
2024-02-24 10:15:30,245 - INFO - Listening for updates...
2024-02-24 10:15:35,567 - INFO - User 123456789 sent /start command
```

### 6.3 Xatolarni Tekshirish

**Agar error bo'lsa:**

```python
# Error: "ConnectionRefusedError"
# →  MySQL ishlamayapti. Tekshiring: mysql -u root -p

# Error: "Unknown database 'shop_db'"
# → Database yaratilmagan. STEP 2'ni takrorlang

# Error: "Access denied for user 'root'"
# → Parol noto'g'ri. .env'ni tekshiring

# Error: "No module named 'aiogram'"
# → Dependencies o'rnatilmagan. STEP 4'ni takrorlang
```

---

## 🧪 STEP 7: Telegram'da Test Qilish

### 7.1 Telegram'da Bot'ni Topish
```
1. Telegram'ni oching
2. Search: @YourBotName (t.me/BotFather'dan oling)
3. Bot'ni tanlang
```

### 7.2 Buyurtma Beraylik!
```
💬 Siz:
/start

📱 Bot:
👋 Assalamu alaikum, Ahmad!
🛍️ Online do'konimizga xush kelibsiz!

[Tugmalar ko'rinishi]
🛍️ Do'konga kirish
🛒 Savatni ko'rish
⭐ Eng ko'p sotilganlar
📦 Buyurtmalarim
👤 Profilim
❓ Yordam
```

### 7.3 Oсновные Testing Jarayoni

```
1️⃣ /start → Asosiy menu ko'rinishi kerak ✅

2️⃣ 🛍️ Do'konga kirish → Kategoriyalar ko'rinishi kerak ✅

3️⃣ Kategoriya tanlash → Mahsulotlar ko'rinishi kerak ✅

4️⃣ Mahsulot tanlash → Mahsulot detalyalari ko'rinishi kerak ✅

5️⃣ 🛒 Savatga qo'shish → "✅ Savatga qo'shildi" ko'rinishi kerak ✅

6️⃣ 🛒 Savatni ko'rish → Mahsulotlar bilan savat ko'rinishi kerak ✅

7️⃣ Buyurtma qilish → F.I.SH. kiritish uchun so'rash ko'rinishi kerak ✅

8️⃣ Buyurtma ma'lumotlarini to'ldirish (ismingiz yetkazib berish manzili) ✅

9️⃣ Buyurtma tasdiqlash → Chek ko'rinishi kerak ✅

✅ Hammasi tayyor!
```

---

## 🔄 Keyin Qayta Ishga Tushirish

```bash
# Har safar:
1. Terminal'ni version proyek
2. Virtual environment'ni aktivlash: venv\Scripts\activate
3. Bot'ni ishga: python main.py
4. STOP: Ctrl+C
```

---

## 📊 Database'ni Tekshirish

### Terminal'dan:
```sql
-- Database'ga kiritish
mysql -u root -p shop_db

-- Jadvallari ko'rish
SHOW TABLES;

-- Mahsulotlarni ko'rish
SELECT * FROM products;

-- Kategoriyalarni ko'rish
SELECT * FROM categories;

-- Foydalanuvchilarni ko'rish
SELECT * FROM users;
```

---

## 🎯 Troubleshooting Jadval

| Muammo | Yechim |
|--------|--------|
| Bot javob bermayapti | main.py ishlamayapti. pyterminalni tekshiring |
| MySQL connection error | MySQL ishlamayapti. `mysql -u root -p` bilan tekshiring |
| Bot to'hamayapti | BotToken noto'g'ri. t.me/BotFather'dan tekshiring |
| Database error | .env'da DB ma'lumotlari noto'g'ri. Tekshiring |
| Uzbek til muammo | UTF-8 encoding o'rnatilish. DB_CHARSET=utf8mb4 qo'shing |
| requirements failed | Python 3.9+ zarur. python --version tekshiring |

---

## 📁 Keyin Yaratish Kerak Bo'lgan Fayllar (Kelasi versiyalar)

```bash
handlers/shop_user.py      # Foydalanuvchi commands
handlers/shop_admin.py     # Admin panel
handlers/payments.py       # To'lov integration
services/payment_service.py # Payment gateway
utils/validators.py        # Data validation
utils/formatters.py        # Text formatting
```

---

## 🎓 Maqsadli Qo'shimcha

### Admin Panel (Kelasi versiya)
- ✅ Mahsulotlarni CRUD
- ✅ Kategoriyalarni boshqarish
- ✅ Buyurtmalarni monitoring
- ✅ Satish statistikasi

### Integration (Kelasi versiya)
- ✅ Click To'lov API
- ✅ Payme To'lov API
- ✅ Email Notification
- ✅ SMS Notification

### Advanced (Kelasi versiya)
- ✅ REST API (FastAPI)
- ✅ Web Dashboard
- ✅ Machine Learning Recommendations
- ✅ Inventory Management

---

## ✅ TAYYOR!

**Agar quyidagi ko'rinsa, muvaffaqiyatli o'natildi:**

```
✅ Terminal'da: INFO:asyncio Server started
✅ Telegram'da: Bot respond qaytaradi
✅ Database: Jadvallari ko'rinib turibdi
✅ .env: Barcha ma'lumotlar to'ldirilgan
```

---

## 🆘 Qoshimcha Yordam

Agar muammo bo'lsa:
1. [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) o'qing
2. [SQL_EXAMPLES.sql](database/SQL_EXAMPLES.sql) tekshiring
3. Logs'larni o'qing (console'da)
4. [GitHub Issues](https://github.com) ochinng

---

## 📞 Murojaat

- 📧 Email: support@shop.uz
- 💬 Telegram: @support_bot
- 🐛 Bug reporti: [Issues](https://github.com/issues)

---

**OMAD! 🍀**
