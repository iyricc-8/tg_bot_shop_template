"""
Shop Handler - Magasin asosiy logikasi
Uzbekcha: Barcha savdoning funksiyalari
"""

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.shop_keyboards import (
    get_main_menu_kb, get_categories_kb, get_products_kb,
    get_product_detail_kb, get_cart_kb, get_quantity_kb,
    get_checkout_kb, get_payment_method_kb, get_order_confirmation_kb,
    get_orders_kb, get_top_sales_kb, get_profile_kb, get_admin_kb,
    get_yes_no_kb, create_quantity_buttons
)
from states.shop_states import ShopStates
from services.db_api.shop_services import (
    CategoryService, ProductService, UserService, CartService,
    OrderService, ReviewService, PaymentService, StatisticsService
)
from db.database import AsyncSessionLocal

router = Router()


# ========================
# ASOSIY MENYU
# ========================

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Bot boshlash"""
    async with AsyncSessionLocal() as session:
        # Foydalanuvchi yaratish
        user = await UserService.get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.first_name
        )
    
    await state.clear()
    await message.answer(
        f"👋 Assalamu alaikum, {message.from_user.first_name}!\n\n"
        "🛍️ Online do'konimizga xush kelibsiz!\n"
        "Mahsulotlar ko'rish va xarid qilishni boshlang.",
        reply_markup=get_main_menu_kb()
    )


@router.message(F.text == "🛍️ Do'konga kirish")
async def shop_menu(message: Message, state: FSMContext):
    """Do'kon menyu"""
    async with AsyncSessionLocal() as session:
        categories = await CategoryService.get_all_categories(session)
    
    if not categories:
        await message.answer("Hozircha kategoriyalar mavjud emas.")
        return
    
    await state.set_state(ShopStates.viewing_categories)
    await message.answer(
        "📂 Kategoriyalarni tanlang:",
        reply_markup=get_categories_kb(categories)
    )


@router.message(F.text == "⭐ Eng ko'p sotilganlar")
async def top_sales(message: Message, state: FSMContext):
    """Eng ko'p sotilgan mahsulotlar"""
    async with AsyncSessionLocal() as session:
        products = await ProductService.get_top_products(session)
    
    if not products:
        await message.answer("Hozircha sotilgan mahsulotlar yo'q.")
        return
    
    await state.set_state(ShopStates.browsing_top_sales)
    
    text = "🔥 <b>ENG KO'P SOTILGAN MAHSULOTLAR:</b>\n\n"
    for i, product in enumerate(products[:10], 1):
        text += f"{i}. {product.name_uz}\n"
        text += f"   💰 {product.price:,.0f} so'm\n"
        text += f"   📊 {product.sales_count} ta sotilgan\n\n"
    
    await message.answer(
        text,
        reply_markup=get_top_sales_kb(products),
        parse_mode="HTML"
    )


# ========================
# KATEGORIYA VA MAHSULOTLAR
# ========================

@router.callback_query(F.data.startswith("category_"))
async def view_category_products(callback: CallbackQuery, state: FSMContext):
    """Kategoriya mahsulotlarini ko'rish"""
    category_id = int(callback.data.split("_")[1])
    
    async with AsyncSessionLocal() as session:
        category = await CategoryService.get_category_by_id(session, category_id)
        products = await ProductService.get_products_by_category(session, category_id)
        
        # Загружаем данные внутри контекста
        if not products:
            await callback.answer("Bu kategoriyada mahsulotlar yo'q.", show_alert=True)
            return
        
        category_name = category.name_uz
        products_data = [(p.name_uz, p.price, p.stock, p.id) for p in products]
    
    await state.set_state(ShopStates.viewing_products)
    await state.update_data(category_id=category_id)
    
    text = f"📂 <b>{category_name}</b> kategoriyasi\n\n"
    text += "Mahsulotlarni tanlang:\n\n"
    
    for name, price, stock, pid in products_data:
        text += f"📦 {name}\n"
        text += f"💰 {price:,.0f} so'm\n"
        text += f"📊 Qolgan: {stock} ta\n\n"
    
    # Создаем клавиатуру с ID товаров
    kb = InlineKeyboardBuilder()
    for name, price, stock, pid in products_data:
        kb.button(text=f"📦 {name} - {price:,.0f} so'm", callback_data=f"product_{pid}")
    kb.button(text="◀️ Kategoriyalarga qaytar", callback_data="back_to_categories")
    kb.adjust(1)
    
    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("product_"))
