"""
Telegram Bot Shop Klaviaturalari
Uzbekcha (Latin): Barcha tugmachalari
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# ========================
# ASOSIY OYNI KLAVIATURALARI
# ========================

def get_main_menu_kb() -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi"""
    kb = ReplyKeyboardBuilder()
    
    kb.button(text="🛍️ Do'konga kirish")
    kb.button(text="🛒 Savatni ko'rish")
    kb.button(text="⭐ Eng ko'p sotilganlar")
    kb.button(text="📦 Buyurtmalarim")
    kb.button(text="👤 Profilim")
    kb.button(text="❓ Yordam")
    
    kb.adjust(2, 2, 2)
    return kb.as_markup(resize_keyboard=True)


# ========================
# KATEGORIYA VA MAHSULOT KLAVIATURALARI
# ========================

def get_categories_kb(categories: list) -> InlineKeyboardMarkup:
    """Kategoriyalar inline klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    for category in categories:
        kb.button(
            text=f"📂 {category.name_uz}",
            callback_data=f"category_{category.id}"
        )
    
    kb.button(text="◀️ Orqaga", callback_data="back_to_main")
    kb.adjust(1)
    return kb.as_markup()


def get_products_kb(products: list, page: int = 1, total_pages: int = 1) -> InlineKeyboardMarkup:
    """Mahsulotlar inline klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    # Mahsulotlarni ko'rsatish (har bittasi alohida tugma)
    for product in products:
        kb.button(
            text=f"📦 {product.name_uz} - {product.price:,.0f} so'm",
            callback_data=f"product_{product.id}"
        )
    
    kb.button(text="◀️ Kategoriyalarga qaytar", callback_data="back_to_categories")
    kb.adjust(1)
    
    return kb.as_markup()


def get_product_detail_kb(product_id: int) -> InlineKeyboardMarkup:
    """Mahsulot detallarini ko'rsatish klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    kb.button(text="🛒 Savatga qo'shish", callback_data=f"add_to_cart_{product_id}")
    kb.button(text="⭐ Sharhlar", callback_data=f"reviews_{product_id}")
    kb.button(text="◀️ Orqaga", callback_data="back_to_products")
    
    kb.adjust(1)
    return kb.as_markup()


# ========================
# SAVAT KLAVIATURALARI
# ========================

def get_cart_kb(cart_items: list) -> InlineKeyboardMarkup:
    """Savat klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    if cart_items:
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
            
            kb.button(
                text=f"🗑️ {name} ({quantity}x)",
                callback_data=f"remove_from_cart_{item_id}"
            )
        
        kb.button(text="➕ Mahsulot qo'shish", callback_data="continue_shopping")
        kb.button(text="✅ Buyurtma qilish", callback_data="checkout_start")
    else:
        kb.button(text="🛍️ Do'konga kirish", callback_data="back_to_categories")
    
    kb.button(text="◀️ Orqaga", callback_data="back_to_main")
    kb.adjust(1)
    
    return kb.as_markup()


def get_quantity_kb(product_id: int) -> InlineKeyboardMarkup:
    """Mahsulot miqdorini tanlash klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    for qty in [1, 2, 3, 5, 10]:
        kb.button(
            text=f"{qty}",
            callback_data=f"qty_select_{product_id}_{qty}"
        )
    
    kb.button(text="❌ Bekor qilish", callback_data="cancel_qty")
    kb.adjust(5)
    
    return kb.as_markup()


# ========================
# BUYURTMA OFORMLASH KLAVIATURALARI
# ========================

def get_checkout_kb() -> InlineKeyboardMarkup:
    """Buyurtmani oformlash klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📝 F.I.SH. kiritish", callback_data="enter_name")
    kb.button(text="📱 Telefon raqamini kiritish", callback_data="enter_phone")
    kb.button(text="🏠 Manzilni kiritish", callback_data="enter_address")
    kb.button(text="✅ Buyurtmani tasdiqlash", callback_data="confirm_order")
    kb.button(text="🛒 Savat orqaga", callback_data="back_to_cart")
    
    kb.adjust(1)
    return kb.as_markup()


def get_payment_method_kb() -> InlineKeyboardMarkup:
    """To'lov usuli tanlash klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    kb.button(text="💳 Click", callback_data="payment_click")
    kb.button(text="📱 Payme", callback_data="payment_payme")
    kb.button(text="🏧 Karta", callback_data="payment_card")
    kb.button(text="🏪 Naqd to'lov", callback_data="payment_cash")
    kb.button(text="🔄 Ko'chirish", callback_data="payment_transfer")
    kb.button(text="❌ Bekor qilish", callback_data="cancel_payment")
    
    kb.adjust(2, 2, 2)
    return kb.as_markup()


def get_order_confirmation_kb() -> InlineKeyboardMarkup:
    """Buyurtma tasdiqlash klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    kb.button(text="✅ Ha, tasdiqlash", callback_data="confirm_order_yes")
    kb.button(text="❌ Yo'q, bekor qilish", callback_data="confirm_order_no")
    
    kb.adjust(1)
    return kb.as_markup()


