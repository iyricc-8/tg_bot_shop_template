-- ========================
-- TELEGRAM BOT SHOP DATABASE
-- SQL MISOLLARI VA FOYDALI SORASHLAR
-- Uzbek Lotin - UTF-8 Encoding
-- ========================

-- ========================
-- 1. DATABASE VA JADVALLARINI TEKSHIRISH
-- ========================

-- Barcha jadvallari ko'rish
SHOW TABLES;

-- Jadval strukturasini ko'rish
DESCRIBE categories;
DESCRIBE products;
DESCRIBE users;
DESCRIBE orders;
DESCRIBE payments;
DESCRIBE reviews;

-- ========================
-- 2. KATEGORIYALARGA DOIR SORASHLAR
-- ========================

-- Barcha kategoriyalarni olish
SELECT * FROM categories ORDER BY name_uz;

-- Kategoriya soni
SELECT COUNT(*) as total_categories FROM categories;

-- Kategoriyaga tegishli mahsulot soni
SELECT c.id, c.name_uz, COUNT(p.id) as product_count
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.name_uz
ORDER BY product_count DESC;

-- Yangi kategoriya qo'shish
INSERT INTO categories (name_uz, description, image_url) VALUES
('Elektronika', 'Barcha yovvoyi elektronika mahsulotlari', 'https://example.com/electronics.jpg'),
('Kiyim-kechak', 'Yiqilgan va ayol kiyim-kechaklari', 'https://example.com/clothes.jpg'),
('Ovqat-ichimlik', 'Sog''a ishtiyoqli ovqat va ichimliklar', 'https://example.com/food.jpg');

-- ========================
-- 3. MAHSULOTLARGA DOIR SORASHLAR
-- ========================

-- Barcha mahsulotlar (kategoriya bilan)
SELECT p.id, p.name_uz, p.price, c.name_uz as category,
       p.stock, p.sales_count, p.is_active
FROM products p
JOIN categories c ON p.category_id = c.id
ORDER BY p.name_uz;

-- Faqat faol mahsulotlar
SELECT * FROM products WHERE is_active = TRUE ORDER BY name_uz;

-- Eng ko'p sotilgan 10 ta mahsulot
SELECT id, name_uz, price, sales_count, stock
FROM products
WHERE is_active = TRUE
ORDER BY sales_count DESC
LIMIT 10;