async def view_product_detail(callback: CallbackQuery, state: FSMContext):
    """Mahsulot detalyalari"""
    product_id = int(callback.data.split("_")[1])
    
    async with AsyncSessionLocal() as session:
        product = await ProductService.get_product_by_id(session, product_id)
        
        if not product:
            await callback.answer("Mahsulot topilmadi.", show_alert=True)
            return
        
        avg_rating = await ReviewService.get_average_rating(session, product_id)
        
        # Загружаем все данные внутри контекста
        await session.refresh(product, ["category"])
        product_data = {
            "name": product.name_uz,
            "description": product.description_uz or "Tavsif mavjud emas",
            "price": product.price,
            "category": product.category.name_uz,
            "rating": avg_rating,
            "stock": product.stock,
            "sales": product.sales_count,
            "id": product_id
        }
    
    await state.set_state(ShopStates.viewing_product)
    await state.update_data(product_id=product_id)
    
    text = f"<b>{product_data['name']}</b>\n\n"
    text += f"<b>Tavsifi:</b>\n{product_data['description']}\n\n"
    text += f"💰 <b>Narx:</b> {product_data['price']:,.0f} so'm\n"
    text += f"📦 <b>Kategoriya:</b> {product_data['category']}\n"
    text += f"⭐ <b>Reyting:</b> {product_data['rating']}/5\n"
    text += f"📊 <b>Qolgan:</b> {product_data['stock']} ta\n"
    text += f"🔥 <b>Sotilgan:</b> {product_data['sales']} ta\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_product_detail_kb(product_id),
        parse_mode="HTML"
    )
    await callback.answer()


# ========================
# SAVAT
# ========================

