import datetime
from bson import ObjectId

from peewee import (
    Model,
    DateTimeField,
    IntegerField,
    PrimaryKeyField,
    CharField
)
from sanicms import doc


class UserApi:
    id = int
    name = doc.String('name')


class Order(Model):
    id = PrimaryKeyField()  # 改为objectid 主健
    create_time = DateTimeField(verbose_name='create time', default=datetime.datetime.utcnow)
    name = CharField(max_length=128, verbose_name="订单名称")
    amount_fee = IntegerField(null=False, verbose_name="订单金额分")
    order_num = CharField(null=False, unique=True, max_length=32, verbose_name="order uuid unique num")
    user_id = IntegerField(verbose_name='order for user', help_text=UserApi)

    class Meta:
        table_name = 'order'