-- Narx oralig'iga ko'ra mahsulotlar (1M - 5M so'm)
SELECT * FROM products
WHERE price BETWEEN 1000000 AND 5000000
AND is_active = TRUE
ORDER BY price;

-- Qolgan stoki 20 ta kamroq mahsulotlar
SELECT id, name_uz, stock FROM products
WHERE stock < 20
AND is_active = TRUE
ORDER BY stock ASC;

-- Mahsulot izlash (name bor)
SELECT * FROM products
WHERE name_uz LIKE '%Samsung%'
OR name_uz LIKE '%xiaomi%'
OR name_uz LIKE '%iphone%';

-- Barcha mahsulot bilan o'rtacha reyting
SELECT p.id, p.name_uz, p.price, 
       ROUND(AVG(r.rating), 1) as avg_rating,
       COUNT(r.id) as review_count
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id
WHERE p.is_active = TRUE
GROUP BY p.id, p.name_uz, p.price
ORDER BY avg_rating DESC;

-- Kategoriya bo'yicha mahsulot soni va narxlar
SELECT c.name_uz,
       COUNT(p.id) as product_count,
       MIN(p.price) as min_price,
       MAX(p.price) as max_price,
       ROUND(AVG(p.price), 0) as avg_price
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.name_uz;

-- ========================
-- 4. FOYDALANUVCHILARGA DOIR SORASHLAR
-- ========================

-- Barcha foydalanuvchilar
SELECT id, telegram_id, first_name, last_name, 
       phone_number, address, created_at
FROM users
ORDER BY created_at DESC;

-- Telegram ID bo'yicha foydalanuvchi
SELECT * FROM users WHERE telegram_id = 123456789;

-- Foydalanuvchilar statistikasi
SELECT COUNT(*) as total_users FROM users;

-- Eng yaqinda ro'yxatdan o'tgan foydalanuvchilar
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 10;

-- Profili taklif o'rnatilmagan foydalanuvchilar
SELECT * FROM users
WHERE phone_number IS NULL
OR address IS NULL;

-- Eng ko'p buyurtma bergan foydalanuvchilar
SELECT u.id, u.first_name, u.last_name,
       COUNT(o.id) as order_count,
       SUM(o.total_price) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.first_name, u.last_name
ORDER BY total_spent DESC
LIMIT 10;

-- ========================
-- 5. SAVATGA DOIR SORASHLAR
-- ========================

-- Barcha aktivli savatlari (mahsulotlar bilan)
SELECT c.id, u.first_name, u.telegram_id,
       COUNT(ci.id) as item_count,
       SUM(p.price * ci.quantity) as total_value
FROM carts c
JOIN users u ON c.user_id = u.id
LEFT JOIN cart_items ci ON c.id = ci.cart_id
LEFT JOIN products p ON ci.product_id = p.id
GROUP BY c.id, u.first_name, u.telegram_id;

-- Muayyan foydalanuvchining savati
SELECT p.id, p.name_uz, p.price, ci.quantity,
       (p.price * ci.quantity) as item_total
FROM cart_items ci
JOIN products p ON ci.product_id = p.id
WHERE ci.cart_id = (SELECT id FROM carts WHERE user_id = 1);

-- Savat qiymati (foydalanuvchi bo'yicha)
SELECT u.first_name,
       SUM(ci.quantity) as total_items,
       SUM(p.price * ci.quantity) as total_value
FROM carts c
JOIN users u ON c.user_id = u.id
LEFT JOIN cart_items ci ON c.id = ci.cart_id
LEFT JOIN products p ON ci.product_id = p.id
WHERE u.id = 1
GROUP BY u.id, u.first_name;

-- Eng barim savatlari (eng ko'p mahsulot)
SELECT c.id, u.first_name,
       COUNT(ci.id) as item_count,
       SUM(p.price * ci.quantity) as total_value
FROM carts c
JOIN users u ON c.user_id = u.id
LEFT JOIN cart_items ci ON c.id = ci.cart_id
LEFT JOIN products p ON ci.product_id = p.id
GROUP BY c.id, u.first_name
ORDER BY item_count DESC;

-- ========================
-- 6. BUYURTMALARGA DOIR SORASHLAR
-- ========================

-- Barcha buyurtmalar (foydalanuvchi bilan)
SELECT o.id, u.first_name, u.last_name,
       o.total_price, o.status, o.created_at,
       o.delivery_address
FROM orders o
JOIN users u ON o.user_id = u.id
ORDER BY o.created_at DESC;

-- Buyurtmalar statusga ko'ra
SELECT status, COUNT(*) as count, SUM(total_price) as total_value
FROM orders
GROUP BY status;

-- Yangi buyurtmalar (tasdiqlanmagan)
SELECT o.id, u.first_name, o.total_price, o.item_count,
       o.created_at, o.delivery_address
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'yangi'
ORDER BY o.created_at DESC;

-- Muayyan buyurtmaning detalyalari
SELECT o.id, o.total_price, o.status,
       oi.product_id, p.name_uz, oi.quantity,
       oi.price_at_purchase,
       (oi.quantity * oi.price_at_purchase) as total
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.id = 1;

-- Foydalanuvchining buyurtmalari
SELECT o.id, o.total_price, o.status, o.item_count,
       o.created_at
FROM orders o
WHERE o.user_id = 1
ORDER BY o.created_at DESC;

-- Oy bo'yicha buyurtmalar soni
SELECT DATE_TRUNC('month', created_at) as month,
       COUNT(*) as order_count,
       SUM(total_price) as monthly_revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;

-- Kun bo'yicha daromad
SELECT DATE(created_at) as date,
       COUNT(*) as order_count,
       SUM(total_price) as daily_revenue
FROM orders
WHERE status != 'bekor_qilingan'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- ========================
-- 7. SHARHLAR VA REYTING
-- ========================

-- Mahsulotning barcha sharhlari
SELECT r.id, u.first_name, r.rating, r.comment,
       r.created_at
FROM reviews r
JOIN users u ON r.user_id = u.id
WHERE r.product_id = 1
ORDER BY r.created_at DESC;

-- O'rtacha reyting (mahsulot bo'yicha)
SELECT p.id, p.name_uz,
       ROUND(AVG(r.rating), 2) as avg_rating,
       COUNT(r.id) as review_count
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id
GROUP BY p.id, p.name_uz
ORDER BY avg_rating DESC;

-- 5 yulduz bergan foydalanuvchilar
SELECT u.first_name, p.name_uz, r.comment
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN products p ON r.product_id = p.id
WHERE r.rating = 5;

-- Eng barim sharhlanmagan mahsulotlar
SELECT p.id, p.name_uz,
       COUNT(r.id) as review_count
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id
GROUP BY p.id, p.name_uz
ORDER BY review_count DESC;

-- Eng ko'p sharh qo'yilgan mahsulotlar
SELECT p.id, p.name_uz,
       COUNT(r.id) as review_count,
       ROUND(AVG(r.rating), 1) as avg_rating
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id
GROUP BY p.id, p.name_uz
ORDER BY review_count DESC
LIMIT 10;

-- ========================
-- 8. TO'LOVLARGA DOIR SORASHLAR
-- ========================

-- Barcha to'lovlar
SELECT p.id, o.id as order_id, u.first_name,
       p.amount, p.payment_method, p.status,
       p.created_at
FROM payments p
JOIN orders o ON p.order_id = o.id
JOIN users u ON p.user_id = u.id
ORDER BY p.created_at DESC;

-- To'landi to'lovlar (tugatilgan)
SELECT p.id, o.id as order_id,
       p.amount, p.payment_method,
       p.transaction_id, p.created_at
FROM payments p
JOIN orders o ON p.order_id = o.id
WHERE p.status = 'to'landi'
ORDER BY p.created_at DESC;

-- Kutilmoqda bo'lgan to'lovlar
SELECT p.id, o.id as order_id, u.first_name,
       p.amount, p.payment_method,
       p.created_at
FROM payments p
JOIN orders o ON p.order_id = o.id
JOIN users u ON p.user_id = u.id
WHERE p.status = 'kutilmoqda'
ORDER BY p.created_at DESC;

-- To'lov usuli bo'yicha statistika
SELECT payment_method,
       COUNT(*) as transaction_count,
       SUM(amount) as total_amount,
       ROUND(AVG(amount), 0) as avg_amount
FROM payments
WHERE status = 'to'landi'
GROUP BY payment_method
ORDER BY total_amount DESC;

-- ========================
-- 9. STATISTIKA VA HISOBLAR VA TAHLIL
-- ========================

-- Jami hisobot
SELECT
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM products) as total_products,
    (SELECT COUNT(*) FROM orders) as total_orders,
    (SELECT SUM(total_price) FROM orders WHERE status != 'bekor_qilindan') as total_revenue,
    (SELECT COUNT(*) FROM orders WHERE status = 'yangi') as pending_orders;

-- Dashboard statistikasi (Python uchun)
SELECT
    DATE(NOW()) as report_date,
    COUNT(DISTINCT o.id) as today_orders,
    SUM(o.total_price) as today_revenue,
    COUNT(DISTINCT o.user_id) as today_customers
FROM orders o
WHERE DATE(o.created_at) = DATE(NOW());

-- Oy bilan solishtirish
SELECT
    'Bu oy' as period,
    COUNT(DISTINCT o.id) as order_count,
    SUM(o.total_price) as revenue,
    ROUND(AVG(o.total_price), 0) as avg_order_value
FROM orders o
WHERE MONTH(o.created_at) = MONTH(NOW())
AND YEAR(o.created_at) = YEAR(NOW())
UNION ALL
SELECT
    'O'tgan oy' as period,
    COUNT(DISTINCT o.id) as order_count,
    SUM(o.total_price) as revenue,
    ROUND(AVG(o.total_price), 0) as avg_order_value
FROM orders o
WHERE MONTH(o.created_at) = MONTH(NOW()) - 1
AND YEAR(o.created_at) = YEAR(NOW());

-- Top 10 foydalanuvchi (daromad bo'yicha)
SELECT
    u.id, u.first_name, u.last_name,
    COUNT(o.id) as purchase_count,
    SUM(o.total_price) as lifetime_value,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id AND o.status != 'bekor_qilingan'
GROUP BY u.id, u.first_name, u.last_name
ORDER BY lifetime_value DESC
LIMIT 10;

-- ========================
-- 10. DATA BOSHQARISH VA O'ZGARTIRISHLAR
-- ========================

-- Mahsulot narxini o'zgartirish
UPDATE products SET price = 4000000 WHERE id = 1;

-- Mahsulot stokini yangilash
UPDATE products SET stock = stock - 5 WHERE id = 1;

-- Mahsulotni faolsizlash
UPDATE products SET is_active = FALSE WHERE price > 10000000;

-- Buyurtma statusini yangilash
UPDATE orders SET status = 'yuborildi' WHERE id = 1;

-- Foydalanuvchi ma'lumotlarini yangilash
UPDATE users
SET first_name = 'Ahmad', last_name = 'Qodirov',
    phone_number = '+998901234567'
WHERE telegram_id = 123456789;

-- Ma'lumotlarni o'chirish (EHTIYOT!)
-- Muayyan buyurtmani o'chirish
DELETE FROM orders WHERE id = 1;

-- Bo'sh savatlarni o'chirish
DELETE FROM carts
WHERE id NOT IN (
    SELECT DISTINCT cart_id FROM cart_items
);

-- Bekor qilingan buyurtmalarni o'chirish (bir kundan ko'proq)
DELETE FROM orders
WHERE status = 'bekor_qilingan'
AND created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- ========================
-- 11. BACKUP VA RESTORE
-- ========================

-- Backup yaratish (Terminal'dan):
-- mysqldump -u root -p shop_db > shop_db_backup.sql

-- Restore qilish (Terminal'dan):
-- mysql -u root -p shop_db < shop_db_backup.sql

-- ========================
-- 12. INDEXLAR VA PERFORMANCE
-- ========================

-- Indexlarni ko'rish
SHOW INDEXES FROM products;
SHOW INDEXES FROM orders;

-- Slow queries'larni tekshirish
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Query ana-liz
EXPLAIN SELECT * FROM products WHERE category_id = 1;
EXPLAIN SELECT * FROM orders WHERE status = 'yangi';

-- ========================
-- TAYYOR! Base baravarib
-- ========================
