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


class Commodity(Model):
    id = PrimaryKeyField()  # 改为objectid 主健
    create_time = DateTimeField(verbose_name='create time', default=datetime.datetime.utcnow)
    name = CharField(max_length=128, verbose_name="商品名称")
    amount = IntegerField(null=False, verbose_name="商品数量")
    price_fee = IntegerField(null=False, verbose_name="商品金额分")

    class Meta:
        table_name = 'commodity'
