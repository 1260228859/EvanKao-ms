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

commodity_bp = Blueprint('commodity', url_prefix='commoditys')


@logger()
async def get_user_by_id(request, id):
    cli = request.app.role_client.cli(request)
    async with cli.get('users/{}'.format(id)) as res:
        return await res.json()


# @pay_bp.get('/<id:int>', name="get_order")
# @doc.summary("get order info")
# @doc.produces(Pay)
# async def get_order(request, id):
#     async with request.app.db.acquire(request) as cur:
#         # FIXME
#         records = await cur.fetch(
#             """ SELECT * FROM users WHERE id = $1 """, id)
#         # print('>>>', records)
#         # records = records[0]
#         # datas = [
#         #     # [records, 'city_id', get_city_by_id(request, records['city_id'])],
#         #     [records, 'user_id', get_user_by_id(request, records['user_id'])]
#         # ]
#         # await async_request(datas)
#         return records
#
#
# @order_bp.post('/', name="create_user")
# @doc.summary('create order')
# @doc.description('create order info')
# @doc.consumes(Order)
# async def create_user(request):
#     data = request['data']
#     async with request.app.db.transaction(request) as cur:
#         record = await cur.fetchrow(
#             """ INSERT INTO orders(name, age, role_id)
#                 VALUES($1, $2, $3)
#                 RETURNING id
#             """, data['name'], data['amount_fee'], data['role_id']
#         )
#
#         # TODO:
#         # 发送订单创建事件
#         event_dispatcher = EventDispatcher()
#         event_dispatcher('order_created', {
#             'order': order,
#         })
#
#         return {'id': record['id']}

