from typing import List


class MazeSizes:
    N_10 = "10"
    N_20 = "20"
    N_30 = "30"
    N_40 = "40"
    N_50 = "50"

    @classmethod
    def list(cls) -> List[str]:
        return [
            cls.N_10,
            cls.N_20,
            cls.N_30,
            cls.N_40,
            cls.N_50,
        ]