@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    """Savatga qo'shish"""
    product_id = int(callback.data.split("_")[3])
    
    async with AsyncSessionLocal() as session:
        product = await ProductService.get_product_by_id(session, product_id)
        
        if not product or product.stock <= 0:
            await callback.answer("Bu mahsulot sotilgan.", show_alert=True)
            return
        
        product_name = product.name_uz
        product_stock = product.stock
    
    await state.set_state(ShopStates.selecting_quantity)
    await state.update_data(product_id=product_id)
    
    await callback.message.edit_text(
        f"📦 {product_name}\n\n"
        "Miqdorni tanlang (1-{}):\n\n".format(min(10, product_stock)),
        reply_markup=get_quantity_kb(product_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("qty_select_"))
async def select_quantity(callback: CallbackQuery, state: FSMContext):
    """Miqdor tanlash"""
    parts = callback.data.split("_")
    product_id = int(parts[2])
    quantity = int(parts[3])
    
    async with AsyncSessionLocal() as session:
        user = await UserService.get_user_by_telegram_id(
            session, callback.from_user.id
        )
        
        # Savatga qo'shish
        await CartService.add_to_cart(
            session, user.id, product_id, quantity
        )
        
        product = await ProductService.get_product_by_id(session, product_id)
        total_price, total_items = await CartService.get_cart_total(session, user.id)
        
        # Загружаем данные внутри контекста
        product_name = product.name_uz
        product_price = product.price
    
    await callback.message.edit_text(
        f"✅ <b>{product_name}</b> savatga qo'shildi!\n\n"
        f"📦 Miqdor: {quantity} ta\n"
        f"💰 Narx: {product_price * quantity:,.0f} so'm\n\n"
        f"🛒 Savatda jami: {total_items} ta mahsulot\n"
        f"💵 Umumiy summa: {total_price:,.0f} so'm",
        parse_mode="HTML"
    )
    
    # Asosiy menyu
    await callback.message.answer(
        "Yana nima qilishni xohlaysiz?",
        reply_markup=get_main_menu_kb()
    )
    await callback.answer()


@router.message(F.text == "🛒 Savatni ko'rish")
async def view_cart(message: Message, state: FSMContext):
    """Savatni ko'rish"""
    async with AsyncSessionLocal() as session:
        user = await UserService.get_user_by_telegram_id(session, message.from_user.id)
        cart = await CartService.get_cart_with_items(session, user.id)
        total_price, total_items = await CartService.get_cart_total(session, user.id)
        
        # Загружаем все данные ВНУТРИ контекста
        if cart and cart.items:
            cart_data = []
            for item in cart.items:
                await session.refresh(item, ["product"])
                cart_data.append({
                    "name": item.product.name_uz,
                    "price": item.product.price,
                    "quantity": item.quantity,
                    "item_id": item.id
                })
        else:
            cart_data = None
    
    await state.set_state(ShopStates.in_cart)
    
    if not cart_data:
        await message.answer(
            "🛒 Savatiniz bo'sh.\n\n"
            "Do'kongi'dan mahsulot qo'shing!",
            reply_markup=get_main_menu_kb()
        )
        return
    
    text = "🛒 <b>SAVAT:</b>\n\n"
    for item in cart_data:
        text += f"📦 {item['name']}\n"
        text += f"   💰 {item['price']:,.0f} so'm x {item['quantity']} = "
        text += f"{item['price'] * item['quantity']:,.0f} so'm\n\n"
    
    text += f"<b>Umumiy summa: {total_price:,.0f} so'm</b>"
    
    await message.answer(
        text,
        reply_markup=get_cart_kb(cart_data or []),
        parse_mode="HTML"
    )


# ========================
# BUYURTMA OFORMLASH
# ========================

@router.callback_query(F.data == "checkout_start")
async def checkout_start(callback: CallbackQuery, state: FSMContext):
    """Oformlashni boshlash"""
    async with AsyncSessionLocal() as session:
        user = await UserService.get_user_by_telegram_id(
            session, callback.from_user.id
        )
        user_id = user.id
    
    await state.set_state(ShopStates.entering_first_name)
    await state.update_data(user_id=user_id)
    
    await callback.message.edit_text(
        "📝 Iltimos, ismingizni kiriting:",
        reply_markup=None
    )
    await callback.answer()


@router.message(ShopStates.entering_first_name)
async def enter_first_name(message: Message, state: FSMContext):
    """Ism kiritish"""
    await state.update_data(first_name=message.text)
    await state.set_state(ShopStates.entering_last_name)
    
    await message.answer("👤 Familyangizni kiriting:")


@router.message(ShopStates.entering_last_name)
async def enter_last_name(message: Message, state: FSMContext):
    """Familya kiritish"""
    await state.update_data(last_name=message.text)
    await state.set_state(ShopStates.entering_phone)
    
    await message.answer("📱 Telefon raqamingizni kiriting (masalan: +998901234567):")


@router.message(ShopStates.entering_phone)
async def enter_phone(message: Message, state: FSMContext):
    """Telefon kiritish"""
    await state.update_data(phone=message.text)
    await state.set_state(ShopStates.entering_address)
    
    await message.answer("🏠 Yetkazib berish manzilini kiriting:")


@router.message(ShopStates.entering_address)
async def enter_address(message: Message, state: FSMContext):
    """Manzil kiritish"""
    data = await state.get_data()
    
    async with AsyncSessionLocal() as session:
        # Foydalanuvchi ma'lumotlarini yangilash
        await UserService.update_user_profile(
            session,
            data['user_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone'],
            address=message.text
        )
        
        # Buyurtma yaratish
        order = await OrderService.create_order(
            session,
            data['user_id'],
            message.text
        )
        
        if not order:
            await message.answer("Xato: Savat bo'sh!")
            return
        
        # Buyurtma ma'lumotlarini olish
        order = await OrderService.get_order_by_id(session, order.id)
        await session.refresh(order, ["items"])
        
        # Загружаем все товары внутри контекста
        items_data = []
        total = 0
        for item in order.items:
            await session.refresh(item, ["product"])
            items_data.append({
                "name": item.product.name_uz,
                "quantity": item.quantity,
                "price": item.price_at_purchase
            })
            total += item.quantity * item.price_at_purchase
        
        order_data = {
            "id": order.id,
            "total": total,
            "items": items_data
        }
    
    await state.set_state(ShopStates.reviewing_order)
    await state.update_data(order_id=order_data['id'])
    
    # Buyurtma tafsili
    text = "📋 <b>BUYURTMANING TAFSILI:</b>\n\n"
    text += f"<b>Raqami:</b> #{order_data['id']}\n"
    text += f"<b>F.I.SH:</b> {data['first_name']} {data['last_name']}\n"
    text += f"<b>Telefon:</b> {data['phone']}\n"
    text += f"<b>Manzil:</b> {message.text}\n\n"
    text += f"<b>Mahsulotlar:</b>\n"
    
    for item in order_data['items']:
        text += f"  • {item['name']} - "
        text += f"{item['quantity']} ta x {item['price']:,.0f} = "
        text += f"{item['quantity'] * item['price']:,.0f} so'm\n"
    
    text += f"\n<b>Jami:</b> {order_data['total']:,.0f} so'm"
    
    await message.answer(
        text,
        reply_markup=get_order_confirmation_kb(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "confirm_order_yes")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    """Buyurtmani tasdiqlash"""
    data = await state.get_data()
    
    async with AsyncSessionLocal() as session:
        order = await OrderService.get_order_by_id(session, data['order_id'])
        await OrderService.update_order_status(session, order.id, "tasdiqlandi")
        
        total_price = order.total_price
        
        # To'lov risobni yaratish
        await PaymentService.create_payment(
            session,
            order.id,
            order.user_id,
            total_price,
            "kutilmoqda"
        )
    
    text = "✅ <b>Buyurtma tasdiqlandi!</b>\n\n"
    text += f"Buyurtma raqami: <b>#{data['order_id']}</b>\n"
    text += f"Jami summa: <b>{total_price:,.0f} so'm</b>\n\n"
    text += "💳 To'lov usulini tanlang:"
    
    await state.update_data(order_id=data['order_id'], total_price=total_price)
    
    await callback.message.edit_text(
        text,
        reply_markup=get_payment_method_kb(),
        parse_mode="HTML"
    )
    
    await callback.answer()


# ========================
# PAYMENT HANDLERS
# ========================

async def process_payment(callback: CallbackQuery, state: FSMContext, payment_method: str):
    """Общий обработчик платежей"""
    from services.invoice_generator import generate_invoice
    
    data = await state.get_data()
    order_id = data.get('order_id')
    
    if not order_id:
        await callback.answer("Xato: Buyurtma topilmadi!", show_alert=True)
        return
    
    async with AsyncSessionLocal() as session:
        # Получаем информацию о заказе
        order = await OrderService.get_order_by_id(session, order_id)
        user = await UserService.get_user_by_telegram_id(session, callback.from_user.id)
        payment = await PaymentService.get_payment_by_order_id(session, order_id)
        
        # Обновляем статус платежа
        if payment:
            await PaymentService.update_payment_status(
                session, payment.id, "tasdiqlandi", payment_method
            )
        
        # Обновляем статус заказа
        await OrderService.update_order_status(session, order_id, "tasdiqlandi")
        
        # Подготавливаем данные для чека
        await session.refresh(order, ["items", "user"])
        
        items_for_invoice = []
        for item in order.items:
            await session.refresh(item, ["product"])
            items_for_invoice.append((
                item.product.name_uz,
                item.quantity,
                item.price_at_purchase
            ))
    
    # Генерируем чек
    payment_methods = {
        "payment_click": "💳 Click",
        "payment_payme": "📱 Payme",
        "payment_card": "🏧 Karta",
        "payment_cash": "🏪 Naqd To'lov",
        "payment_transfer": "🔄 Ko'chirish"
    }
    
    method_name = payment_methods.get(callback.data, "Noma'lum")
    
    invoice_text = generate_invoice(
        order_id=order_id,
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        phone=user.phone_number or "---",
        address=user.address or "---",
        total=order.total_price,
        items=items_for_invoice
    )
    
    # Добавляем информацию о способе платежа
    invoice_text += f"\n💳 <b>TO'LOV USULI:</b> {method_name}\n"
    invoice_text += "✅ <b>TO'LOV QABUL QILINDI!</b>\n\n"
    invoice_text += "Sizga tez orada xabar yuboriladi. Raxmat! 🙏"
    
    # Отправляем чек
    await callback.message.edit_text(
        invoice_text,
        reply_markup=None,
        parse_mode="HTML"
    )
    
    # Отправляем подтверждение на главное меню
    await callback.message.answer(
        "🏠 Asosiy menyu",
        reply_markup=get_main_menu_kb()
    )
    
    await state.clear()
    await callback.answer(f"✅ {method_name} orqali to'lov qabul qilindi!", show_alert=False)


@router.callback_query(F.data == "payment_click")
async def payment_click(callback: CallbackQuery, state: FSMContext):
    """Click orqali to'lov"""
    await process_payment(callback, state, "Click")


@router.callback_query(F.data == "payment_payme")
async def payment_payme(callback: CallbackQuery, state: FSMContext):
    """Payme orqali to'lov"""
    await process_payment(callback, state, "Payme")


@router.callback_query(F.data == "payment_card")
async def payment_card(callback: CallbackQuery, state: FSMContext):
    """Karta orqali to'lov"""
    await process_payment(callback, state, "Karta")


@router.callback_query(F.data == "payment_cash")
async def payment_cash(callback: CallbackQuery, state: FSMContext):
    """Naqd to'lov"""
    await process_payment(callback, state, "Naqd To'lov")


@router.callback_query(F.data == "payment_transfer")
async def payment_transfer(callback: CallbackQuery, state: FSMContext):
    """Ko'chirish orqali to'lov"""
    await process_payment(callback, state, "Ko'chirish")


@router.callback_query(F.data == "cancel_payment")
async def cancel_payment(callback: CallbackQuery, state: FSMContext):
    """Bekor qilish"""
    data = await state.get_data()
    order_id = data.get('order_id')
    
    if order_id:
        async with AsyncSessionLocal() as session:
            # Bekor qilish
            await OrderService.update_order_status(session, order_id, "bekor_qilingan")
    
    text = "❌ <b>Buyurtma bekor qilindi!</b>\n\n"
    text += "Yangi buyurtma qilish uchun /shop buyruq yuboring."
    
    await callback.message.edit_text(
        text,
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )
    
    await state.clear()
    await callback.answer()


# ========================
# FOYDALANUVCHI BUYURTMALARI
# ========================

@router.message(F.text == "📦 Buyurtmalarim")
async def view_orders(message: Message, state: FSMContext):
    """Foydalanuvch buyurtmalarini ko'rish"""
    async with AsyncSessionLocal() as session:
        user = await UserService.get_user_by_telegram_id(
            session, message.from_user.id
        )
        
        if not user:
            await message.answer("Xato: Foydalanuvchi topilmadi!")
            return
        
        user_id = user.id
        orders = await OrderService.get_user_orders(session, user_id)
    
    if not orders:
        await message.answer(
            "📦 Hozircha buyurtmalaringiz yo'q.\n\n"
            "Do'kondan xarid qilishni boshlang!",
            reply_markup=get_main_menu_kb()
        )
        return
    
    await state.set_state(ShopStates.viewing_orders)
    await message.answer(
        "📦 Buyurtmalaringiz:",
        reply_markup=get_orders_kb(orders)
    )


# ========================
# PROFIL
# ========================

@router.message(F.text == "👤 Profilim")
async def view_profile(message: Message, state: FSMContext):
    """Profilni ko'rish"""
    async with AsyncSessionLocal() as session:
        user = await UserService.get_user_by_telegram_id(
            session, message.from_user.id
        )
        
        # Загружаем все данные внутри контекста
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name or "",
            "phone": user.phone_number or "Kiritilmagan",
            "address": user.address or "Kiritilmagan",
            "created_at": user.created_at.strftime('%d.%m.%Y')
        }
    
    await state.set_state(ShopStates.viewing_account)
    
    text = "👤 <b>PROFIL:</b>\n\n"
    text += f"<b>Salom:</b> {user_data['first_name']} {user_data['last_name']}\n"
    text += f"<b>Telefon:</b> {user_data['phone']}\n"
    text += f"<b>Manzil:</b> {user_data['address']}\n"
    text += f"<b>Registratsiya:</b> {user_data['created_at']}"
    
    await message.answer(
        text,
        reply_markup=get_profile_kb(user_data),
        parse_mode="HTML"
    )


# ========================
# CART OPERATIONS
# ========================

@router.callback_query(F.data.startswith("remove_from_cart_"))
async def remove_from_cart(callback: CallbackQuery, state: FSMContext):
    """Savat'dan mahsulotni chiqarish"""
    item_id = int(callback.data.split("_")[-1])
    
    async with AsyncSessionLocal() as session:
        await CartService.remove_from_cart(session, item_id)
        
        # Savat'ni yangi korinishda ko'rsatish
        user = await UserService.get_user_by_telegram_id(session, callback.from_user.id)
        cart = await CartService.get_cart_with_items(session, user.id)
        
        if not cart or not cart.items:
            text = "🛒 Savatiniz bo'sh.\n\nDo'kongi'dan mahsulot qo'shing!"
            cart_data = []
        else:
            cart_data = []
            total_price = 0
            for item in cart.items:
                await session.refresh(item, ["product"])
                item_total = item.product.price * item.quantity
                total_price += item_total
                cart_data.append({
                    "name": item.product.name_uz,
                    "price": item.product.price,
                    "quantity": item.quantity,
                    "item_id": item.id
                })
            
            text = "🛒 <b>SAVAT:</b>\n\n"
            for item in cart_data:
                text += f"📦 {item['name']}\n"
                text += f"   💰 {item['price']:,.0f} so'm x {item['quantity']} = "
                text += f"{item['price'] * item['quantity']:,.0f} so'm\n\n"
            
            text += f"<b>Umumiy summa: {total_price:,.0f} so'm</b>"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_cart_kb(cart_data),
        parse_mode="HTML"
    )
    await callback.answer("✅ Mahsulot savat'dan chiqarildi")


