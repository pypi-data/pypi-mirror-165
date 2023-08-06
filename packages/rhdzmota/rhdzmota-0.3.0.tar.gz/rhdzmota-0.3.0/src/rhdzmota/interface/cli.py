import json
import datetime as dt
from typing import Optional

from ..settings import get_environ_variable


class CLI:

    class Formatter:

        def __init__(self, cls: Optional = None, default: Optional = None):  # type: ignore
            self.serializer = lambda obj: json.dumps(obj, cls=cls, default=default, indent=4)

        def __call__(self, method):
            def wrapper(other, *args, **kwargs):
                start = getattr(other, "start")
                output = method(other, *args, **kwargs)
                if not isinstance(output, str):
                    output = self.serializer(output)
                end = dt.datetime.utcnow()
                print(f"\n{10*'-'} Command Output:", output, f"\n{10*'-'} Metadata:", sep="\n")
                return {
                    "> timestamp_start": start,
                    "> timestamp_end": end,
                    "> duration_seconds": (end - start).seconds,
                }
            return wrapper

    def __init__(self):
        self.start = dt.datetime.utcnow()

    @Formatter()
    def environ(self, name: str) -> Optional[str]:
        return get_environ_variable(
            name=name,
            enforce=False,
        )
