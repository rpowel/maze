import peewee as pw

from common.path import get_resource_path

db = pw.SqliteDatabase(get_resource_path("data/maze_db.db"))


class BaseModel(pw.Model):
    class Meta:
        database = db
