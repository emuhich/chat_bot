from tgbot.models.db_gino import User, Sessions


async def create_user(user_id: int, username: str, is_active: bool, is_password: bool):
    user = User(id=user_id, username=username, is_active=is_active, is_password=is_password)
    await user.create()


async def delete_user(user_id: int):
    await User.delete.where(User.id == user_id).gino.status()


async def get_user(user_id):
    return await User.query.where(User.id == user_id).gino.first()


async def get_session(user_id):
    return await Sessions.query.where(Sessions.user_id == user_id).gino.first()


async def create_session(user_id):
    session = Sessions(user_id=user_id)
    await session.create()