@router.callback_query(F.data == "continue_shopping")
async def continue_shopping(callback: CallbackQuery, state: FSMContext):
    """Xarid qilishni davom ettirish"""
    async with AsyncSessionLocal() as session:
        categories = await CategoryService.get_all_categories(session)
    
    await state.set_state(ShopStates.viewing_categories)
    await callback.message.edit_text(
        "📂 Kategoriyalarni tanlang:",
        reply_markup=get_categories_kb(categories)
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_products")
async def back_to_products(callback: CallbackQuery, state: FSMContext):
    """Mahsulotlarga qaytish"""
    data = await state.get_data()
    category_id = data.get('category_id')
    
    if not category_id:
        await callback.answer("Xato: Kategoriya topilmadi", show_alert=True)
        return
    
    async with AsyncSessionLocal() as session:
        products = await ProductService.get_products_by_category(session, category_id)
    
    await state.set_state(ShopStates.viewing_products)
    await callback.message.edit_text(
        "📦 Mahsulotlarni tanlang:",
        reply_markup=get_products_kb(products)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("reviews_"))
async def show_reviews(callback: CallbackQuery, state: FSMContext):
    """Mahsulot sharhlarini ko'rish"""
    product_id = int(callback.data.split("_")[1])
    
    async with AsyncSessionLocal() as session:
        product = await ProductService.get_product_by_id(session, product_id)
        reviews = await ReviewService.get_product_reviews(session, product_id)
    
    if not reviews:
        text = f"⭐ <b>{product.name_uz}</b> uchun sharhlar yo'q\n\n"
        text += "Birinchi sharh qoldirvchi bo'ling!"
    else:
        text = f"⭐ <b>{product.name_uz}</b> - Sharhlar:\n\n"
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        text += f"O'rtacha reyting: {avg_rating:.1f}/5 ⭐\n"
        text += f"Jami: {len(reviews)} sharh\n\n"
        
        for idx, review in enumerate(reviews[:5], 1):  # Ko'rsatish faqat 5 tasi
            text += f"{idx}. ⭐ {review.rating}/5\n"
            text += f"   💬 {review.comment[:100]}...\n\n"
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_product_detail_kb(product_id))
    await callback.answer()


