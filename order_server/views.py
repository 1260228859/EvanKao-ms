import logging
import ujson
import time
import asyncio
import datetime

from sanic import Blueprint

from sanicms import doc
from sanicms.utils import *
from sanicms.exception import ServerError
from sanicms.loggers import logger
from models import *

_logger = logging.getLogger('sanic')

order_bp = Blueprint('order', url_prefix='orders')

@logger()
async def get_user_by_id(request, id):
    cli = request.app.role_client.cli(request)
    async with cli.get('users/{}'.format(id)) as res:
        return await res.json()


@order_bp.get('/<id:int>', name="get_order")
@doc.summary("get order info")
@doc.produces(Order)
async def get_order(request, id):
    async with request.app.db.acquire(request) as cur:
        # FIXME
        records = await cur.fetch(
            """ SELECT * FROM users WHERE id = $1 """, id)
        # print('>>>', records)
        # records = records[0]
        # datas = [
        #     # [records, 'city_id', get_city_by_id(request, records['city_id'])],
        #     [records, 'user_id', get_user_by_id(request, records['user_id'])]
        # ]
        # await async_request(datas)
        return records
