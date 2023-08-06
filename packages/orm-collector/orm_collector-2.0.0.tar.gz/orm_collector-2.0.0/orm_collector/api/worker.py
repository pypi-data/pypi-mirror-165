from uvicorn.workers import UvicornWorker

class ORMUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "auto"}
