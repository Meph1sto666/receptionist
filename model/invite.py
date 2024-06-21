from peewee import *

from model.base_model import BaseModel
from model.user import User


class Invite(BaseModel):
    id = TextField(primary_key=True)
    created_at = DateTimeField()
    expires_at = DateTimeField()
    max_uses = IntegerField()
    url = TextField()
    user_id = ForeignKeyField(User, backref='invites', null=False)
