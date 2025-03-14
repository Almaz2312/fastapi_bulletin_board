from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRegistrationSchema


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.repository = UserRepository(db_session)

    async def register_user(self, data: UserRegistrationSchema):
        user = await self.repository.create_user(data)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_users(self):
        return await self.repository.get_users()

    async def get_user(self, user_id):
        return await self.repository.get_user_by_field(User.id, user_id)
