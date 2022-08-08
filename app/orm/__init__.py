from .scores import Scores

__all__ = [
    "Scores",
]

for table in __all__:
    local_ = locals()
    local_[table].create_table(safe=True)
