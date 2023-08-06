import functools
import importlib
from typing import Optional

def load_class(path:str) -> Optional[object]:
    """
    Loads a class by string path
    :param path: string path
    :return: either a class or None if resource is not found
    """
    try:
        module_path, cls_name = path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        cls = getattr(module, cls_name, None)
        if cls is None:
            return None
        return cls
    except ModuleNotFoundError as e:
        return None
