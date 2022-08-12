from typing import List


class ShowMazeGeneration:
    TRUE = "True"
    FALSE = "False"

    @classmethod
    def list(cls) -> List[bool]:
        return [
            cls.TRUE,
            cls.FALSE,
        ]
