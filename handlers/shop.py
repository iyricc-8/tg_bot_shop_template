from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from states.shop_states import ShopStates
from db.database import AsyncSessionLocal
from db.models import CartItem
from db.repositories import (
    CategoryRepository, ProductRepository, CartRepository, UserRepository,
    OrderRepository
)
from keyboards.shop import (
    get_main_menu, get_categories_keyboard, get_products_keyboard,
    get_product_keyboard, get_top_sales_keyboard, get_cart_keyboard,
    get_cart_empty_keyboard, get_checkout_keyboard, get_orders_keyboard,
    get_empty_orders_keyboard, get_account_keyboard, get_cancel_keyboard,
    get_user_data_keyboard
)
from services.invoice_generator import generate_invoice

router = Router()


# ============ ГЛАВНОЕ МЕНЮ ============


@router.message(F.text == "🛍️ Магазин")
async def shop_menu(message: Message, state: FSMContext):
    """Магазин - выбор категории"""
    async with AsyncSessionLocal() as session:
        categories = await CategoryRepository.get_all(session)
    
    if not categories:
        await message.answer("❌ Нет доступных категорий")
        return
    
    keyboard = get_categories_keyboard(categories)
    await message.answer("📚 Выберите категорию:", reply_markup=keyboard)
    await state.set_state(ShopStates.viewing_categories)


# ============ КАТЕГОРИИ И ТОВАРЫ ============


@router.callback_query(F.data.startswith("cat_"))
async def category_products(callback: CallbackQuery, state: FSMContext):
    """Показать товары в категории"""
    category_id = int(callback.data.split("_")[1])
    
    async with AsyncSessionLocal() as session:
        category = await CategoryRepository.get_by_id(session, category_id)
        products = await ProductRepository.get_by_category(session, category_id)
    
    if not products:
        await callback.answer("❌ В этой категории нет товаров", show_alert=True)
        return
    
    text = f"📦 <b>{category.name_uz}</b>\n"
    if category.description:
        text += f"ℹ️ {category.description}\n\n"
    text += f"Найдено товаров: {len(products)}\n"
    text += "Выберите товар для просмотра:"
    
    keyboard = get_products_keyboard(products, category_id)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(ShopStates.viewing_products)
    await callback.answer()


@router.callback_query(F.data == "cat_list")
async def back_to_categories(callback: CallbackQuery, state: FSMContext):
    """Вернуться к категориям"""
    async with AsyncSessionLocal() as session:
        categories = await CategoryRepository.get_all(session)
    
    keyboard = get_categories_keyboard(categories)
    await callback.message.edit_text("📚 Выберите категорию:", reply_markup=keyboard)
    await state.set_state(ShopStates.viewing_categories)
    await callback.answer()


@router.callback_query(F.data.startswith("prod_"))
async def view_product(callback: CallbackQuery, state: FSMContext):
    """Просмотр товара"""
    product_id = int(callback.data.split("_")[1])
    
    async with AsyncSessionLocal() as session:
        product = await ProductRepository.get_by_id(session, product_id)
    
    if not product:
        await callback.answer("❌ Товар не найден", show_alert=True)
        return
    
    text = f"📦 <b>{product.name_uz}</b>\n\n"
    text += f"💰 Цена: <b>{product.price:,.0f} so'm</b>\n"
    text += f"📊 Свободно: <b>{product.stock} шт</b>\n"
    text += f"⭐ Продано: <b>{product.sales_count} шт</b>\n\n"
    if product.description_uz:
        text += f"📝 {product.description_uz}\n\n"
    
    if product.image_url:
        try:
            await callback.message.delete()
            await callback.message.chat.send_photo(
                photo=product.image_url,
                caption=text,
                reply_markup=get_product_keyboard(product_id),
                parse_mode="HTML"
            )
            await state.update_data(last_product_id=product_id)
            await state.set_state(ShopStates.viewing_product)
            return
        except:
            pass
    
    await callback.message.edit_text(text, reply_markup=get_product_keyboard(product_id), parse_mode="HTML")
    await state.update_data(last_product_id=product_id)
    await state.set_state(ShopStates.viewing_product)
    await callback.answer()


