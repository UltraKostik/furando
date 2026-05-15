# Telegram бот Фурандо, Furando. Разработчик @UltraKostik

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎲 Погнали")]
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

comment_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✍️ Оставить комментарий")],
        [KeyboardButton(text="⏩ Пропустить")],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оставьте комментарий или пропустите"
)

comment_keyboard_notext = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⏩ Пропустить комментарий")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Пропустить комментарий"
)