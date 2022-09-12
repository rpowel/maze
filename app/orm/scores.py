from typing import List, Tuple

import peewee as pw

from .base import BaseModel


class Scores(BaseModel):
    score_id = pw.AutoField()
    maze_type = pw.CharField()
    size_x = pw.IntegerField()
    size_y = pw.IntegerField()
    time_seconds = pw.IntegerField()
    timestamp = pw.TimestampField()

    @classmethod
    def top_n_scores(
        cls,
        maze_type: str = None,
        size_x: int = None,
        size_y: int = None,
        num_limit: int = 10,
    ) -> List[Tuple[str, int, int, str, str]]:
        data_list = []
        data_raw = (
            cls.select(
                cls.maze_type,
                cls.size_x,
                cls.size_y,
                cls.time_seconds,
                cls.timestamp,
            )
            .limit(num_limit)
            .where(
                (cls.maze_type == maze_type) if maze_type else None,
                (cls.size_x == size_x) if size_x else None,
                (cls.size_y == size_y) if size_y else None,
            )
            .order_by(cls.time_seconds)
        )

        for row in data_raw:
            time_sec = row.time_seconds
            time_score = f"{str(time_sec // 60).zfill(2)}:{str(time_sec).zfill(2)}"
            data_list.append(
                (
                    row.maze_type,
                    row.size_x,
                    row.size_y,
                    time_score,
                    row.timestamp.strftime("%Y-%m-%d"),
                )
            )

        return data_list