# ============ ДОБАВЛЕНИЕ В КОРЗИНУ ============


@router.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    """Добавить товар в корзину"""
    parts = callback.data.split("_")
    quantity = int(parts[1])
    product_id = int(parts[2])
    
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(session, callback.from_user.id, callback.from_user.first_name)
        product = await ProductRepository.get_by_id(session, product_id)
        
        if product.stock < quantity:
            await callback.answer(f"❌ Недостаточно товара (доступно: {product.stock})", show_alert=True)
            return
        
        await CartRepository.add_item(session, user.id, product_id, quantity)
    
    await callback.answer(f"✅ {product.name_uz} добавлено в корзину ({quantity} шт)", show_alert=False)


@router.callback_query(F.data.startswith("add_cart_"))
async def add_to_cart_one(callback: CallbackQuery, state: FSMContext):
    """Добавить 1 товар в корзину"""
    product_id = int(callback.data.split("_")[2])
    
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(session, callback.from_user.id, callback.from_user.first_name)
        product = await ProductRepository.get_by_id(session, product_id)
        
        if product.stock < 1:
            await callback.answer("❌ Товар закончился", show_alert=True)
            return
        
        await CartRepository.add_item(session, user.id, product_id, 1)
    
    await callback.answer(f"✅ {product.name_uz} добавлено в корзину", show_alert=False)


@router.callback_query(F.data == "back_to_products")
async def back_to_products(callback: CallbackQuery, state: FSMContext):
    """Вернуться к товарам"""
    data = await state.get_data()
    last_product_id = data.get("last_product_id")
    
    if last_product_id:
        async with AsyncSessionLocal() as session:
            product = await ProductRepository.get_by_id(session, last_product_id)
            category_id = product.category_id
            products = await ProductRepository.get_by_category(session, category_id)
        
        keyboard = get_products_keyboard(products, category_id)
        async with AsyncSessionLocal() as session:
            category = await CategoryRepository.get_by_id(session, category_id)
            text = f"📦 <b>{category.name_uz}</b>\nВыберите товар:"
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    
    await callback.answer()


# ============ ТОП ПРОДАЖИ ============


@router.message(F.text == "🔥 Топ продажи")
async def top_sales(message: Message, state: FSMContext):
    """Показать топ продажи"""
    async with AsyncSessionLocal() as session:
        products = await ProductRepository.get_top_sales(session, limit=10)
    
    if not products:
        await message.answer("❌ Нет товаров в топе продаж")
        return
    
    text = "🔥 <b>ТОП ПРОДАЖИ</b>\n\n"
    text += "Самые популярные товары:\n"
    
    keyboard = get_top_sales_keyboard(products)
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(ShopStates.browsing_top_sales)


# ============ КОРЗИНА ============


@router.message(F.text == "🛒 Корзина")
async def view_cart(message: Message, state: FSMContext):
    """Показать корзину"""
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(session, message.from_user.id, message.from_user.first_name)
        cart = await CartRepository.get_with_items(session, user.id)
        
        # Убедиться, что товары загружены
        cart_result = await session.execute(
            select(CartItem).where(CartItem.cart_id == cart.id)
        )
        cart_items = cart_result.scalars().all()
    
    if not cart_items:
        await message.answer(
            "🛒 Ваша корзина пуста",
            reply_markup=get_cart_empty_keyboard()
        )
        return
    
    text = "🛒 <b>ВАША КОРЗИНА</b>\n\n"
    total = 0
    for idx, item in enumerate(cart_items, 1):
        # Подгрузить товар если не загружен
        if not item.product:
            async with AsyncSessionLocal() as s:
                item.product = await ProductRepository.get_by_id(s, item.product_id)
        
        item_total = item.product.price * item.quantity
        total += item_total
        text += f"{idx}. {item.product.name_uz}\n"
        text += f"   Цена: {item.product.price:,.0f} so'm × {item.quantity} шт = {item_total:,.0f} so'm\n\n"
    
    text += f"<b>━━━━━━━━━━━━━━</b>\n"
    text += f"<b>💰 ИТОГО: {total:,.0f} so'm</b>\n"
    text += f"📦 Товаров: {sum(item.quantity for item in cart_items)} шт\n"
    
    keyboard = get_cart_keyboard(cart_items)
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(ShopStates.in_cart)


