from .scores import Scores

__all__ = [
    "Scores",
]

for table in __all__:
    table.create_table(safe=True)
