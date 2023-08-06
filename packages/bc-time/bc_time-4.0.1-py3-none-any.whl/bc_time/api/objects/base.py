from abc import ABC
from bc_time.api.api import Api

class Base(ABC):
    # Protected
    _content_type_id = None

    # Public
    api = None

    def __init__(self, api: Api=None) -> None:
        self.api = Api() if api is None else api