# ========================
# ORQAGA QAYTISH
# ========================

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    """Asosiy menyu'ga qaytish"""
    await state.clear()
    await callback.message.delete()
    
    await callback.message.answer(
        "🏠 Asosiy menyu",
        reply_markup=get_main_menu_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery, state: FSMContext):
    """Kategoriyalarga qaytish"""
    async with AsyncSessionLocal() as session:
        categories = await CategoryService.get_all_categories(session)
    
    await state.set_state(ShopStates.viewing_categories)
    await callback.message.edit_text(
        "📂 Kategoriyalarni tanlang:",
        reply_markup=get_categories_kb(categories)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("back_to_"))
async def go_back(callback: CallbackQuery):
    """Umumiy orqaga tugmasi"""
    await callback.answer("Orqaga qaytildi.", show_alert=False)


# ========================
# QOLGAN KOMANDALAR
# ========================

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Yordam"""
    help_text = """
❓ <b>BOT QOLLANMASI</b>

🛍️ <b>Shopni ishlatish:</b>
1. /start bosing
2. "🛍️ Do'konga kirish" tugmasini bosing
3. Kategoriyani tanlang
4. Mahsulotni tanlang va savatchaga qo'shing
5. Savatchani ko'ring va buyurtma qo'yib chiqing

