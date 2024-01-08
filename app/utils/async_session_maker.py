from functools import lru_cache
from importlib import import_module

main_module = import_module("app.main")


@lru_cache
def get_async_session_maker():
    return main_module.app.async_session_maker
