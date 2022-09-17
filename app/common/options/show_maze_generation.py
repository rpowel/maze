from typing import List


class ShowMazeGeneration:
    TRUE = "True"
    FALSE = "False"

    @classmethod
    def list(cls) -> List[str]:
        return [
            cls.TRUE,
            cls.FALSE,
        ]
