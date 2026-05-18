# Telegram бот Фурандо, Furando. Разработчик @UltraKostik

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎲 Погнали")],
        [KeyboardButton(text="💸 Premium")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажмите кнопку"
)

video_note_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❤️"), KeyboardButton(text="⚠️"), KeyboardButton(text="👎"), KeyboardButton(text="😴")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оцените кружок"
)

money_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1 день • 39 ⭐"), KeyboardButton(text="7 дней • 89 ⭐")],
        [KeyboardButton(text="30 дней • 169 ⭐"), KeyboardButton(text="90 дней • 349 ⭐🔥")],
        [KeyboardButton(text="180 дней • 499 ⭐🔥"), KeyboardButton(text="365 дней • 899 ⭐🔥")],
        [KeyboardButton(text="🤗 Патроны проекта")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите тариф"
)

back_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Вернуться назад"
)

comment_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✍️ Оставить комментарий")],
        [KeyboardButton(text="⏩ Пропустить")],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оставьте комментарий или пропустите"
)

warning_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⚠️ Насилие"), KeyboardButton(text="⚠️ Незаконные товары")],
        [KeyboardButton(text="⚠️ Порнография"), KeyboardButton(text="⚠️ Мошенничество")],
        [KeyboardButton(text="⚠️ Персональные данные")],
        [KeyboardButton(text="⚠️ Нарушение авторских прав")],
        [KeyboardButton(text="⚠️ Другое")],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите причину жалобы"
)

comment_keyboard_notext = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⏩ Пропустить комментарий")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Пропустить комментарий"
)