import os


def get_resource_path(relative_path):
    base_path = os.path.join(
        os.path.abspath(__file__),
        os.path.pardir,
        os.path.pardir,
    )

    return os.path.join(base_path, relative_path)