# ============ РЕДАКТИРОВАНИЕ КОРЗИНЫ ============


@router.callback_query(F.data.startswith("del_cart_"))
async def delete_from_cart(callback: CallbackQuery, state: FSMContext):
    """Удалить товар из корзины"""
    cart_item_id = int(callback.data.split("_")[2])
    
    async with AsyncSessionLocal() as session:
        await CartRepository.remove_item(session, cart_item_id)
        user = await UserRepository.get_or_create(session, callback.from_user.id)
        cart = await CartRepository.get_with_items(session, user.id)
    
    if not cart.items:
        await callback.message.edit_text(
            "🛒 Ваша корзина пуста",
            reply_markup=get_cart_empty_keyboard()
        )
        await callback.answer("✅ Товар удален из корзины")
        return
    
    text = "🛒 <b>ВАША КОРЗИНА</b>\n\n"
    total = 0
    for idx, item in enumerate(cart.items, 1):
        item_total = item.product.price * item.quantity
        total += item_total
        text += f"{idx}. {item.product.name_uz}\n"
        text += f"   Цена: {item.product.price:,.0f} so'm × {item.quantity} шт = {item_total:,.0f} so'm\n\n"
    
    text += f"<b>━━━━━━━━━━━━━━</b>\n"
    text += f"<b>💰 ИТОГО: {total:,.0f} so'm</b>\n"
    
    keyboard = get_cart_keyboard(cart.items)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer("✅ Товар удален из корзины")


@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery, state: FSMContext):
    """Очистить корзину"""
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(session, callback.from_user.id)
        await CartRepository.clear(session, user.id)
    
    await callback.message.edit_text(
        "🛒 Ваша корзина пуста",
        reply_markup=get_cart_empty_keyboard()
    )
    await callback.answer("✅ Корзина очищена", show_alert=False)


# ============ ОФОРМЛЕНИЕ ЗАКАЗА ============


@router.callback_query(F.data == "checkout")
async def checkout_start(callback: CallbackQuery, state: FSMContext):
    """Начать оформление заказа"""
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(session, callback.from_user.id)
        cart = await CartRepository.get_with_items(session, user.id)
    
    if not cart.items:
        await callback.answer("❌ Корзина пуста!", show_alert=True)
        return
    
    text = "📝 <b>ОФОРМЛЕНИЕ ЗАКАЗА</b>\n\n"
    text += "Введите ваше имя:"
    
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(ShopStates.entering_first_name)
    await state.update_data(checkout_data={})
    await callback.answer()


@router.message(ShopStates.entering_first_name)
async def receive_first_name(message: Message, state: FSMContext):
    """Получить имя"""
    if len(message.text) > 50:
        await message.answer("❌ Имя слишком длинное (максимум 50 символов)")
        return
    
    data = await state.get_data()
    checkout_data = data.get("checkout_data", {})
    checkout_data["first_name"] = message.text
    
    await state.update_data(checkout_data=checkout_data)
    await message.answer("📝 Введите вашу фамилию:")
    await state.set_state(ShopStates.entering_last_name)


@router.message(ShopStates.entering_last_name)
async def receive_last_name(message: Message, state: FSMContext):
    """Получить фамилию"""
    if len(message.text) > 50:
        await message.answer("❌ Фамилия слишком длинная (максимум 50 символов)")
        return
    
    data = await state.get_data()
    checkout_data = data.get("checkout_data", {})
    checkout_data["last_name"] = message.text
    
    await state.update_data(checkout_data=checkout_data)
    await message.answer("📱 Введите ваш номер телефона (например: +998901234567):")
    await state.set_state(ShopStates.entering_phone)


