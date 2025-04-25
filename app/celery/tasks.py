import asyncio
from celery import shared_task
from celery.schedules import crontab
from sqlalchemy import select, update, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.celery import celery_app
from app.db.session import sessionmanager
from app.db.redis import redis_db
from app.models.advertisement import Advertisement
from app.models.user import User


@celery_app.task
def update_ads_views():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_update_ads_views())
    loop.close()


async def _update_ads_views():
    async with sessionmanager.session() as session:
        try:

            #Get all ads from db
            query = select(Advertisement.id).where(Advertisement.active.is_(True))
            result = await session.execute(query)
            ads = result.scalars().all()
            if not ads:
                return

            # Get view counts from redis
            views_ads = await get_redis_views(ads)
            if not views_ads:
                return

            await bulk_update_ads_views(views_ads, session)
            await redis_db.flushdb()
        except Exception:
            await session.rollback()
            raise


async def get_redis_views(ads_ids: list) -> dict:
    redis_pipeline = redis_db.pipeline()
    for ad_id in ads_ids:
        redis_pipeline.scard(ad_id)

    views_data = await redis_pipeline.execute()

    return {ad_id: count for ad_id, count in zip(ads_ids, views_data) if count}


async def bulk_update_ads_views(view_ads: dict, session: AsyncSession):
    query = update(Advertisement)\
        .where(Advertisement.id.in_(view_ads.keys()))\
        .values(
        views=Advertisement.views + case({
            ad_id: count for ad_id, count in view_ads.items()},     # Need to be a mapping
            value=Advertisement.id,     # Specify row to check for update
            else_=Advertisement.views or 0
        )
    )
    await session.execute(query)
    await session.commit()
