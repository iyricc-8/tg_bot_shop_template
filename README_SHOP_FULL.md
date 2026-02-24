# 🛍️ Telegram Bot Online Magazin

**Zamonaviy, to'liq функционал bilan online do'kon - Telegram messenjerida!**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Language](https://img.shields.io/badge/language-Python%203.9%2B-orange)
![Database](https://img.shields.io/badge/database-MySQL-blue)

---

## ✨ Asosiy Xususiyatlari

### 📦 Mahsulot Boshqaruvi
- ✅ Kategoriyalar bilan tashkil etilgan katalog
- ✅ Mahsulot detalyalari va tasviri
- ✅ Narx, stock, va satish statistikasi
- ✅ Mahsulot qidirish va filtrlash
- ✅ Eng ko'p sotilgan mahsulotlar ro'yxati

### 🛒 Savat va Buyurtma
- ✅ Dinamik savat boshqaruvi
- ✅ Mahsulot miqdorini o'zgartirish
- ✅ Savat qiymati hisoblash (real-time)
- ✅ Oson buyurtma oformlash
- ✅ F.I.SH va manzil kiritish

### 📊 Buyurtma Sistema
- ✅ Buyurtma tracking
- ✅ Status boshqaruvi (yangi → tasdiqlandi → yuborildi → yetkazildi)
- ✅ Buyurtma tarixini ko'rish
- ✅ To'lov ma'lumotlari saqlanishi

### ⭐ Sharh va Reyting
- ✅ Foydalanuvchilar sharhlar qoldirishlari
- ⭐ 1-5 yulduzlar bilan reyting sistemi
- ✅ O'rtacha reyting hisoblash
- ✅ Eng yaxshi mahsulotlarni ko'rish

### 💳 To'lov Usullari
- ✅ Click to'lov
- ✅ Payme to'lov
- ✅ Bank kartasi
- ✅ Naqd to'lov
- ✅ Pul ko'chirish

### 👤 Foydalanuvchi Profilim
- ✅ Shaxsiy ma'lumotlar saqlash
- ✅ Telefon va manzil yangilash
- ✅ Buyurtma tarixi
- ✅ Qoldirgan sharhlari

### 🎯 Admin Panel (Kelasi versiya)
- ✅ Mahsulotlarni boshqarish
- ✅ Kategoriyalar setup
- ✅ Buyurtmalarni monitoring
- ✅ Satish statistikasi
- ✅ Foydalanuvchi boshqaruvi

---

## 🛠️ Texnologiya Stakki

| Texnologiya | Versiya | Maqsadi |
|-------------|---------|--------|
| **Python** | 3.9+ | Asosiy til |
| **Aiogram** | 3.7+ | Telegram Bot API |
| **SQLAlchemy** | 2.0+ | ORM Framework |
| **MySQL** | 8.0+ | Database |
| **Async/Await** | Built-in | Asinxron operatsiyalar |

---

## 📋 Jadvallari va Ma'lumotlar Tuzilishi

```
┌──────────────────────────────────────────────────┐
│          SHOP DATABASE ARCHITECTURE              │
├──────────────────────────────────────────────────┤
│
│  USERS                    PRODUCTS               │
│  ├─ id                    ├─ id                  │
│  ├─ telegram_id           ├─ name_uz             │
│  ├─ first_name            ├─ description_uz      │
│  ├─ last_name       ┌────→├─ price              │
│  ├─ phone_number    │     ├─ category_id        │
│  └─ address         │     ├─ stock              │
│        │            │     └─ sales_count        │
│  CARTS │            │                           │
│  ├─ id │            │  CATEGORIES              │
│  └─ user_id◄────────┘  ├─ id                   │
│        │                ├─ name_uz              │
│        ↓                └─ description          │
│  CART_ITEMS                                     │
│  ├─ id                ORDERS          PAYMENTS │
│  ├─ cart_id     ┌────→├─ id          ├─ id    │
│  ├─ product_id  │     ├─ user_id     ├─ order │
│  └─ quantity    │     ├─ status      ├─ amount│
│                 │     ├─ total_price ├─ status│
│                 │     └─ items◄──┐   └─ method│
│          ORDER_ITEMS   │         │             │
│          ├─ order_id───┘         │   REVIEWS  │
│          ├─ product_id           └──→├─ id   │
│          └─ quantity_price            ├─ rating
│                                       └─ comment
│
└──────────────────────────────────────────────────┘
```

---

## 🚀 Boshlash

### Tezkor O'rnatish (5 daqiqa)
```bash
# 1. Repo klonlash
git clone <repo-url>
cd Shablon_8_homework

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Dependencies o'rnatish
pip install -r requirements.txt

# 4. .env faylini sozlash
cp .env.dist .env
# .env'da MySQL ma'lumotlarini kiriting

# 5. Database yaratish
mysql -u root -p shop_db < database/shop_db_mysql.sql

# 6. Botni ishga tushirish
python main.py
```

### MySQL Setup
```sql
-- 1. Database yaratish
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. Jadvallari yuklashtirish
mysql -u root -p shop_db < database/shop_db_mysql.sql

-- 3. Test ma'lumotlarini kiritish (ixtiyoriy)
-- SQL faylida misollar mavjud
```

### .env Konfiguratsiyasi
```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here
ADMINS=123456789,987654321

# MySQL Database
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=shop_db

# Boshqa parametrlar
TIMEZONE=Asia/Tashkent
```

---

## 📱 Telegram da Foydalanish

### Asosiy Menyu
```
🏠 ASOSIY MENYU
├─ 🛍️ Do'konga kirish → Kategoriyalarni tanlash
├─ 🛒 Savatni ko'rish → Savatning tarkibini ko'rish
├─ ⭐ Eng ko'p sotilganlar → Top 10 mahsulotlar
├─ 📦 Buyurtmalarim → Buyurtma tarixini ko'rish
├─ 👤 Profilim → Shaxsiy ma'lumotlar
└─ ❓ Yordam → Yordam ma'lumotlari
```

### Xarid Qilish Jarayoni
```
1️⃣ Do'konga kirish
   ↓
2️⃣ Kategoriya tanlash
   ↓
3️⃣ Mahsulot tanlash
   ↓
4️⃣ Miqdor kiritish
   ↓
5️⃣ Savatga qo'shish
   ↓
6️⃣ Savatni ko'rish
   ↓
7️⃣ Buyurtma qilish (Checkout)
   ↓
8️⃣ F.I.SH. kiritish
   ↓
9️⃣ Telefon raqlamni kiritish
   ↓
🔟 Manzilni kiritish
   ↓
1️⃣1️⃣ To'lov usulini tanlash
   ↓
1️⃣2️⃣ Buyurtma tasdiqlash
   ↓
✅ BUYURTMA QABUL QILINDI!
```

---

## 📊 Database SQL Sorashlar

### O'rta Foydali Sorashlar
```sql
-- Eng ko'p sotilgan mahsulotlar
SELECT name_uz, sales_count FROM products 
ORDER BY sales_count DESC LIMIT 10;

-- Foydalanuvchi buyurtmalarim
SELECT id, total_price, status FROM orders 
WHERE user_id = 1 ORDER BY created_at DESC;

-- Mahsulotning o'rtacha reytingi
SELECT ROUND(AVG(rating), 1) FROM reviews 
WHERE product_id = 1;

-- Jami daromad (butun vaqt)
SELECT SUM(total_price) FROM orders 
WHERE status != 'bekor_qilingan';

-- Ruz bo'yicha daromad
SELECT DATE(created_at), SUM(total_price) 
FROM orders GROUP BY DATE(created_at);
```

Barcha SQL sorashlar uchun: [SQL_EXAMPLES.sql](database/SQL_EXAMPLES.sql)

---

## 📁 Loyiha Struktura

```
project/
├── main.py                 # Bot asosiy fayli
├── requirements.txt        # Python dependencies
├── .env.dist              # Environment template
├── config/                # Konfiguratsiya
│   └── config.py
├── db/                    # Database ORM
│   ├── models.py         # SQLAlchemy models
│   ├── database.py       # Database connection
│   └── repositories.py   # Database queries
├── database/             # SQL fayllar
│   ├── shop_db_mysql.sql # MySQL jadvallari
│   └── SQL_EXAMPLES.sql  # Misollar
├── handlers/             # Telegram handlers
│   ├── shop_full.py     # Asosiy shop logic
│   ├── shop.py
│   └── users/
├── keyboards/            # Inline klaviaturalar
│   └── shop_keyboards.py
├── states/               # FSM states
│   └── shop_states.py
├── services/             # Business logic
│   └── db_api/
│       └── shop_services.py  # Database services
└── middlewares/          # Middleware

📚 DOKUMENTATSIYA
├── README.md            # Bu fayl
├── INSTALLATION_GUIDE.md (o'rnatish qo'llanmasi)
├── MYSQL_QUICKSTART.md  (tezkor boshlash)
└── SQL_DOCUMENTATION.md (SQL ma'lumotlar)
```

---

## 🔌 API va Servicelari

### Database Services (services/db_api/shop_services.py)

#### CategoryService
```python
await CategoryService.get_all_categories(session)
await CategoryService.get_category_by_id(session, category_id)
```

#### ProductService
```python
await ProductService.get_products_by_category(session, category_id)
await ProductService.get_product_by_id(session, product_id)
await ProductService.get_top_products(session, limit=10)
await ProductService.search_products(session, query)
```

#### UserService
```python
await UserService.get_or_create_user(session, telegram_id, first_name)
await UserService.update_user_profile(session, user_id, ...)
```

#### CartService
```python
await CartService.add_to_cart(session, user_id, product_id, quantity)
await CartService.get_cart_with_items(session, user_id)
await CartService.get_cart_total(session, user_id)
await CartService.clear_cart(session, user_id)
```

#### OrderService
```python
await OrderService.create_order(session, user_id, address, notes)
await OrderService.get_user_orders(session, user_id)
await OrderService.update_order_status(session, order_id, status)
```

#### ReviewService
```python
await ReviewService.add_review(session, product_id, user_id, rating, comment)
await ReviewService.get_product_reviews(session, product_id)
await ReviewService.get_average_rating(session, product_id)
```

---

## 🐛 Masalolarni Hal Qilish

### Xato: "Database connection error"
```bash
# 1. MySQL ishlayotganini tekshiring
mysql -u root -p

# 2. .env dagi ma'lumotlarni tekshiring
# 3. Database o'rishing lmagan bo'lsa:
mysql -u root -p shop_db < database/shop_db_mysql.sql
```

### Xato: "Table was not found"
```sql
-- SQL jadvallari qayta yaratish
USE shop_db;
SOURCE database/shop_db_mysql.sql;
```

### Uzbek tilida muammo
```env
# .env'da charset ko'rsatish
DB_CHARSET=utf8mb4
```

### Xato: Bot javob bermayapti
```bash
# 1. Bot token to'g'ri ekanligini tekshiring
# 2. aiogram version: pip install aiogram>=3.7
# 3. Logs'larni tekshiring
```

---

## 🎓 Maslahatlar va O'z Darslar

- **Async/Await**: Barcha database amaliyotlari async
- **SQLAlchemy ORM**: Type-safe va flexible
- **FSM States**: Buyurtma oformlash jarayoni
- **Inline Keyboards**: Dinamik menu navigatsiyasi
- **UTF-8 Encoding**: Uzbek lotin tilida to'g'ri ishlash

---

## 📈 Kelasi Versiyalar (v2.0+)

- [ ] Admin Panel GUI
- [ ] Payment Gateway Integration (Click, Payme)
- [ ] Email/SMS Notifications
- [ ] Advanced Analytics
- [ ] Inventory Management
- [ ] Multi-language Support
- [ ] Machine Learning Recommendations
- [ ] REST API (FastAPI)
- [ ] Web Dashboard
- [ ] Mobile App Integration

---

## 🤝 Hissə Qo'shish

Xatolarini toping, taklif bering va PR jo'nating:
1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add AmazingFeature'`)
4. Branch'ga push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request ochingg

---

## 📝 Lisenziya

Bu loyiha MIT Lisenziyasi bilan muhofaza qilingan. Batafsil: [LICENSE](LICENSE)

---

## 📞 Murojaat

- 💬 Telegram: [@bot_support](https://t.me/bot_support)
- 📧 Email: support@telegrambotshop.uz
- 🐛 Issues: [GitHub Issues](https://github.com)

---

## 📚 Qo'shimcha Resurslar

- [Aiogram Documentation](https://aiogram.dev)
- [SQLAlchemy ORM](https://sqlalchemy.org)
- [MySQL Reference](https://dev.mysql.com/doc)
- [Python Async](https://docs.python.org/3/library/asyncio.html)
- [Telegram Bot API](https://core.telegram.org/bots)

---

**Yaratuvchi:** Telegramm Bot Development Team  
**Lotintirish:** O'zbek Lotin (Cyrillic → Latin)  
**Tarih:** 2024-2025  
**Versiya:** 1.0.0  

---

⭐ **Agar yoqqan bo'lsa, ⭐ star berish unutmang!**

🙏 **Rahmat foydalanish uchun!**