@router.message(ShopStates.entering_phone)
async def receive_phone(message: Message, state: FSMContext):
    """Получить номер телефона"""
    phone = message.text.replace(" ", "").replace("-", "")
    
    if len(phone) < 10:
        await message.answer("❌ Неверный номер телефона")
        return
    
    data = await state.get_data()
    checkout_data = data.get("checkout_data", {})
    checkout_data["phone_number"] = phone
    
    await state.update_data(checkout_data=checkout_data)
    await message.answer("📍 Введите адрес доставки:")
    await state.set_state(ShopStates.entering_address)


@router.message(ShopStates.entering_address)
async def receive_address(message: Message, state: FSMContext):
    """Получить адрес"""
    if len(message.text) > 500:
        await message.answer("❌ Адрес слишком длинный (максимум 500 символов)")
        return
    
    data = await state.get_data()
    checkout_data = data.get("checkout_data", {})
    checkout_data["address"] = message.text
    
    await state.update_data(checkout_data=checkout_data)
    
    # Показать обзор заказа
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(session, message.from_user.id)
        cart = await CartRepository.get_with_items(session, user.id)
    
    total = sum(item.product.price * item.quantity for item in cart.items)
    
    text = "📋 <b>ПОДТВЕРЖДЕНИЕ ЗАКАЗА</b>\n\n"
    text += f"<b>👤 Информация тронбери:</b>\n"
    text += f"Имя: {checkout_data['first_name']}\n"
    text += f"Фамилия: {checkout_data['last_name']}\n"
    text += f"Телефон: {checkout_data['phone_number']}\n"
    text += f"Адрес: {checkout_data['address']}\n\n"
    text += f"<b>📦 Товары:</b>\n"
    for item in cart.items:
        text += f"• {item.product.name_uz} × {item.quantity} = {item.product.price * item.quantity:,.0f} so'm\n"
    text += f"\n<b>💰 ИТОГО: {total:,.0f} so'm</b>\n"
    
    keyboard = get_checkout_keyboard()
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(ShopStates.reviewing_order)


@router.callback_query(F.data == "confirm_order", ShopStates.reviewing_order)
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    """Подтвердить заказ"""
    data = await state.get_data()
    checkout_data = data.get("checkout_data", {})
    
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(
            session,
            callback.from_user.id,
            checkout_data.get("first_name")
        )
        
        # Обновить данные пользователя
        await UserRepository.update(
            session,
            callback.from_user.id,
            first_name=checkout_data.get("first_name"),
            last_name=checkout_data.get("last_name"),
            phone_number=checkout_data.get("phone_number"),
            address=checkout_data.get("address")
        )
        
        # Получить корзину
        cart = await CartRepository.get_with_items(session, user.id)
        
        # Создать заказ
        order = await OrderRepository.create(
            session,
            user.id,
            delivery_address=checkout_data.get("address"),
            notes=f"Телефон: {checkout_data.get('phone_number')}"
        )
        
        # Добавить товары в заказ
        for item in cart.items:
            await OrderRepository.add_item(
                session,
                order.id,
                item.product_id,
                item.quantity,
                item.product.price
            )
            
            # Обновить остаток и продажи
            await ProductRepository.update_stock(session, item.product_id, item.quantity)
            await ProductRepository.increase_sales(session, item.product_id, item.quantity)
        
        # Очистить корзину
        await CartRepository.clear(session, user.id)
    
    # Выбрать рубль и ОФОРМИТЬ заказ
    await callback.message.edit_text(
        "✅ <b>ЗАКАЗ УСПШНО ПРИНЯТ!</b>\n\n"
        f"📦 Номер заказа: <b>#{order.id}</b>\n"
        f"💰 Сумма: <b>{order.total_price:,.0f} so'm</b>\n\n"
        "Спасибо за покупку! Мы свяжемся с вами в ближайшее время.",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    
    # Генерировать и отправить чек
    invoice_text = generate_invoice(
        order_id=order.id,
        first_name=checkout_data.get("first_name"),
        last_name=checkout_data.get("last_name"),
        phone=checkout_data.get("phone_number"),
        address=checkout_data.get("address"),
        total=order.total_price,
        items=[(item.product.name_uz, item.quantity, item.product.price) for item in cart.items]
    )
    
    await callback.message.answer(invoice_text, parse_mode="HTML")
    
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "cancel_checkout")
async def cancel_checkout(callback: CallbackQuery, state: FSMContext):
    """Отмена оформления"""
    await callback.message.edit_text(
        "❌ Заказ отменен",
        reply_markup=get_main_menu()
    )
    await state.clear()
    await callback.answer()


