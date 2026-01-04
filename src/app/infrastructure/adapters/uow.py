from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.uow import AbstractUnitOfWork


class Uow(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