🛒 <b>Asosiy tugmalar:</b>
• 🛍️ Do'konga kirish - Katalog
• ⭐ Eng ko'p sotilganlar - Populyar mahsulotlar
• 🛒 Savatim - Sizning savatchang
• 👤 Profil - Profilingiz va buyurtmalaringiz

💳 <b>To'lov usullari:</b>
• Kredit karta
• Mobile Money
• Jismoniy pul

❓ <b>Savollar:</b>
Bot muammolari bo'lsa, admin bilan bog'laning.

📞 Admin: @support
    """
    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("shop"))
async def cmd_shop(message: Message, state: FSMContext):
    """Do'konni ochish"""
    async with AsyncSessionLocal() as session:
        categories = await CategoryService.get_all_categories(session)
    
    if not categories:
        await message.answer("Hozircha kategoriyalar mavjud emas.")
        return
    
    await state.set_state(ShopStates.viewing_categories)
    await message.answer(
        "📂 Kategoriyalarni tanlang:",
        reply_markup=get_categories_kb(categories)
    )


@router.message(Command("cart"))
async def cmd_cart(message: Message, state: FSMContext):
    """Savatni ko'rsatish"""
    async with AsyncSessionLocal() as session:
        user = await UserService.get_user_by_telegram_id(session, message.from_user.id)
        cart = await CartService.get_cart_with_items(session, user.id)
        
        if not cart or not cart.items:
            await message.answer(
                "🛒 Sizning savatchangiz bo'sh.\n\n"
                "Mahsulot qo'shish uchun /shop komandasini ishlating."
            )
            return
        
        # Загружаем все товары внутри контекста
        cart_items_data = []
        total = 0
        for item in cart.items:
            await session.refresh(item, ["product"])
            price = item.product.price * item.quantity
            total += price
            cart_items_data.append({
                "name": item.product.name_uz,
                "unit_price": item.product.price,
                "quantity": item.quantity,
                "total": price
            })
    
    await state.set_state(ShopStates.in_cart)
    
    text = "🛒 <b>SIZNING SAVATCHANGIZ:</b>\n\n"
    for idx, item in enumerate(cart_items_data, 1):
        text += f"{idx}. {item['name']}\n"
        text += f"   💰 {item['unit_price']:,.0f} × {item['quantity']} = {item['total']:,.0f} so'm\n\n"
    
    text += f"<b>Jami: {total:,.0f} so'm</b>"
    
    await message.answer(text, reply_markup=get_cart_kb(cart_items_data), parse_mode="HTML")


