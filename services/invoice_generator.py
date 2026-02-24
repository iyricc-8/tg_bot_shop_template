from datetime import datetime


def generate_invoice(order_id, first_name, last_name, phone, address, total, items):
    """
    Генерирует красивый чек/счет на узбекском языке
    
    Args:
        order_id: ID заказа
        first_name: Имя покупателя
        last_name: Фамилия покупателя
        phone: Номер телефона
        address: Адрес доставки
        total: Общая сумма
        items: Список товаров (список кортежей (название, количество, цена))
    """
    
    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    time_str = now.strftime("%H:%M:%S")
    
    invoice = "╔════════════════════════════════════╗\n"
    invoice += "║        ✨ XARID KVITANSIYASI ✨     ║\n"
    invoice += "║         (СЕРТИФИКАТ ПОКУПКИ)        ║\n"
    invoice += "╚════════════════════════════════════╝\n\n"
    
    invoice += f"<b>📦 Заказ номер:</b> #{order_id}\n"
    invoice += f"<b>📅 Дата:</b> {date_str}\n"
    invoice += f"<b>⏰ Время:</b> {time_str}\n\n"
    
    invoice += "┌─ 👤 ИНФОРМАЦИЯ ПОКУПАТЕЛЯ ─────┐\n"
    invoice += f"│ Имя: {first_name} {last_name}\n"
    invoice += f"│ Телефон: {phone}\n"
    invoice += f"│ Адрес: {address}\n"
    invoice += "└─────────────────────────────────┘\n\n"
    
    invoice += "┌─ 📦 ЗАКАЗАННЫЕ ТОВАРЫ ──────────┐\n"
    invoice += "│                                 │\n"
    
    total_by_items = 0
    for idx, (name, qty, price) in enumerate(items, 1):
        item_total = qty * price
        total_by_items += item_total
        
        # Форматируем строку товара
        invoice += f"│ {idx}. {name}\n"
        invoice += f"│    {qty} × {price:,.0f} = {item_total:,.0f} so'm\n"
    
    invoice += "│                                 │\n"
    invoice += "└─────────────────────────────────┘\n\n"
    
    invoice += "╔═════════════════════════════════╗\n"
    invoice += f"║  💰 ЖАМИ СУММА:  {total:>13,.0f} so'm  ║\n"
    invoice += "╚═════════════════════════════════╝\n\n"
    
    invoice += "📍 <b>ETKAZIP MANZILI:</b>\n"
    invoice += f"{address}\n\n"
    
    invoice += "✅ <b>BUYURTMA QABUL QILINDI!</b>\n\n"
    
    invoice += "📞 <b>TEZKOR ALOQA:</b>\n"
    invoice += "Bizga qo'ng'iroq qiling yoki SMS yuboring:\n"
    invoice += "+998 (XX) XXX-XX-XX\n\n"
    
    invoice += "⭐ Бўюртмангиз учун рахмат! ⭐\n"
    invoice += "Жун ўра шахс сизга қўйидги 24 соат ичида\n"
    invoice += "муносабат ўрнатади!\n\n"
    
    invoice += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    invoice += f"🤖 Автоматический контроль: {order_id}\n"
    
    return invoice
