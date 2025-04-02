from starlette.requests import Request

from app.db.redis import redis_db


class ViewCounterMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        x_forwarder_for = request.headers.get("X-Forwarded-For")
        if x_forwarder_for:
            ip_address = x_forwarder_for.split(",")[0]
        else:
            ip_address = request.headers.get("REMOTE_ADDR")

        response = await call_next(request)

        if "api/v1/advertisements/ads/" not in str(request.url.path) or request.method != "GET":
            return response

        ads_id = request.url.path.split("/")[-1]
        if not ads_id.isdigit():
            return response

        redis_db.sadd(ads_id, ip_address)
        await redis_db.aclose()
        return response
