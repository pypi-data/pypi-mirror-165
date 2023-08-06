from bc_time.api.objects.object_base_write import ObjectBaseWrite
from bc_time.api.objects.object_base_read import ObjectBaseRead
from bc_time.api.api import Api
from bc_time.api.enumerators.content_type import ContentType

class Employees(ObjectBaseWrite, ObjectBaseRead):
    def __init__(self, api: Api=None) -> None:
        super().__init__(api)
        self._content_type_id = ContentType.employee