from typing import List


class WindowWidth:
    W_500 = "500"
    W_600 = "600"
    W_800 = "800"

    @classmethod
    def list(cls) -> List[str]:
        return [
            cls.W_500,
            cls.W_600,
            cls.W_800,
        ]


class WindowHeight:
    H_600 = "600"
    H_800 = "800"

    @classmethod
    def list(cls) -> List[str]:
        return [
            cls.H_600,
            cls.H_800,
        ]
