"""
Админская консоль для управления магазином
Использование: python admin_console.py
"""

import asyncio
from db.database import AsyncSessionLocal, init_db
from db.repositories import (
    CategoryRepository, ProductRepository, UserRepository,
    OrderRepository
)


async def show_menu():
    print("\n" + "="*50)
    print("🛍️  АДМИНСКА КОНСОЛЬ МАГАЗИНА")
    print("="*50)
    print("1️⃣  Показать все товары")
    print("2️⃣  Показать все категории")
    print("3️⃣  Показать все заказы")
    print("4️⃣  Показать пользователей")
    print("5️⃣  Добавить товар")
    print("6️⃣  Добавить категорию")
    print("7️⃣  Обновить статус заказа")
    print("8️⃣  Удалить товар")
    print("0️⃣  Выход")
    print("="*50)


async def show_products():
    async with AsyncSessionLocal() as session:
        products = await ProductRepository.get_all(session)
        if not products:
            print("❌ Товаров не найдено")
            return
        
        print("\n📦 ТОВАРЫ:")
        print("-" * 80)
        for product in products:
            print(f"ID: {product.id}")
            print(f"  📝 Название: {product.name_uz}")
            print(f"  💰 Цена: {product.price:,.0f} so'm")
            print(f"  📊 Остаток: {product.stock} шт")
            print(f"  ⭐ Продано: {product.sales_count} шт")
            print(f"  📋 Категория ID: {product.category_id}")
            print()


async def show_categories():
    async with AsyncSessionLocal() as session:
        categories = await CategoryRepository.get_all(session)
        if not categories:
            print("❌ Категорий не найдено")
            return
        
        print("\n📚 КАТЕГОРИИ:")
        print("-" * 50)
        for category in categories:
            print(f"ID: {category.id} - {category.name_uz}")
            if category.description:
                print(f"   Описание: {category.description}")
            print()


async def show_orders():
    async with AsyncSessionLocal() as session:
        # Это просто демонстрация, так как нет прямого метода
        print("\n📦 ЗАКАЗЫ:")
        print("-" * 50)
        print("Для просмотра заказов используйте класс OrderRepository")


async def show_users():
    async with AsyncSessionLocal() as session:
        # Просто демонстрация
        print("\n👥 ПОЛЬЗОВАТЕЛИ:")
        print("-" * 50)
        print("Функция просмотра пользователей")


async def add_product():
    name = input("📝 Введите название товара (узбекский): ").strip()
    if not name:
        print("❌ Название не может быть пустым")
        return
    
    try:
        price = float(input("💰 Введите цену: "))
    except ValueError:
        print("❌ Неверная цена")
        return
    
    try:
        category_id = int(input("📂 Введите ID категории: "))
    except ValueError:
        print("❌ Неверный ID категории")
        return
    
    description = input("📋 Описание (пусто для пропуска): ").strip()
    
    try:
        stock = int(input("📊 Остаток (по умолчанию 100): ") or "100")
    except ValueError:
        stock = 100
    
    async with AsyncSessionLocal() as session:
        product = await ProductRepository.create(
            session,
            name_uz=name,
            price=price,
            category_id=category_id,
            description_uz=description if description else None,
            stock=stock
        )
        print(f"✅ Товар добавлен успешно! ID: {product.id}")


async def add_category():
    name = input("📝 Введите название категории (узбекский): ").strip()
    if not name:
        print("❌ Название не может быть пустым")
        return
    
    description = input("📋 Описание (пусто для пропуска): ").strip()
    
    async with AsyncSessionLocal() as session:
        category = await CategoryRepository.create(
            session,
            name_uz=name,
            description=description if description else None
        )
        print(f"✅ Категория добавлена успешно! ID: {category.id}")


async def update_order_status():
    try:
        order_id = int(input("📦 Введите ID заказа: "))
    except ValueError:
        print("❌ Неверный ID")
        return
    
    print("Доступные статусы:")
    print("1. yangi (Новый)")
    print("2. tasdiqlandi (Подтвержден)")
    print("3. yuborildi (Отправлен)")
    print("4. yetkazildi (Доставлен)")
    print("5. bekor qilingan (Отменен)")
    
    status_map = {
        "1": "yangi",
        "2": "tasdiqlandi",
        "3": "yuborildi",
        "4": "yetkazildi",
        "5": "bekor qilingan"
    }
    
    status_choice = input("Выберите статус (1-5): ").strip()
    status = status_map.get(status_choice)
    
    if not status:
        print("❌ Неверный выбор")
        return
    
    async with AsyncSessionLocal() as session:
        order = await OrderRepository.update_status(session, order_id, status)
        if order:
            print(f"✅ Статус заказа обновлен: {status}")
        else:
            print("❌ Заказ не найден")


async def main():
    await init_db()
    
    while True:
        await show_menu()
        choice = input("Выберите опцию: ").strip()
        
        if choice == "1":
            await show_products()
        elif choice == "2":
            await show_categories()
        elif choice == "3":
            await show_orders()
        elif choice == "4":
            await show_users()
        elif choice == "5":
            await add_product()
        elif choice == "6":
            await add_category()
        elif choice == "7":
            await update_order_status()
        elif choice == "0":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор")


if __name__ == "__main__":
    asyncio.run(main())
