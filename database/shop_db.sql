-- 🛍️ SQL ЗАПРОСЫ ДЛЯ СОЗДАНИЯ БАЗЫ ДАННЫХ МАГАЗИНА
-- Для MySQL 8.0+

-- ============ СОЗДАТЬ БАЗУ ДАННЫХ ============
CREATE DATABASE IF NOT EXISTS shop_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE shop_db;

-- ============ ТАБЛИЦА КАТЕГОРИЙ ============
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_uz VARCHAR(100) NOT NULL UNIQUE,
    description LONGTEXT NULL,
    image_url VARCHAR(500) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name_uz)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ ТАБЛИЦА ПРОДУКТОВ ============
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_uz VARCHAR(150) NOT NULL,
    description_uz LONGTEXT NULL,
    price DECIMAL(12, 2) NOT NULL,
    image_url VARCHAR(500) NULL,
    category_id INT NOT NULL,
    stock INT DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    sales_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_category (category_id),
    INDEX idx_price (price),
    INDEX idx_sales (sales_count)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ ============
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    first_name VARCHAR(100) NULL,
    last_name VARCHAR(100) NULL,
    phone_number VARCHAR(20) NULL,
    address LONGTEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_telegram_id (telegram_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ ТАБЛИЦА КОРЗИН ============
CREATE TABLE IF NOT EXISTS carts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ ТАБЛИЦА ТОВАРОВ В КОРЗИНЕ ============
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_cart_id (cart_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ ТАБЛИЦА ЗАКАЗОВ ============
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'yangi',
    item_count INT DEFAULT 0,
    total_price DECIMAL(12, 2) DEFAULT 0.00,
    delivery_address LONGTEXT NULL,
    notes LONGTEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ ТАБЛИЦА ТОВАРОВ В ЗАКАЗЕ ============
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============ ПРИМЕРЫ ДАННЫХ ============

-- Категории
INSERT INTO categories (name_uz, description) VALUES
('📱 Смартфонлар', 'Ҳамма ўхшашди энг уинги смартфонлар'),
('💻 Компютерлар', 'Исчи ва ўйлаш учун ҳалкилар'),
('⌚ Аксессуарлар', 'Телефон ва компютер учун аксессуарлар'),
('🎧 Тўлқунлар', 'Музика уйнаш учун юксак сифатли тўлқунлар'),
('🔌 Батериялар', 'Портатив батериялар ва қўвват жойлари');

-- Товары
INSERT INTO products (name_uz, description_uz, price, category_id, stock, sales_count) VALUES
('iPhone 15 Pro', 'Сўнгги қўлли смартфон ишлаш кучи ва замонавий дизайн', 1200000, 1, 15, 5),
('Samsung Galaxy S24', 'Юксак сифатли камера ва дўмий экран', 900000, 1, 20, 8),
('Xiaomi 14 Ultra', 'Аҳсан нарх-сифат нисбати', 600000, 1, 25, 12),
('MacBook Air M3', 'Қувватли ва енгил компютер', 1500000, 2, 10, 3),
('ASUS ROG Gaming Laptop', 'Ўйинлар учун барқарор ноутбук', 2000000, 2, 8, 2),
('USB-C Кабел', 'Қоватли USB-C кабел', 25000, 3, 100, 45),
('Защитное стекло', 'Телефон экрани учун қўлай', 15000, 3, 150, 60),
('Чехол для телефона', 'Мӯҳовислик ва сўрағандир', 35000, 3, 80, 35),
('AirPods Pro', 'Сим ҳазилача ҳа буғай', 250000, 4, 12, 10),
('Sony WH-1000XM5', 'Юксак сифатли завод наушников', 450000, 4, 18, 6),
('JBL Flip 6', 'Портатив Bluetooth ағирлик', 180000, 4, 22, 14),
('Портативная батарея 10000mAh', 'Тез зарядка ва портатив', 85000, 5, 50, 28),
('Портативная батарея 20000mAh', 'Ишчи 2-3 кун давомида', 150000, 5, 35, 15),
('Быстрая зарядка 65W', 'Ҳайирчилик 30 дақиқада', 120000, 5, 40, 22);

-- ============ SQL ЗАПРОСЫ ЗАВЕРШЕНЫ ============
