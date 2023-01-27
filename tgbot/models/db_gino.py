import datetime
from typing import List

import sqlalchemy as sa
from aiogram import Dispatcher
from gino import Gino
from sqlalchemy import Column, DateTime, sql, BigInteger, String

from tgbot.config import load_config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimeBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(DateTime(True),
                        default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow,
                        server_default=db.func.now())


class User(TimeBaseModel):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    username = Column(String(100), default=None)
    is_active = Column(db.Boolean, default=False)
    is_password = Column(db.Boolean, default=False)

    query: sql.Select


class Sessions(TimeBaseModel):
    __tablename__ = 'session'
    user_id = Column(BigInteger, primary_key=True)
    query: sql.Select


async def on_startup(dispatcher: Dispatcher):
    config = load_config(".env")
    print("Установка связи с PostgreSQL")
    await db.set_bind(f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}")
    print("Готово")
    print("Создаем таблицу")
    await db.gino.create_all()
    print("Готово")
