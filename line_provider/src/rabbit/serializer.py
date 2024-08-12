from typing import Any
import json

import pydantic


def serialize_data(data: Any, schema: type[pydantic.BaseModel]) -> bytes:
    data = schema(**data.__dict__).model_dump(mode='json')
    return json.dumps(data).encode()
