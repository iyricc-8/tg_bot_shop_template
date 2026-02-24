-- Telegram Bot Online Shop Database
-- Encoding: UTF-8
-- Language: Uzbek (Latin)

-- ========================
-- 1. KATEGORIYALAR (CATEGORIES)
-- ========================
CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name_uz VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name_uz (name_uz)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================
-- 2. MAHSULOTLAR (PRODUCTS)
-- ========================
CREATE TABLE IF NOT EXISTS products (
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
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_category_id (category_id),
    INDEX idx_is_active (is_active),
    INDEX idx_sales_count (sales_count)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================
-- 3. FOYDALANUVCHILAR (USERS)
-- ========================
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    telegram_id BIGINT UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_telegram_id (telegram_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================
-- 4. SAVAT (CART)
-- ========================
CREATE TABLE IF NOT EXISTS carts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================
-- 5. SAVAT MAHSULOTLARI (CART ITEMS)
-- ========================
CREATE TABLE IF NOT EXISTS cart_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_cart_id (cart_id),
    INDEX idx_product_id (product_id),
    UNIQUE KEY unique_cart_product (cart_id, product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================
-- 6. BUYURTMALAR (ORDERS)
-- ========================
CREATE TABLE IF NOT EXISTS orders (
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
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================
-- 7. BUYURTMA MAHSULOTLARI (ORDER ITEMS)
-- ========================
CREATE TABLE IF NOT EXISTS order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================
-- 8. SHARHLAR (REVIEWS)
-- ========================
CREATE TABLE IF NOT EXISTS reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    -- Rating: 1-5 yulduzlar
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_user_id (user_id),
    INDEX idx_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================
-- 9. TO'LOVLAR (PAYMENTS)
-- ========================
CREATE TABLE IF NOT EXISTS payments (
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
    INDEX idx_order_id (order_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========================
-- 10. TEST MA'LUMOTLARNI KIRITISH
-- ========================

-- Kategoriyalar bilan toldirish
INSERT INTO categories (name_uz, description, image_url) VALUES
('Elektronika', 'Zamonaviy elektronik mahsulotlar', 'https://example.com/electronics.jpg'),
('Kiyim-kechak', 'Erkak va ayol kiyim-kechagi', 'https://example.com/clothes.jpg'),
('Ovqat-ichimlik', 'Sog''a va mazali ovqat-ichimliklar', 'https://example.com/food.jpg'),
('Kitoblar', 'Butun dunyoning mashhur kitoblari', 'https://example.com/books.jpg'),
('Sport uskunasi', 'Sport va fitness uchun vosita-uskunalar', 'https://example.com/sports.jpg');

-- Mahsulotlar bilan toldirish
INSERT INTO products (name_uz, description_uz, price, image_url, category_id, stock, sales_count) VALUES
-- Elektronika
('Samsung Galaxy A14', 'Yuqori sifatli smartphone, 128GB xotira', 3500000, 'https://example.com/samsung.jpg', 1, 50, 25),
('Xiaomi Redmi Note 12', 'Juda yaxshi kamera va batareya', 2800000, 'https://example.com/xiaomi.jpg', 1, 40, 35),
('Apple AirPods Pro', 'Wireless quloqchin, shovqin bilan togri kelishi', 5200000, 'https://example.com/airpods.jpg', 1, 30, 20),

-- Kiyim-kechak
('Erkak futbolkasi (L)', 'Shutirintage 100% paxta, qo''ng''ir rang', 450000, 'https://example.com/tshirt.jpg', 2, 100, 45),
('Ayol jeansi (M)', 'Klassik ko''k rang jeans', 650000, 'https://example.com/jeans.jpg', 2, 80, 60),
('Quyosh shlyapasi', 'Yozda surgun uchun qulay shlyapa', 120000, 'https://example.com/hat.jpg', 2, 200, 100),

-- Ovqat-ichimlik
('Shokolad (100g)', 'Belgiyada ishlab chiqarilgan damli shokolad', 35000, 'https://example.com/chocolate.jpg', 3, 300, 150),
('Qahva (250g)', 'Ekvador'dan keltirgan premium qahva', 85000, 'https://example.com/coffee.jpg', 3, 150, 80),
('Apelsin sharbati (1L)', 'Tabiiy ingradientlardan tayyorlangan', 28000, 'https://example.com/juice.jpg', 3, 200, 120),

-- Kitoblar
('Otaboyning oʻtgan kunlari', 'Abdulla Qodirining mashhur romani', 42000, 'https://example.com/book1.jpg', 4, 60, 30),
('Shayx Usmon - Kimyogar', 'Ilmiiy fantastika asari', 38000, 'https://example.com/book2.jpg', 4, 45, 25),
('Alisher Navoiy asarlari', 'Klassik o''zbek adabiyoti', 55000, 'https://example.com/book3.jpg', 4, 70, 50),

-- Sport
('Yoga mat (173cm)', 'Shammu va ekologik mat', 165000, 'https://example.com/yoga.jpg', 5, 40, 22),
('Dumbbell (5kg)', 'Shundlik dumbbell, paxta bilan tutqichlar', 125000, 'https://example.com/dumbbell.jpg', 5, 100, 55);

-- ========================
-- 11. INDEKSLARNI TEKSHIRISH
-- ========================
CREATE INDEX idx_products_name_uz ON products(name_uz);
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_payments_status ON payments(status);

-- ========================
-- 12. STAT JADVALINI YUKLAMASI UCHUN QULOQLASH
-- ========================
DELIMITER $$

-- Mahsulot sotilganda sales_count yangilash
CREATE TRIGGER update_product_sales_after_order 
AFTER INSERT ON order_items 
FOR EACH ROW 
BEGIN
    UPDATE products SET sales_count = sales_count + NEW.quantity WHERE id = NEW.product_id;
END$$

-- Sharah qo'shilganda mahsulotning reyting kalkulyatori
CREATE TRIGGER update_product_after_review 
AFTER INSERT ON reviews 
FOR EACH ROW 
BEGIN
    UPDATE products SET popularity = popularity + 1 WHERE id = NEW.product_id;
END$$

DELIMITER ;

-- ========================
-- TEST FOYDALANUVCHILAR
-- ========================
INSERT INTO users (telegram_id, first_name, last_name, phone_number, address) VALUES
(123456789, 'Ahmad', 'Qodirov', '+998901234567', 'Tashkent, Yunusabad tumani, 1-ko''cha'),
(987654321, 'Sevara', 'Hasanova', '+998901234568', 'Tashkent, Shayxontohur tumani, A-ko''cha'),
(555777999, 'Mirjahon', 'Yusupov', '+998909876543', 'Tashkent, Mirzo Ulugbek tumani');

-- ========================
-- SHUNGA QARAB SAVAT VA BUYURTMA SHABLONINI YARATISH
-- ========================
-- Test savati (qayd: bu faqat misol, avtomatshe yaratiladi)
-- INSERT INTO carts (user_id) SELECT id FROM users WHERE telegram_id = 123456789;

-- ========================
-- MALUMOT ORQALI SORASH MISOLLARI
-- ========================
-- Eng ko'p sotilgan mahsulotlarni ko'rish:
-- SELECT name_uz, price, sales_count FROM products ORDER BY sales_count DESC LIMIT 10;

-- Muayyan kategoriyaning mahsulotlari:
-- SELECT name_uz, price, stock FROM products WHERE category_id = 1 AND is_active = TRUE;

-- Foydalanuvchining buyurtmalari:
-- SELECT o.id, o.status, o.total_price, o.created_at FROM orders o WHERE o.user_id = 1;

-- ========================
-- JADVALLARNI RO'YXATI
-- ========================
-- SHOW TABLES;

-- ========================
-- DATABASE STATS
-- ========================
-- Jami mahsulotlar soni: SELECT COUNT(*) as total_products FROM products;
-- Jami buyurtmalar soni: SELECT COUNT(*) as total_orders FROM orders;
-- Jami foydalanuvchilar: SELECT COUNT(*) as total_users FROM users;
