from bc_time.api.objects.base import Base
from bc_time.api.constants.api import Api as ApiConstants

class ObjectBaseRead(Base):
    def get_all_using_pagination(self, filters: dict=None, page: int=1, row_count: int=ApiConstants.DEFAULT_ROW_COUNT) -> dict:
        return self.api.get_all_using_pagination(
            content_type_id=self._content_type_id,
            filters=filters,
            page=page,
            row_count=row_count
        )

    def get_one(self, content_uid: int) -> dict:
        return self.api.get_one(
            content_type_id=self._content_type_id,
            content_uid=content_uid
        )

    def get_many(self, content_uids: list) -> dict:
        return self.api.get_many(
            content_type_id=self._content_type_id,
            content_uids=content_uids
        )