# ========================
# BUYURTMALAR VA PROFIL KLAVIATURALARI
# ========================

def get_orders_kb(orders: list) -> InlineKeyboardMarkup:
    """Buyurtmalar ro'yxati klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    if orders:
        for order in orders:
            status_emoji = {
                "yangi": "🆕",
                "tasdiqlandi": "✅",
                "yuborildi": "📦",
                "yetkazildi": "✔️",
                "bekor_qilingan": "❌"
            }.get(order.status, "❓")
            
            kb.button(
                text=f"{status_emoji} Buyurtma #{order.id} - {order.total_price:,.0f} so'm",
                callback_data=f"order_detail_{order.id}"
            )
        
        kb.button(text="◀️ Orqaga", callback_data="back_to_main")
    else:
        kb.button(text="🛍️ Do'kondan xarid qilish", callback_data="back_to_categories")
    
    kb.adjust(1)
    return kb.as_markup()


def get_top_sales_kb(products: list) -> InlineKeyboardMarkup:
    """Eng ko'p sotilgan mahsulotlar klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    for product in products[:10]:  # Faqat top 10
        kb.button(
            text=f"⭐ {product.name_uz} ({product.sales_count} sotilgan)",
            callback_data=f"product_{product.id}"
        )
    
    kb.button(text="🛍️ Do'konning boshiga", callback_data="back_to_categories")
    kb.button(text="◀️ Orqaga", callback_data="back_to_main")
    kb.adjust(1)
    
    return kb.as_markup()


def get_profile_kb(user) -> InlineKeyboardMarkup:
    """Foydalanuvchi profili klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    kb.button(text="✏️ Profilni tahrirlash", callback_data="edit_profile")
    kb.button(text="📋 Mening buyurtmalarim", callback_data="my_orders")
    kb.button(text="⭐ Mening sharhlarim", callback_data="my_reviews")
    kb.button(text="🔐 Parolni o'zgartirish", callback_data="change_password")
    kb.button(text="◀️ Orqaga", callback_data="back_to_main")
    
    kb.adjust(1)
    return kb.as_markup()


def get_admin_kb() -> ReplyKeyboardMarkup:
    """Admin panel klaviaturasi"""
    kb = ReplyKeyboardBuilder()
    
    kb.button(text="📊 Statistika")
    kb.button(text="🏪 Mahsulotlar")
    kb.button(text="📦 Buyurtmalar")
    kb.button(text="👥 Foydalanuvchilar")
    kb.button(text="💬 Sharhlar")
    kb.button(text="◀️ Orqaga")
    
    kb.adjust(2, 2, 2)
    return kb.as_markup(resize_keyboard=True)


# ========================
# YORDAMCHI KLAVIATURALARI
# ========================

def get_yes_no_kb() -> InlineKeyboardMarkup:
    """Ha/Yo'q javoblash klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    kb.button(text="✅ Ha", callback_data="answer_yes")
    kb.button(text="❌ Yo'q", callback_data="answer_no")
    
    kb.adjust(2)
    return kb.as_markup()


def get_cancel_kb() -> InlineKeyboardMarkup:
    """Bekor qilish klaviaturasi"""
    kb = InlineKeyboardBuilder()
    
    kb.button(text="❌ Bekor qilish", callback_data="cancel")
    
    return kb.as_markup()


# ========================
# DINAMIK TUGMALAR YARATUVCHILARI
# ========================

def create_quantity_buttons(product_id: int, max_qty: int = 10) -> InlineKeyboardMarkup:
    """Dinamik miqdor tugmalari"""
    kb = InlineKeyboardBuilder()
    
    for qty in range(1, min(max_qty + 1, 11)):
        kb.button(text=f"{qty}", callback_data=f"qty_{product_id}_{qty}")
    
    kb.adjust(5)
    return kb.as_markup()


def create_category_filter_kb(category_id: int) -> InlineKeyboardMarkup:
    """Kategoriya bo'yicha filtrlash tugmalari"""
    kb = InlineKeyboardBuilder()
    
    kb.button(text="💰 Arzon narxlar", callback_data=f"filter_price_low_{category_id}")
    kb.button(text="💎 Qimmat narxlar", callback_data=f"filter_price_high_{category_id}")
    kb.button(text="🔥 Eng ko'p sotilganlar", callback_data=f"filter_popular_{category_id}")
    kb.button(text="⭐ Eng yaxshi sharhlar", callback_data=f"filter_rating_{category_id}")
    kb.button(text="🔄 Eski", callback_data=f"filter_new_{category_id}")
    
    kb.adjust(2)
    return kb.as_markup()


def get_back_button() -> InlineKeyboardMarkup:
    """Orqaga qaytish tugmasi"""
    kb = InlineKeyboardBuilder()
    
    kb.button(text="◀️ Orqaga", callback_data="go_back")
    
    return kb.as_markup()
