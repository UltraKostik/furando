from datetime import datetime
import logging
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
import database as db
import keyboards as kb
import time

logger = logging.getLogger(__name__)
router = Router()

class PremiumPaymentState(StatesGroup):
    choosing_tariff = State()   
    waiting_for_payment = State()
    
SECONDS_IN_DAY = 86400
TARIFFS = {
    "1 день": {"days": 1, "amount": 39, "payload": "premium_1day"},
    "7 дней": {"days": 7, "amount": 89, "payload": "premium_7days"},
    "30 дней": {"days": 30, "amount": 169, "payload": "premium_30days"},
    "90 дней": {"days": 90, "amount": 349, "payload": "premium_90days"},
    "180 дней": {"days": 180, "amount": 499, "payload": "premium_180days"},
    "365 дней": {"days": 365, "amount": 899, "payload": "premium_365days"},
}

@router.message(F.text == "💸 Premium")
async def show_premium_info(message: Message, state: FSMContext):
    user_id = message.from_user.id
    is_premium = await db.is_premium(user_id)
    benefits_text = (
        "💫 Уникальный эмодзи-статус (💎) возле ника под карточкой видеокружка\n"
        "💫 Включение ника в список патронов\n"
        "💫 Приоритетные показы видеокружков\n"
        "💫 Увеличенный лимит на количество символов комментариев\n"
        "💫 Увеличенный лимит на количество просмотренных видеокружков в день\n"
        "💫 Увеличенный лимит на количество отправленных видеокружков в день\n\n"
        "🌟 Выбери оптимальный тариф:\n\n"
        "💎 1 день • 39 ⭐\n"
        "💎 7 дней • 89 ⭐\n"
        "💎 30 дней • 169 ⭐\n"
        "💎 90 дней • 349 ⭐ • 🔥 всего ~3,9 ⭐/день\n"
        "💎 180 дней • 499 ⭐ • 🔥 всего ~2,8 ⭐/день\n"
        "💎 365 дней • 899 ⭐ • 🔥 всего ~2,5 ⭐/день\n\n"
        "Любая поддержка очень ценна! ❤️"
    )
    
    if is_premium:
        end_date = await db.get_premium_end_date(user_id)
        end_date_str = datetime.fromtimestamp(end_date).strftime('%d.%m.%Y')
        await message.answer(
            f"⭐ У вас уже активирован Premium! Он доступен до {end_date_str}.\n\n"
            f"Если вы хотите продлить подписку, просто выберите новый тариф.\n\n"
            f"{benefits_text}",
            reply_markup=kb.money_keyboard
        )
    else:
        await message.answer(
            f"<b>Активируй Premium</b> – открой новые возможности Фурандо и поддержи проект!\n\n"
            f"{benefits_text}",
            parse_mode="HTML",
            reply_markup=kb.money_keyboard
        )
    
    await state.set_state(PremiumPaymentState.choosing_tariff)


@router.message(PremiumPaymentState.choosing_tariff, F.text.contains("⭐"))
async def send_invoice(message: Message, state: FSMContext):
    text = message.text
    tariff = None
    for key in TARIFFS:
        if key in text:
            tariff = TARIFFS[key]
            break
    
    if not tariff:
        await message.answer("❌ Неизвестный тариф")
        return
    
    await message.answer_invoice(
        title="⭐ Premium",
        description=f"Доступ к премиум-возможностям Фурандо на {tariff['days']} дней",
        payload=tariff["payload"],
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=f"Premium на {tariff['days']} дней", amount=tariff["amount"])],
    )
    
    end_date = int(time.time()) + tariff["days"] * SECONDS_IN_DAY
    await state.update_data(end_date=end_date)
    await state.set_state(PremiumPaymentState.waiting_for_payment)
    
    
@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(PremiumPaymentState.waiting_for_payment, F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    payment = message.successful_payment
    end_date = (await state.get_data()).get("end_date")
    await message.answer(
        f"✅ Оплата прошла успешно!\n\n"
        f"⭐ Потрачено звезд: {payment.total_amount}\n"
        f"🎉 Premium активирован до {datetime.fromtimestamp(end_date).strftime('%d.%m.%Y')}\n"
        f"Огромное спасибо за поддержку! ❤️",
        parse_mode="HTML",
        reply_markup=kb.back_keyboard
    )
    await db.save_premium_subscription(
        user_id=message.from_user.id,
        username = message.from_user.username,
        end_date = end_date
    )
    await state.clear()