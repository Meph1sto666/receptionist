from peewee import *

from model.base_model import BaseModel


class User(BaseModel):
    id = IntegerField(primary_key=True)
    invites = IntegerField()
    timezone = IntegerField()
    invite_permission = BooleanField()
    allow_ping = BooleanField()
    language = TextField()
