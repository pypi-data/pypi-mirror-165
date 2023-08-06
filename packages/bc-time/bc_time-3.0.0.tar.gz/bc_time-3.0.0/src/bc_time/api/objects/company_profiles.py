from bc_time.api.objects.base import Base
from bc_time.api.api import Api
from bc_time.api.enumerators.content_type import ContentType
from bc_time.api.enumerators.status import Status
from bc_time.api.constants.api import Api as ApiConstants

class CompanyProfiles(Base):
    def __init__(self, api: Api=None) -> None:
        super().__init__(api)

    def confirm_user_email(self, email: str, status: int=Status.active) -> dict:
        """Email and username - in this context - are synonymous in BC Time.
        """
        filters = {
            'filter_user_name': email,
            'filter_user_status': status,
        }
        return self.api.get_all_using_pagination(
            content_type_id=ContentType.company_profile_user_membership_email_confirm,
            filters=filters
        )

    def get_all_users_using_pagination(self, filters: dict=None, page: int=1, row_count: int=ApiConstants.DEFAULT_ROW_COUNT) -> dict:
        return self.api.get_all_using_pagination(
            content_type_id=ContentType.company_profile_user_membership,
            filters=filters,
            page=page,
            row_count=row_count
        )

    def get_current_company_profile(self) -> dict:
        return self.api.get_all_using_pagination(content_type_id=ContentType.current_company_profile)