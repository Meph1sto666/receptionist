from peewee import *

from model.base_model import BaseModel
from model.user import User


class PingRule(BaseModel):
    id = AutoField(primary_key=True)
    start = DateTimeField()
    end = DateTimeField()
    creation_time = TextField()
    user_id = ForeignKeyField(User, backref="ping_rules", null=False)
