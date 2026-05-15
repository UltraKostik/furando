#Telegram бот Фурандо, Furando. Разработчик @UltraKostik

from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums import ContentType
from time import ctime
import keyboards as kb
import logging
import database as db

router = Router()
logger = logging.getLogger(__name__)

class CommentState(StatesGroup):
    waiting_for_comment = State()
    waiting_for_activity = State()

@router.message(F.text == "/start")
async def handle_start(message: Message, state: FSMContext):
    try:
        await state.clear()
        await message.answer(
            "Привет! Я Фурандо! 🦊\n\n"
            "Умный бот для обмена видеокружками. "
            f"Отправь мне свой кружок — получишь случайный из общей коллекции (уже {await db.get_stats_video_note()} видеокружков).\n\n"
            "<b>🎲 /get — получить случайный кружок</b>",
            reply_markup=kb.main_keyboard,  
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer("⚠️ Произошла ошибка. Пожалуйста, попробуйте позже.")
        logger.exception(f"[{ctime()}]. Ошибка в handle_start: {type(e).__name__}: {e}")
        
@router.message(F.text.in_(["/get", "🎲 Погнали", "⏩ Дальше"]))
async def handle_get_random_video_note(message: Message, state: FSMContext):
    try:
        result = await db.get_random_video_with_stats()
        if result:
            file_id, comment, username, likes, views = result
            author_name = '@'+username if username else "Безымянный автор"
            await state.update_data(current_file_id=file_id)
            await message.answer_video_note(file_id, reply_markup=kb.video_note_keyboard)
            if comment:
                await message.answer(f"❤️ Лайки: {likes}\n👁️ Просмотры: {views}\n🗿 Автор: {author_name}\n\n💬 Комментарий автора:\n\n \"{comment}\"")
            else:
                await message.answer(f"❤️ Лайки: {likes}\n👁️ Просмотры: {views}\n🗿 Автор: {author_name}\n\n💬 Комментарий автора:\n\n <i>Комментария нет</i>", parse_mode="HTML")
            await db.increment_views(file_id)
            await state.set_state(CommentState.waiting_for_activity)
        else:
            await message.answer(
                "❌ Пока видеокружков для вас нет!\n"
                "Не стесняйтесь, а отправьте свой видеокружок!"
            )
            await state.clear()
    except Exception as e:
        await message.answer("⚠️ Произошла ошибка. Пожалуйста, попробуйте позже.")
        logger.exception(f"[{ctime()}]. Ошибка в handle_get_random_video_note: {type(e).__name__}: {e}")

@router.message(F.content_type == ContentType.VIDEO_NOTE)
async def handle_save_video_note(message: Message, state: FSMContext):
    try:
        await state.update_data(
            file_id=message.video_note.file_id,
            user_id=message.from_user.id,
            username=message.from_user.username
        )
        await message.answer(
            "✍️ Не хотите ли вы оставить комментарий под видеокружком?\n\n"
            "Расскажите про себя или как снимался видеокружок\n\n"
            "<b>⚠️ Комментарий не должен быть больше 500 символов и не должен нарушать политику конфиденциальности, "
            "законодательство РФ или содержать рекламный материал!</b>",
            reply_markup=kb.comment_keyboard,
            parse_mode="HTML"
        )
        await state.set_state(CommentState.waiting_for_comment)
    except Exception as e:
        await message.answer("❌ Ошибка при получении кружка.")
        logger.exception(f"[{ctime()}]. Ошибка в handle_save_video_note: {type(e).__name__}: {e}")
        
#Хендлеры для комментариев
        
@router.message(CommentState.waiting_for_comment, F.text == "❌ Отмена")
async def not_send_video_note(message: Message, state: FSMContext):
    await message.answer("Отправление видеокружка отменено", reply_markup=kb.main_keyboard)
    await state.clear()
    await db.get_stats_video_note()
        
@router.message(CommentState.waiting_for_comment, F.text == "✍️ Оставить комментарий")
async def ask_for_comment(message: Message, state: FSMContext):
    await message.answer("✍️ Напишите ваш комментарий:", reply_markup=kb.comment_keyboard_notext)
    
@router.message(CommentState.waiting_for_comment, F.text.in_(["⏩ Пропустить", "⏩ Пропустить комментарий"]))
async def skip_comment(message: Message, state: FSMContext): 
    data = await state.get_data()
    file_id = data.get("file_id")
    user_id = data.get("user_id")
    username = data.get("username")
    await db.save_video_note(user_id=user_id, file_id=file_id, username=username)
    await message.answer("✅ Кружок сохранён без комментария!", reply_markup=kb.main_keyboard)
    await state.clear()

@router.message(CommentState.waiting_for_comment)
async def save_with_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    file_id = data.get("file_id")
    user_id = data.get("user_id")
    username = data.get("username")
    comment = message.text.strip()[:500]
    await db.save_video_note(user_id=user_id, file_id=file_id, comment=comment, username=username)
    await message.answer(f"✅ Кружок сохранён с комментарием!\n💬 \"{comment}\"", reply_markup=kb.main_keyboard)
    await state.clear()

#Хендлеры для взаимодейсвтия с карточками кружков

@router.message(CommentState.waiting_for_activity, F.text == "❤️")
async def send_like(message: Message, state: FSMContext):
    data = await state.get_data()
    current_file_id = data.get("current_file_id")
    if current_file_id:
        await db.increment_likes(current_file_id)
        await message.answer("❤️ Лайк отправлен!")
        await handle_get_random_video_note(message, state)

@router.message(CommentState.waiting_for_activity, F.text == "⚠️")
async def send_warning(message: Message, state: FSMContext):
    pass

@router.message(CommentState.waiting_for_activity, F.text == "😴")
async def send_sleep(message: Message, state: FSMContext):
    await message.answer("🔙 Возврат в главное меню")
    await handle_start(message, state)

@router.message(CommentState.waiting_for_activity, F.text == "👎")
async def send_dislike(message: Message, state: FSMContext):
    pass