import logging
import ujson
import time
import asyncio
import datetime
import uuid

from sanic import Blueprint

from sanicms import doc
from sanicms.redis_status_helps.status import plus_counter, create_order_map
from sanicms.utils import *
from sanicms.exception import ServerError
from nameko.events import EventDispatcher
from nameko.events import event_handler
from sanicms.loggers import logger
from models import *

_logger = logging.getLogger('sanic')

commodity_bp = Blueprint('commodity', url_prefix='commoditys')


@logger()
async def get_user_by_id(request, id):
    cli = request.app.role_client.cli(request)
    async with cli.get('users/{}'.format(id)) as res:
        return await res.json()


@commodity_bp.post('/', name="purchase")
@doc.summary('商品抢购接口')
@doc.description('库存增减创建订单')
@doc.consumes(Commodity)
async def create_user(request):
    res = {
        "status": False,
        "msg": ""
    }

    data = request['data']
    user_id = data.get('user_id')
    commodity_id = data.get('commodity_id')

    """

        流程：
        1. redis计数器判断
            - 计数器设置为库存数量
            - 当超过计数器时，直接返回失败。
        2. 通过计数器的订单获得一个唯一标识
            - 将用户-标识 写入redis
            - 写入订单队列 + 超时队列

    :return: 返回状态 + 标识
    """

    # 计数器
    flag = plus_counter(commodity_id)
    # 成功申请
    if not flag:
        res['msg'] = '商品已售毕'
        return res

    # 判断用户是否存在
    record = await get_user_by_id(request, user_id)
    if not record:
        res['msg'] = '用户不存在'
        return res

    # 生成唯一的订单号
    order_id = uuid.uuid1()

    order_info = {
        "commodity_id": commodity_id,
        "user_id": user_id,
        "order_id": str(order_id)
    }
    # order_info = str(goods_id) + ',' + str(user_id) + ',' + str(order_id)
    try:
        create_order_map(order_info)

        # 发送商品扣库存成功事件
        event_dispatcher = EventDispatcher()
        event_dispatcher('order_created', {
            'order': order_info,
        })

        res["status"] = True
        res["data"] = order_info
        return res

    except Exception as e:
        print("log: ", e)
        res["status"] = False
        res["msg"] = "抢购出错，请重试." + str(e)
        return res


@event_handler('orders', 'order_created')
def handle_order_created(payload):
    print(payload)
    order_info =  payload['order']
    logger.error(f'=====order_info=={order_info}=======')
