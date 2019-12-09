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


class Merchant(Model):
    id = PrimaryKeyField()  # 改为objectid 主健
    create_time = DateTimeField(verbose_name='create time', default=datetime.datetime.utcnow)
    name = CharField(max_length=128, verbose_name="商户名称")

    class Meta:
        table_name = 'merchant'
