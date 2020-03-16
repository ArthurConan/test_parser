import jinja2
import aiohttp_jinja2

from aiohttp import web
from aiojobs.aiohttp import setup as aiojobs_setup
from aioredis import create_redis_pool

from config import settings
from config.routes import routes


async def startup(app):
    """
    Create connection to redis for existed application
    :param app: instance of application
    :return:
    """
    app['redis'] = await create_redis_pool(settings.REDIS_URL, encoding='utf-8')


async def cleanup(app):
    """
    Close connection to redis
    :param app: instance of application
    :return:
    """
    app['redis'].close()
    await app['redis'].wait_closed()


async def create_app():
    """
    Create web application and manage connection to redis
    :return: instance of application
    """
    app = web.Application()
    jinja_env = aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    for route in routes:
        app.router.add_route(**route)
    startup_tasks = [startup]
    app.on_startup.extend(startup_tasks)
    app.on_cleanup.append(cleanup)
    aiojobs_setup(app)
    return app


if __name__ == '__main__':
    web.run_app(create_app(), host=settings.HOST, port=settings.PORT)
