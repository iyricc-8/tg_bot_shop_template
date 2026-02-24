"""
Скрипт инициализации БД с примерами товаров
Запустить: python init_shop_db.py
"""

import asyncio
from db.database import AsyncSessionLocal, init_db
from db.repositories import CategoryRepository, ProductRepository


async def init_shop_data():
    """Инициализировать БД с примерами товаров"""
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Проверим, есть ли уже данные
        existing_categories = await CategoryRepository.get_all(session)
        if existing_categories:
            print("✅ БД уже инициализирована!")
            return
        
        # Создать категории
        categories_data = [
            {
                "name_uz": "📱 Смартфонлар",
                "description": "Ҳамма ўхшашди энг уинги смартфонлар"
            },
            {
                "name_uz": "💻 Компютерлар",
                "description": "Исчи ва ўйлаш учун ҳалкилар"
            },
            {
                "name_uz": "⌚ Аксессуарлар",
                "description": "Телефон ва компютер учун аксессуарлар"
            },
            {
                "name_uz": "🎧 Тўлқунлар",
                "description": "Музика уйнаш учун юксак сифатли тўлқунлар"
            },
            {
                "name_uz": "🔌 Батериялар",
                "description": "Портатив батериялар ва қўвват жойлари"
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category = await CategoryRepository.create(
                session,
                cat_data["name_uz"],
                cat_data["description"]
            )
            categories.append(category)
            print(f"✅ Категория создана: {category.name_uz}")
        
        # Создать товары
        products_data = [
            # Смартфоны
            {
                "category": 0,
                "name_uz": "iPhone 15 Pro",
                "price": 1200000,
                "description_uz": "Сўнгги қўлли смартфон ишлаш кучи ва замонавий дизайн",
                "stock": 15
            },
            {
                "category": 0,
                "name_uz": "Samsung Galaxy S24",
                "price": 900000,
                "description_uz": "Юксак сифатли камера ва дўмий экран",
                "stock": 20
            },
            {
                "category": 0,
                "name_uz": "Xiaomi 14 Ultra",
                "price": 600000,
                "description_uz": "Аҳсан нарх-сифат нисбати",
                "stock": 25
            },
            {
                "category": 0,
                "name_uz": "OnePlus 12",
                "price": 750000,
                "description_uz": "Ишчи, зуҳур ва қўвватли батарея",
                "stock": 18
            },
            {
                "category": 0,
                "name_uz": "Google Pixel 8 Pro",
                "price": 1100000,
                "description_uz": "Энг яхши AI камерали смартфон",
                "stock": 12
            },
            
            # Компютеры
            {
                "category": 1,
                "name_uz": "MacBook Air M3",
                "price": 1500000,
                "description_uz": "Қувватли ва енгил компютер",
                "stock": 10
            },
            {
                "category": 1,
                "name_uz": "ASUS ROG Gaming Laptop",
                "price": 2000000,
                "description_uz": "Ўйинлар учун барқарор ноутбук",
                "stock": 8
            },
            {
                "category": 1,
                "name_uz": "Dell XPS 15",
                "price": 1800000,
                "description_uz": "Креативларга мўқими компютер",
                "stock": 6
            },
            
            # Аксессуары
            {
                "category": 2,
                "name_uz": "USB-C Кабел",
                "price": 25000,
                "description_uz": "Қоватли USB-C кабел",
                "stock": 100
            },
            {
                "category": 2,
                "name_uz": "Защитное стекло",
                "price": 15000,
                "description_uz": "Телефон экрани учун қўлай",
                "stock": 150
            },
            {
                "category": 2,
                "name_uz": "Чехол для телефона",
                "price": 35000,
                "description_uz": "Мӯҳовислик ва сўрағандир",
                "stock": 80
            },
            {
                "category": 2,
                "name_uz": "Беспроводное зарядное устройство",
                "price": 45000,
                "description_uz": "Қўлай ва тез сим зарядлаш",
                "stock": 30
            },
            
            # Наушники
            {
                "category": 3,
                "name_uz": "AirPods Pro",
                "price": 250000,
                "description_uz": "Сим ҳазилача ҳа буғай",
                "stock": 12
            },
            {
                "category": 3,
                "name_uz": "Sony WH-1000XM5",
                "price": 450000,
                "description_uz": "Юксак сифатли завод наушников",
                "stock": 18
            },
            {
                "category": 3,
                "name_uz": "JBL Flip 6",
                "price": 180000,
                "description_uz": "Портатив Bluetooth ағирлик",
                "stock": 22
            },
            {
                "category": 3,
                "name_uz": "Beats Studio Pro",
                "price": 320000,
                "description_uz": "Профессионал оддийо ва комфорт",
                "stock": 10
            },
            
            # Батареи
            {
                "category": 4,
                "name_uz": "Портативная батарея 10000mAh",
                "price": 85000,
                "description_uz": "Тез зарядка ва портатив",
                "stock": 50
            },
            {
                "category": 4,
                "name_uz": "Портативная батарея 20000mAh",
                "price": 150000,
                "description_uz": "Ишчи 2-3 кун давомида",
                "stock": 35
            },
            {
                "category": 4,
                "name_uz": "Быстрая зарядка 65W",
                "price": 120000,
                "description_uz": "Ҳайирчилик 30 дақиқада",
                "stock": 40
            },
            {
                "category": 4,
                "name_uz": "Портативная батарея 30000mAh",
                "price": 220000,
                "description_uz": "Соат ишчи давомида электр жой",
                "stock": 15
            }
        ]
        
        for prod_data in products_data:
            product = await ProductRepository.create(
                session,
                name_uz=prod_data["name_uz"],
                price=prod_data["price"],
                category_id=categories[prod_data["category"]].id,
                description_uz=prod_data["description_uz"],
                stock=prod_data["stock"]
            )
            print(f"✅ Товар создан: {product.name_uz} ({product.price:,.0f} so'm)")
        
        print("\n✅ БД инициализирована успешно!")
        print(f"✅ Создано категорий: {len(categories)}")
        print(f"✅ Создано товаров: {len(products_data)}")


if __name__ == "__main__":
    asyncio.run(init_shop_data())
