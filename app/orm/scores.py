import peewee as pw

from .base import BaseModel


class Scores(BaseModel):
    score_id = pw.AutoField()
    maze_type = pw.CharField()
    size_x = pw.IntegerField()
    size_y = pw.IntegerField()
    time_seconds = pw.IntegerField()
    timestamp = pw.TimestampField()
