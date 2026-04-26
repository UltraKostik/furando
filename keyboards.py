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
        [KeyboardButton(text="❤️ Лайк"), KeyboardButton(text="⚠️ Пожаловаться"), KeyboardButton(text="👎 Дизлайк")],
        [KeyboardButton(text="⏩ Дальше")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оцените кружок"
)

comment_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✍️ Оставить комментарий")],
        [KeyboardButton(text="⏩ Пропустить")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оставьте комментарий или пропустите"
)