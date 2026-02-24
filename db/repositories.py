from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from db.models import Category, Product, User, Cart, CartItem, Order, OrderItem

# ============ КАТЕГОРИИ ============


class CategoryRepository:
    @staticmethod
    async def get_all(session: AsyncSession):
        """Получить все категории"""
        result = await session.execute(select(Category))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(session: AsyncSession, category_id: int):
        """Получить категорию по ID"""
        result = await session.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(session: AsyncSession, name_uz: str, description: str = None, image_url: str = None):
        """Создать новую категорию"""
        category = Category(name_uz=name_uz, description=description, image_url=image_url)
        session.add(category)
        await session.commit()
        return category


# ============ ТОВАРЫ ============


class ProductRepository:
    @staticmethod
    async def get_all(session: AsyncSession):
        """Получить все товары"""
        result = await session.execute(select(Product).where(Product.is_active == True))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(session: AsyncSession, product_id: int):
        """Получить товар по ID"""
        result = await session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_category(session: AsyncSession, category_id: int):
        """Получить товары по категории"""
        result = await session.execute(
            select(Product).where(
                and_(
                    Product.category_id == category_id,
                    Product.is_active == True
                )
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_top_sales(session: AsyncSession, limit: int = 10):
        """Получить топ продаж"""
        result = await session.execute(
            select(Product)
            .where(Product.is_active == True)
            .order_by(desc(Product.sales_count))
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def create(session: AsyncSession, name_uz: str, price: float, category_id: int,
                     description_uz: str = None, image_url: str = None, stock: int = 100):
        """Создать новый товар"""
        product = Product(
            name_uz=name_uz,
            price=price,
            category_id=category_id,
            description_uz=description_uz,
            image_url=image_url,
            stock=stock
        )
        session.add(product)
        await session.commit()
        return product

    @staticmethod
    async def update_stock(session: AsyncSession, product_id: int, quantity: int):
        """Обновить остаток товара"""
        product = await ProductRepository.get_by_id(session, product_id)
        if product:
            product.stock -= quantity
            await session.commit()
        return product

    @staticmethod
    async def increase_sales(session: AsyncSession, product_id: int, quantity: int):
        """Увеличить количество продаж"""
        product = await ProductRepository.get_by_id(session, product_id)
        if product:
            product.sales_count += quantity
            await session.commit()
        return product


# ============ ПОЛЬЗОВАТЕЛИ ============


class UserRepository:
    @staticmethod
    async def get_by_telegram_id(session: AsyncSession, telegram_id: int):
        """Получить пользователя по ID Telegram"""
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(session: AsyncSession, telegram_id: int, first_name: str = None, last_name: str = None):
        """Создать нового пользователя"""
        user = User(telegram_id=telegram_id, first_name=first_name, last_name=last_name)
        session.add(user)
        await session.commit()
        return user

    @staticmethod
    async def update(session: AsyncSession, telegram_id: int, **kwargs):
        """Обновить данные пользователя"""
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            await session.commit()
        return user

    @staticmethod
    async def get_or_create(session: AsyncSession, telegram_id: int, first_name: str = None):
        """Получить пользователя или создать"""
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if not user:
            user = await UserRepository.create(session, telegram_id, first_name)
        return user


# ============ КОРЗИНА ============


class CartRepository:
    @staticmethod
    async def get_or_create(session: AsyncSession, user_id: int):
        """Получить или создать корзину"""
        result = await session.execute(select(Cart).where(Cart.user_id == user_id))
        cart = result.scalar_one_or_none()
        if not cart:
            cart = Cart(user_id=user_id)
            session.add(cart)
            await session.commit()
        return cart

    @staticmethod
    async def get_with_items(session: AsyncSession, user_id: int):
        """Получить корзину с товарами"""
        cart = await CartRepository.get_or_create(session, user_id)
        # Обновим сессию, чтобы загрузить отношения
        await session.refresh(cart)
        return cart

    @staticmethod
    async def add_item(session: AsyncSession, user_id: int, product_id: int, quantity: int = 1):
        """Добавить товар в корзину"""
        cart = await CartRepository.get_or_create(session, user_id)
        
        # Проверим, есть ли уже такой товар
        result = await session.execute(
            select(CartItem).where(
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
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            session.add(cart_item)
        
        await session.commit()
        return cart_item

    @staticmethod
    async def remove_item(session: AsyncSession, cart_item_id: int):
        """Удалить товар из корзины"""
        result = await session.execute(select(CartItem).where(CartItem.id == cart_item_id))
        cart_item = result.scalar_one_or_none()
        if cart_item:
            await session.delete(cart_item)
            await session.commit()
        return cart_item

    @staticmethod
    async def clear(session: AsyncSession, user_id: int):
        """Очистить корзину"""
        cart = await CartRepository.get_or_create(session, user_id)
        await session.execute(select(CartItem).where(CartItem.cart_id == cart.id))
        result = await session.execute(select(CartItem).where(CartItem.cart_id == cart.id))
        items = result.scalars().all()
        for item in items:
            await session.delete(item)
        await session.commit()


# ============ ЗАКАЗЫ ============


class OrderRepository:
    @staticmethod
    async def create(session: AsyncSession, user_id: int, delivery_address: str = None, notes: str = None):
        """Создать заказ"""
        order = Order(user_id=user_id, delivery_address=delivery_address, notes=notes, status="yangi")
        session.add(order)
        await session.commit()
        return order

    @staticmethod
    async def get_by_id(session: AsyncSession, order_id: int):
        """Получить заказ по ID"""
        result = await session.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_orders(session: AsyncSession, user_id: int):
        """Получить все заказы пользователя"""
        result = await session.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(desc(Order.created_at))
        )
        return result.scalars().all()

    @staticmethod
    async def add_item(session: AsyncSession, order_id: int, product_id: int, quantity: int, price: float):
        """Добавить товар в заказ"""
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_at_purchase=price
        )
        session.add(order_item)
        
        # Обновим резюме заказа
        order = await OrderRepository.get_by_id(session, order_id)
        order.item_count += quantity
        order.total_price += price * quantity
        
        await session.commit()
        return order_item

    @staticmethod
    async def update_status(session: AsyncSession, order_id: int, status: str):
        """Обновить статус заказа"""
        order = await OrderRepository.get_by_id(session, order_id)
        if order:
            order.status = status
            await session.commit()
        return order

    @staticmethod
    async def get_with_items(session: AsyncSession, order_id: int):
        """Получить заказ с товарами"""
        order = await OrderRepository.get_by_id(session, order_id)
        if order:
            await session.refresh(order)
        return order
