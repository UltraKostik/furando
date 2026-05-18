import logging
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
import keyboards as kb

logger = logging.getLogger(__name__)
router = Router()

class PremiumPaymentState(StatesGroup):
    choosing_tariff = State()   
    waiting_for_payment = State()

@router.message(F.text == "💸 Premium")
async def show_premium_info(message: Message, state: FSMContext):
    await message.answer(
        "<b>Активируй Premium</b> – открой новые возможности Фурандо и поддержи проект!\n\n"
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
        "Любая поддержка очень ценна! ❤️",
        parse_mode="HTML",
        reply_markup=kb.money_keyboard
    )
    await state.set_state(PremiumPaymentState.choosing_tariff)

@router.message(F.text == "1 день • 39 ⭐")
async def send_invoice_1_day(message: Message, state: FSMContext):
    prices = [LabeledPrice(label="Premium на 1 день", amount=39)]
    await message.answer_invoice(
        title="⭐ Premium",
        description="Доступ к премиум-возможностям Фурандо на 1 день",
        payload="premium_1day",
        provider_token="",
        currency="XTR",
        prices=prices,
    )
    await state.set_state(PremiumPaymentState.waiting_for_payment)

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(PremiumPaymentState.waiting_for_payment, F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    payment = message.successful_payment
    await message.answer(
        f"✅ Оплата прошла успешно!\n\n"
        f"⭐ Потрачено звезд: {payment.total_amount}\n"
        f"🎉 Premium активирован на 1 день!\n"
        f"Огромное спасибо за поддержку! ❤️",
        parse_mode="HTML",
        reply_markup=kb.back_keyboard
    )
    await state.clear()