from bc_time.api.objects.object_base_write import ObjectBaseWrite
from bc_time.api.objects.object_base_read import ObjectBaseRead
from bc_time.api.objects.group_base import GroupBase
from bc_time.api.api import Api
from bc_time.api.enumerators.content_type import ContentType

class VisitorGroups(ObjectBaseWrite, ObjectBaseRead, GroupBase):
    def __init__(self, api: Api=None) -> None:
        super().__init__(api)
        self._content_type_id = ContentType.visitor_group
        self._membership_content_type_id = ContentType.visitor_group_membership