# ============ МОИ ЗАКАЗЫ ============


@router.message(F.text == "📦 Мои заказы")
async def my_orders(message: Message, state: FSMContext):
    """Мои заказы"""
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(session, message.from_user.id, message.from_user.first_name)
        orders = await OrderRepository.get_user_orders(session, user.id)
    
    if not orders:
        await message.answer(
            "📦 У вас еще нет заказов",
            reply_markup=get_empty_orders_keyboard()
        )
        return
    
    keyboard = get_orders_keyboard(orders)
    text = "📦 <b>МОИ ЗАКАЗЫ</b>\n\nВыберите заказ для просмотра:"
    
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(ShopStates.viewing_orders)


@router.callback_query(F.data.startswith("order_"))
async def view_order_details(callback: CallbackQuery, state: FSMContext):
    """Просмотр деталей заказа"""
    order_id = int(callback.data.split("_")[1])
    
    async with AsyncSessionLocal() as session:
        order = await OrderRepository.get_with_items(session, order_id)
    
    if not order:
        await callback.answer("❌ Заказ не найден", show_alert=True)
        return
    
    status_labels = {
        "yangi": "Янги",
        "tasdiqlandi": "Тасдиқланди",
        "yuborildi": "Юборилди",
        "yetkazildi": "Етказилди",
        "bekor qilingan": "Бекор қилинган"
    }
    
    text = f"📦 <b>ЗАКАЗ #{order.id}</b>\n\n"
    text += f"📊 Статус: {status_labels.get(order.status, order.status)}\n"
    text += f"📅 Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
    text += f"<b>📝 ТОВАРЫ:</b>\n"
    
    for item in order.items:
        text += f"• {item.product.name_uz} × {item.quantity} = {item.price_at_purchase * item.quantity:,.0f} so'm\n"
    
    text += f"\n<b>💰 ИТОГО: {order.total_price:,.0f} so'm</b>\n\n"
    text += f"📍 Адрес доставки:\n{order.delivery_address}\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Орқага", callback_data="back_to_orders")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "back_to_orders")
async def back_to_orders(callback: CallbackQuery, state: FSMContext):
    """Вернуться к заказам"""
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(session, callback.from_user.id)
        orders = await OrderRepository.get_user_orders(session, user.id)
    
    if not orders:
        keyboard = get_empty_orders_keyboard()
        text = "📦 У вас еще нет заказов"
    else:
        keyboard = get_orders_keyboard(orders)
        text = "📦 <b>МОИ ЗАКАЗЫ</b>\n\nВыберите заказ для просмотра:"
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


# ============ АККАУНТ ============


@router.message(F.text == "👤 Аккаунт")
async def view_account(message: Message, state: FSMContext):
    """Просмотр аккаунта"""
    async with AsyncSessionLocal() as session:
        user = await UserRepository.get_or_create(session, message.from_user.id, message.from_user.first_name)
    
    text = "<b>👤 МОЙ АККАУНТ</b>\n\n"
    text += f"Имя: {user.first_name or 'Не указано'}\n"
    text += f"Фамилия: {user.last_name or 'Не указано'}\n"
    text += f"Телефон: {user.phone_number or 'Не указано'}\n"
    text += f"Адрес: {user.address or 'Не указано'}\n"
    
    keyboard = get_account_keyboard()
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(ShopStates.viewing_account)


# ============ ВЕРНУТЬСЯ В МЕНЮ ============


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Вернуться в главное меню"""
    await callback.message.edit_text(
        "🏠 <b>ГЛАВНОЕ МЕНЮ</b>",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await state.clear()
    await callback.answer()


@router.message(F.text == "/start")
async def start_command(message: Message, state: FSMContext):
    """Команда /start"""
    await message.answer(
        "🏠 <b>ГЛАВНОЕ МЕНЮ</b>",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await state.clear()
