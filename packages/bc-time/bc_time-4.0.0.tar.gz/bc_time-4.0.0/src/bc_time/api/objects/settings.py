from bc_time.api.objects.base import Base
from bc_time.api.api import Api
from bc_time.api.enumerators.content_type import ContentType

class Settings(Base):
    def __init__(self, api: Api=None) -> None:
        super().__init__(api)

    def get_all_settings(self) -> dict:
        return self.api.get_all_using_pagination(content_type_id=ContentType.settings)