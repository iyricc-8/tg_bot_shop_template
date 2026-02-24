"""
Shop API Services - Magasin ma'lumotlarini boshqarish
"""

from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from db.models import (
    Category, Product, User, Cart, CartItem, 
    Order, OrderItem, Review, Payment
)
from datetime import datetime


# ========================
# KATEGORIYA SERVISLARI
# ========================

class CategoryService:
    """Kategoriyalar bilan ishlash"""
    
    @staticmethod
    async def get_all_categories(session: AsyncSession):
        """Barcha kategoriyalarni olish"""
        result = await session.execute(
            select(Category).order_by(Category.name_uz)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_category_by_id(session: AsyncSession, category_id: int):
        """ID bo'yicha kategoriya olish"""
        result = await session.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()


# ========================
# MAHSULOT SERVISLARI
# ========================

class ProductService:
    """Mahsulotlar bilan ishlash"""
    
    @staticmethod
    async def get_products_by_category(
        session: AsyncSession, 
        category_id: int,
        skip: int = 0,
        limit: int = 10
    ):
        """Kategoriya bo'yicha mahsulotlar"""
        result = await session.execute(
            select(Product)
            .where(
                and_(
                    Product.category_id == category_id,
                    Product.is_active == True
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(Product.name_uz)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_product_by_id(session: AsyncSession, product_id: int):
        """ID bo'yicha mahsulot olish"""
        result = await session.execute(
            select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.category))
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_top_products(session: AsyncSession, limit: int = 10):
        """Eng ko'p sotilgan mahsulotlar"""
        result = await session.execute(
            select(Product)
            .where(Product.is_active == True)
            .order_by(desc(Product.sales_count))
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def search_products(session: AsyncSession, query: str):
        """Mahsulot izlash"""
        result = await session.execute(
            select(Product)
            .where(
                and_(
                    Product.name_uz.ilike(f"%{query}%"),
                    Product.is_active == True
                )
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_products_by_price_range(
        session: AsyncSession,
        min_price: float,
        max_price: float
    ):
        """Narx oralig'iga ko'ra mahsulotlar"""
        result = await session.execute(
            select(Product)
            .where(
                and_(
                    Product.price >= min_price,
                    Product.price <= max_price,
                    Product.is_active == True
                )
            )
            .order_by(Product.price)
        )
        return result.scalars().all()


# ========================
# FOYDALANUVCHI SERVISLARI
# ========================

class UserService:
    """Foydalanuvchilar bilan ishlash"""
    
    @staticmethod
    async def get_or_create_user(session: AsyncSession, telegram_id: int, first_name: str = None):
        """Foydalanuvchini olish yoki yaratish"""
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                telegram_id=telegram_id,
                first_name=first_name
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        
        return user
    
    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int):
        """ID bo'yicha foydalanuvchi"""
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int):
        """Telegram ID bo'yicha foydalanuvchi"""
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_user_profile(
        session: AsyncSession,
        user_id: int,
        first_name: str = None,
        last_name: str = None,
        phone_number: str = None,
        address: str = None
    ):
        """Foydalanuvchi profilini yangilash"""
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if phone_number:
                user.phone_number = phone_number
            if address:
                user.address = address
            
            user.updated_at = datetime.now()
            await session.commit()
            await session.refresh(user)
        
        return user


# ========================
# SAVAT SERVISLARI
# ========================

class CartService:
    """Savat bilan ishlash"""
    
    @staticmethod
    async def get_or_create_cart(session: AsyncSession, user_id: int):
        """Savatni olish yoki yaratish"""
        result = await session.execute(
            select(Cart).where(Cart.user_id == user_id)
        )
        cart = result.scalar_one_or_none()
        
        if not cart:
            cart = Cart(user_id=user_id)
            session.add(cart)
            await session.commit()
            await session.refresh(cart)
        
        return cart
    
    @staticmethod
    async def get_cart_with_items(session: AsyncSession, user_id: int):
        """Savatni barcha mahsulotlar bilan olish"""
        result = await session.execute(
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(selectinload(Cart.items).selectinload(CartItem.product))
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def add_to_cart(
        session: AsyncSession,
        user_id: int,
        product_id: int,
        quantity: int = 1
    ):
        """Mahsulotni savatga qo'shish"""
        cart = await CartService.get_or_create_cart(session, user_id)
        
        # Mahsulot allaqachon savatda bor mi?
        result = await session.execute(
            select(CartItem)
            .where(
                and_(
                    CartItem.cart_id == cart.id,
                    CartItem.product_id == product_id
                )
            )
        )
        cart_item = result.scalar_one_or_none()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
            session.add(cart_item)
        
        await session.commit()
        await session.refresh(cart)
        return cart
    
    @staticmethod
    async def remove_from_cart(session: AsyncSession, cart_item_id: int):
        """Mahsulotni savatdan chiqarish"""
        result = await session.execute(
            select(CartItem).where(CartItem.id == cart_item_id)
        )
        cart_item = result.scalar_one_or_none()
        
        if cart_item:
            session.delete(cart_item)
            await session.commit()
        
        return True
    
    @staticmethod
    async def clear_cart(session: AsyncSession, user_id: int):
        """Savatni bo'shash"""
        cart = await CartService.get_or_create_cart(session, user_id)
        
        result = await session.execute(
            select(CartItem).where(CartItem.cart_id == cart.id)
        )
        items = result.scalars().all()
        
        for item in items:
            session.delete(item)
        
        await session.commit()
        return True
    
    @staticmethod
    async def get_cart_total(session: AsyncSession, user_id: int):
        """Savat umumiy narxi"""
        cart = await CartService.get_cart_with_items(session, user_id)
        
        if not cart or not cart.items:
            return 0, 0
        
        total_price = sum(item.product.price * item.quantity for item in cart.items)
        total_items = sum(item.quantity for item in cart.items)
        
        return total_price, total_items


# ========================
# BUYURTMA SERVISLARI
# ========================

class OrderService:
    """Buyurtmalar bilan ishlash"""
    
    @staticmethod
    async def create_order(
        session: AsyncSession,
        user_id: int,
        delivery_address: str,
        notes: str = None
    ):
        """Yangi buyurtma yaratish"""
        cart = await CartService.get_cart_with_items(session, user_id)
        
        if not cart or not cart.items:
            return None
        
        # Umumiy narxi va mahsulot soni
        total_price = sum(item.product.price * item.quantity for item in cart.items)
        item_count = sum(item.quantity for item in cart.items)
        
        order = Order(
            user_id=user_id,
            delivery_address=delivery_address,
            notes=notes,
            total_price=total_price,
            item_count=item_count,
            status="yangi"
        )
        session.add(order)
        await session.flush()  # ID olish uchun
        
        # Buyurtma mahsulotlarini qo'shish
        for cart_item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price_at_purchase=cart_item.product.price
            )
            session.add(order_item)
        
        # Savatni bo'shash
        await CartService.clear_cart(session, user_id)
        
        await session.commit()
        await session.refresh(order)
        
        return order
    
    @staticmethod
    async def get_user_orders(session: AsyncSession, user_id: int):
        """Foydalanuvchining buyurtmalari"""
        result = await session.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .order_by(desc(Order.created_at))
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_order_by_id(session: AsyncSession, order_id: int):
        """ID bo'yicha buyurtma"""
        result = await session.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_order_status(
        session: AsyncSession,
        order_id: int,
        status: str
    ):
        """Buyurtma statusini yangilash"""
        result = await session.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()
        
        if order:
            order.status = status
            order.updated_at = datetime.now()
            await session.commit()
            await session.refresh(order)
        
        return order
    
    @staticmethod
    async def cancel_order(session: AsyncSession, order_id: int):
        """Buyurtmani bekor qilish"""
        return await OrderService.update_order_status(
            session, order_id, "bekor_qilingan"
        )


# ========================
# SHARH SERVISLARI
# ========================

class ReviewService:
    """Sharhlar va reytinglar bilan ishlash"""
    
    @staticmethod
    async def add_review(
        session: AsyncSession,
        product_id: int,
        user_id: int,
        rating: int,
        comment: str = None
    ):
        """Sharh qo'shish"""
        review = Review(
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            comment=comment
        )
        session.add(review)
        await session.commit()
        await session.refresh(review)
        return review
    
    @staticmethod
    async def get_product_reviews(session: AsyncSession, product_id: int):
        """Mahsulotning sharhlarini olish"""
        result = await session.execute(
            select(Review)
            .where(Review.product_id == product_id)
            .options(selectinload(Review.user))
            .order_by(desc(Review.created_at))
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_average_rating(session: AsyncSession, product_id: int):
        """Mahsulotning o'rtacha reytingi"""
        result = await session.execute(
            select(func.avg(Review.rating))
            .where(Review.product_id == product_id)
        )
        avg = result.scalar()
        return round(avg, 1) if avg else 0
    
    @staticmethod
    async def get_user_reviews(session: AsyncSession, user_id: int):
        """Foydalanuvchining sharhlarini olish"""
        result = await session.execute(
            select(Review)
            .where(Review.user_id == user_id)
            .options(selectinload(Review.product))
            .order_by(desc(Review.created_at))
        )
        return result.scalars().all()


# ========================
# TO'LOV SERVISLARI
# ========================

class PaymentService:
    """To'lovlar bilan ishlash"""
    
    @staticmethod
    async def create_payment(
        session: AsyncSession,
        order_id: int,
        user_id: int,
        amount: float,
        payment_method: str,
        currency: str = "UZS"
    ):
        """Yangi to'lov yaratish"""
        payment = Payment(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            status="kutilmoqda"
        )
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment
    
    @staticmethod
    async def get_payment_by_order_id(session: AsyncSession, order_id: int):
        """Buyurtma bo'yicha to'lov"""
        result = await session.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_payment_status(
        session: AsyncSession,
        payment_id: int,
        status: str,
        transaction_id: str = None
    ):
        """To'lov statusini yangilash"""
        result = await session.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        payment = result.scalar_one_or_none()
        
        if payment:
            payment.status = status
            if transaction_id:
                payment.transaction_id = transaction_id
            payment.updated_at = datetime.now()
            await session.commit()
            await session.refresh(payment)
        
        return payment


# ========================
# STATISTIKA SERVISLARI
# ========================

class StatisticsService:
    """Statistika va hisobtash servislari"""
    
    @staticmethod
    async def get_total_products(session: AsyncSession):
        """Jami mahsulotlar soni"""
        result = await session.execute(
            select(func.count(Product.id))
        )
        return result.scalar() or 0
    
    @staticmethod
    async def get_total_users(session: AsyncSession):
        """Jami foydalanuvchilar soni"""
        result = await session.execute(
            select(func.count(User.id))
        )
        return result.scalar() or 0
    
    @staticmethod
    async def get_total_orders(session: AsyncSession):
        """Jami buyurtmalar soni"""
        result = await session.execute(
            select(func.count(Order.id))
        )
        return result.scalar() or 0
    
    @staticmethod
    async def get_total_revenue(session: AsyncSession):
        """Jami daromad"""
        result = await session.execute(
            select(func.sum(Order.total_price))
        )
        return result.scalar() or 0
    
    @staticmethod
    async def get_pending_orders(session: AsyncSession):
        """Tasdiqlanmagan buyurtmalar"""
        result = await session.execute(
            select(func.count(Order.id))
            .where(Order.status == "yangi")
        )
        return result.scalar() or 0