@router.message(Command("profile"))
async def cmd_profile(message: Message, state: FSMContext):
    """Profil"""
    async with AsyncSessionLocal() as session:
        user = await UserService.get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.first_name
        )
        
        # Загружаем все данные внутри контекста
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name or "o'zgartirilmagan",
            "phone": user.phone_number or "o'zgartirilmagan",
            "address": user.address or "o'zgartirilmagan"
        }
    
    await state.set_state(ShopStates.viewing_account)
    
    text = f"""
👤 <b>SIZNING PROFILINGIZ</b>

📛 Ism: {user_data['first_name']}
📌 Familiya: {user_data['last_name']}
📱 Telefon: {user_data['phone']}
📍 Manzil: {user_data['address']}

👁️ Telegram ID: {message.from_user.id}
    """
    await message.answer(text, reply_markup=get_profile_kb(user_data), parse_mode="HTML")


@router.message(Command("orders"))
async def cmd_orders(message: Message, state: FSMContext):
    """Mening buyurtmalarim"""
    async with AsyncSessionLocal() as session:
        user = await UserService.get_user_by_telegram_id(session, message.from_user.id)
        orders = await OrderService.get_user_orders(session, user.id)
        
        if not orders:
            await message.answer(
                "📋 Sizda hali buyurtmalar yo'q.\n\n"
                "Xarid qilish uchun /shop komandasini ishlating."
            )
            return
        
        # Загружаем все данные внутри контекста
        orders_data = []
        for order in orders:
            orders_data.append({
                "id": order.id,
                "total": order.total_price,
                "created": order.created_at.strftime('%d.%m.%Y %H:%M'),
                "status": order.status
            })
    
    await state.set_state(ShopStates.viewing_orders)
    text = "📋 <b>SIZNING BUYURTMALARINGIZ:</b>\n\n"
    
    for idx, order in enumerate(orders_data, 1):
        text += f"{idx}. ID: {order['id']}\n"
        text += f"   💰 {order['total']:,.0f} so'm\n"
        text += f"   📅 {order['created']}\n"
        text += f"   🔔 Status: {order['status']}\n\n"
    
    await message.answer(text, parse_mode="HTML")


