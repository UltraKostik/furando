#Telegram бот Фурандо, Furando. Разработчик @UltraKostik#

import logging
from time import ctime, time
from sqlalchemy import Integer, String, Column, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, func

engine = create_async_engine('sqlite+aiosqlite:///furando.db', echo=True)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

class VideoNote(Base):
    __tablename__ = 'video_notes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    file_id = Column(String, unique=True, nullable=False)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    username = Column(String, nullable=True)
    comment = Column(String, nullable=True)

class PremiumSubscription(Base):
    __tablename__ = 'premium_subscriptions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    end_date = Column(Integer, nullable=False)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в init_db: {type(e).__name__}: {e}")
        
async def save_video_note(user_id: int, username: str = None, file_id: str = None, comment: str = None):
    try:
        async with async_session_maker() as session:
            video = VideoNote(
                user_id = user_id,
                username = username,
                file_id = file_id,
                comment = comment
            )
            session.add(video)
            await session.commit()
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в save_video_note: {type(e).__name__}: {e}")

async def get_random_video_with_stats() -> tuple[str, str | None, str | None, int, int] | None:
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(VideoNote.file_id, VideoNote.comment, VideoNote.username, VideoNote.likes, VideoNote.views).order_by(func.random()).limit(1))
            return result.first()
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в get_random_video_with_stats: {type(e).__name__}: {e}")

async def get_video_stats(file_id: str) -> tuple[int, int, str | None, str | None] | None:
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(VideoNote.file_id, VideoNote.comment, VideoNote.username, VideoNote.likes, VideoNote.views).where(VideoNote.file_id == file_id))
            return result.first()
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в get_video_stats: {type(e).__name__}: {e}")

async def get_stats_video_note() -> int:
    try:
        async with async_session_maker() as session:
            result = await session.execute(func.count(VideoNote.id))
            return result.scalar() or 0
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в get_stats_video_note: {type(e).__name__}: {e}")

async def increment_views(file_id: str):
    try:
        async with async_session_maker() as session:
            await session.execute(
                update(VideoNote)
                .where(VideoNote.file_id == file_id)
                .values(views=VideoNote.views + 1)
            )
            await session.commit()
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в increment_views: {type(e).__name__}: {e}")

async def increment_likes(file_id:str):
    try:
        async with async_session_maker() as session:
            await session.execute(
                update(VideoNote)
                .where(VideoNote.file_id == file_id)
                .values(likes=VideoNote.likes + 1)
            )
            await session.commit()
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в increment_likes: {type(e).__name__}: {e}")
        
#Хендлеры для работы с premium-подпиской 

async def save_premium_subscription(user_id: int, username: str | None, end_date: int):
    try:
        async with async_session_maker() as session:
            existing = await session.execute(select(PremiumSubscription).where(PremiumSubscription.user_id == user_id))
            existing_sub = existing.scalar_one_or_none()
            
            if existing_sub:
                existing_sub.end_date = end_date
                existing_sub.username = username
            else:
                subscription = PremiumSubscription(
                    user_id=user_id,
                    username=username,
                    end_date=end_date
                )
                session.add(subscription)
            
            await session.commit()
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в save_premium_subscription: {type(e).__name__}: {e}")

async def is_premium(user_id: int) -> bool:
    try:
        async with async_session_maker() as session:
            result = await session.execute(
                select(PremiumSubscription).where(
                    PremiumSubscription.user_id == user_id,
                    PremiumSubscription.end_date > int(time.time())
                )
            )
            return result.scalar_one_or_none() is not None
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в is_premium: {type(e).__name__}: {e}")
        return False