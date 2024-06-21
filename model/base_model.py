from peewee import *
import os

db = SqliteDatabase(os.getenv("DB_PATH"))


class BaseModel(Model):
    class Meta:
        database = db
