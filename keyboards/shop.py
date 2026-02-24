from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


# ============ ГЛАВНОЕ МЕНЮ ============


def get_main_menu():
    """Главное меню магазина"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍️ Магазин")],
            [KeyboardButton(text="🔥 Топ продажи"), KeyboardButton(text="🛒 Корзина")],
            [KeyboardButton(text="📦 Мои заказы"), KeyboardButton(text="👤 Аккаунт")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


# ============ КАТЕГОРИИ ============


def get_categories_keyboard(categories):
    """Клавиатура с категориями"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for category in categories:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=category.name_uz,
                callback_data=f"cat_{category.id}"
            )
        ])
    
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🔙 Орқага", callback_data="back_to_menu")
    ])
    
    return keyboard


# ============ ТОВАРЫ В КАТЕГОРИИ ============


def get_products_keyboard(products, category_id):
    """Клавиатура с товарами в категории"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for product in products:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"{product.name_uz} ({product.price:,.0f} so'm)",
                callback_data=f"prod_{product.id}"
            )
        ])
    
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🔙 Категорияга", callback_data="cat_list")
    ])
    
    return keyboard


# ============ ТОВАР ============


def get_product_keyboard(product_id):
    """Клавиатура для товара"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕", callback_data=f"add_1_{product_id}"),
            InlineKeyboardButton(text="Корзинага қўш", callback_data=f"add_cart_{product_id}"),
        ],
        [
            InlineKeyboardButton(text="🔙 Орқага", callback_data="back_to_products")
        ]
    ])
    return keyboard


# ============ ТОП ПРОДАЖИ ============


def get_top_sales_keyboard(products):
    """Клавиатура с топ продажами"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for idx, product in enumerate(products, 1):
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"{idx}. {product.name_uz} - ⭐ ({product.price:,.0f} so'm)",
                callback_data=f"prod_{product.id}"
            )
        ])
    
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🔙 Орқага", callback_data="back_to_menu")
    ])
    
    return keyboard


# ============ КОРЗИНА ============


def get_cart_keyboard(cart_items):
    """Клавиатура для корзины"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for item in cart_items:
        # Handle both dict and object formats
        if isinstance(item, dict):
            name = item.get('name', 'N/A')
            quantity = item.get('quantity', 0)
            item_id = item.get('item_id', 0)
        else:
            name = item.product.name_uz
            quantity = item.quantity
            item_id = item.id
        
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"❌",
                callback_data=f"del_cart_{item_id}"
            ),
            InlineKeyboardButton(
                text=f"{name} x{quantity}",
                callback_data=f"edit_cart_{item_id}"
            )
        ])
    
    keyboard.inline_keyboard.extend([
        [
            InlineKeyboardButton(text="🧹 Очистить", callback_data="clear_cart"),
            InlineKeyboardButton(text="📝 Оформить", callback_data="checkout")
        ],
        [
            InlineKeyboardButton(text="🔙 Орқага", callback_data="back_to_menu")
        ]
    ])
    
    return keyboard


def get_cart_empty_keyboard():
    """Клавиатура пустой корзины"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Орқага", callback_data="back_to_menu")]
    ])
    return keyboard


# ============ ОФОРМЛЕНИЕ ЗАКАЗА ============


def get_checkout_keyboard():
    """Клавиатура для оформления заказа"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Адрес", callback_data="input_address")],
        [InlineKeyboardButton(text="📝 Изменить ввод", callback_data="edit_checkout")],
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_order")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_checkout")]
    ])
    return keyboard


def get_user_data_keyboard():
    """Клавиатура для ввода данных пользователя"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Отправить местоположение", request_location=True)],
            [KeyboardButton(text="Cancel")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_cancel_keyboard():
    """Клавиатура отмены"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


# ============ ЗАКАЗЫ ============


def get_orders_keyboard(orders):
    """Клавиатура для заказов"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    status_emojis = {
        "yangi": "🆕",
        "tasdiqlandi": "✅",
        "yuborildi": "🚚",
        "yetkazildi": "📦",
        "bekor qilingan": "❌"
    }
    
    status_labels = {
        "yangi": "Янги",
        "tasdiqlandi": "Тасдиқланди",
        "yuborildi": "Юборилди",
        "yetkazildi": "Етказилди",
        "bekor qilingan": "Бекор қилинган"
    }
    
    for order in orders:
        emoji = status_emojis.get(order.status, "❓")
        status_text = status_labels.get(order.status, order.status)
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"{emoji} Заказ #{order.id} - {status_text}",
                callback_data=f"order_{order.id}"
            )
        ])
    
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🔙 Орқага", callback_data="back_to_menu")
    ])
    
    return keyboard if orders else None


def get_empty_orders_keyboard():
    """Клавиатура, когда нет заказов"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Орқага", callback_data="back_to_menu")]
    ])
    return keyboard


# ============ АККАУНТ ============


def get_account_keyboard():
    """Клавиатура аккаунта"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Ред. данные", callback_data="edit_profile")],
        [InlineKeyboardButton(text="🔙 Орқага", callback_data="back_to_menu")]
    ])
    return keyboard
