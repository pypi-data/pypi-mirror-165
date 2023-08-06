from bc_time.api.objects.object_base import ObjectBase
from bc_time.api.api import Api
from bc_time.api.enumerators.content_type import ContentType

class Devices(ObjectBase):
    def __init__(self, api: Api=None) -> None:
        super().__init__(api)
        self._content_type_id = ContentType.device