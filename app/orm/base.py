import peewee as pw

db = pw.SqliteDatabase("data/maze_db.db")


class BaseModel(pw.Model):
    class Meta:
        database = db
