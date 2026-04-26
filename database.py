#Telegram бот Фурандо, Furando. Разработчик @UltraKostik#

import logging
from time import ctime
from sqlalchemy import Integer, String, Column
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
    comment = Column(String, nullable=True)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в init_db: {type(e).__name__}: {e}")
        
async def save_video_note(user_id: int, file_id: str, comment: str = None):
    try:
        async with async_session_maker() as session:
            video = VideoNote(
                user_id = user_id,
                file_id = file_id,
                comment = comment
            )
            session.add(video)
            await session.commit()
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в save_video_note: {type(e).__name__}: {e}")

async def get_random_video_note() -> tuple[str, str | None] | None:
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(VideoNote.file_id, VideoNote.comment).order_by(func.random()).limit(1))
            return result.first()
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в get_random_video_note: {type(e).__name__}: {e}")

async def get_stats_video_note() -> int:
    try:
        async with async_session_maker() as session:
            result = await session.execute(func.count(VideoNote.id))
            return result.scalar() or 0
    except Exception as e:
        logger.exception(f"[{ctime()}]. Ошибка в get_stats_video_note: {type(e).__name__}: {e}")