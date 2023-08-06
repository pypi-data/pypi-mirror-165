import dataclasses
import decimal
import json
import datetime
import uuid


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    Extended JSON encoder
    Supports UUID, Decimal, HTML, Dataclasses and DateTime objects
    """
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if isinstance(obj, (decimal.Decimal, uuid.UUID)):
            return str(obj)
        if dataclasses and dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        if hasattr(obj, "__html__"):
            return str(obj.__html__())
        if hasattr(obj, 'asdict') and callable(getattr(obj, 'asdict', None)):
            return obj.asdict()
        return obj.__dict__
