from aiogram.fsm.state import State, StatesGroup


class ShopStates(StatesGroup):
    """Magasin FSM holatlari"""
    
    # ========================
    # KATALOG VA MAHSULOTLAR
    # ========================
    viewing_categories = State()      # Kategoriyalarni ko'rish
    viewing_products = State()        # Mahsulotlarni ko'rish
    viewing_product = State()         # Alohida mahsulot
    browsing_top_sales = State()      # Eng ko'p sotilganlar
    selecting_quantity = State()      # Mahsulot miqdorini tanlash
    
    # ========================
    # SAVAT
    # ========================
    in_cart = State()                 # Savat ko'rinishi
    removing_from_cart = State()      # Savatdan chiqarish
    
    # ========================
    # BUYURTMA OFORMLASH
    # ========================
    checkout_start = State()          # Oformlashni boshlash
    entering_first_name = State()     # Ishmni kiritish
    entering_last_name = State()      # Familyasini kiritish
    entering_phone = State()          # Telefon raqamini kiritish
    entering_address = State()        # Manzilni kiritish
    entering_notes = State()          # Izohlar kiritish
    selecting_payment = State()       # To'lov usulini tanlash
    reviewing_order = State()         # Buyurtmani ko'rib chiqish
    
    # ========================
    # BUYURTMALAR
    # ========================
    viewing_orders = State()          # Buyurtmalar ro'yxati
    viewing_order_details = State()   # Buyurtma detalyalari
    canceling_order = State()         # Buyurtmani bekor qilish
    
    # ========================
    # SHARHLAR VA REYTING
    # ========================
    leaving_review = State()          # Sharh yozish
    rating_product = State()          # Reytingni berish
    viewing_reviews = State()         # Sharhlani ko'rish
    
    # ========================
    # PROFIL
    # ========================
    viewing_account = State()         # Profilni ko'rish
    editing_profile = State()         # Profilni tahrirlash
    updating_phone = State()          # Telefon yangilash
    updating_address = State()        # Manzil yangilash
    
    # ========================
    # ADMIN PANELI
    # ========================
    admin_menu = State()              # Admin menyu
    managing_products = State()       # Mahsulotlarni boshqarish
    adding_product = State()          # Mahsulot qo'shish
    editing_product = State()         # Mahsulot tahrirlash
    managing_orders = State()         # Buyurtmalarni boshqarish
    managing_categories = State()     # Kategoriyalarni boshqarish
    viewing_statistics = State()      # Statistikani ko'rish