@router.message(Command("reviews"))
async def cmd_reviews(message: Message, state: FSMContext):
    """Mening sharhlarim"""
    async with AsyncSessionLocal() as session:
        user = await UserService.get_user_by_telegram_id(session, message.from_user.id)
        reviews = await ReviewService.get_user_reviews(session, user.id)
        
        if not reviews:
            await message.answer(
                "⭐ Sizda sharhlar yo'q.\n\n"
                "Mahsulot xarid qilib, sotib olgandan keyinroq sharh qoldirishingiz mumkin."
            )
            return
        
        # Загружаем все данные внутри контекста
        reviews_data = []
        for review in reviews:
            await session.refresh(review, ["product"])
            reviews_data.append({
                "product_name": review.product.name_uz,
                "rating": review.rating,
                "comment": review.comment
            })
    
    text = "⭐ <b>SIZNING SHARHLARINGIZ:</b>\n\n"
    
    for idx, review in enumerate(reviews_data, 1):
        text += f"{idx}. {review['product_name']}\n"
        text += f"   ⭐ Reyting: {review['rating']}/5\n"
        text += f"   💬 '{review['comment']}'\n\n"
    
    await message.answer(text, parse_mode="HTML")


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    """Admin panel"""
    # Burada admin check qilsangiz bo'ladi
    # Hozircha hamma uchun ochiq
    await state.set_state(ShopStates.admin_menu)
    
    text = """
⚙️ <b>ADMIN PANEL</b>

Bu yerda statistika va boshqaruv imkoniyatlari mavjud.
Hozircha ta'mirlash oraligida.
    """
    await message.answer(text, parse_mode="HTML")

