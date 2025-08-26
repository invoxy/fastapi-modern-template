from uuid import uuid4


def get_random_filename(filename: str) -> str:
    if "." in filename:
        name, *ext = filename.split(".")
        return f"{name}-{uuid4()}.{'.'.join(ext)}"
    return f"{filename}-{uuid4()}"
