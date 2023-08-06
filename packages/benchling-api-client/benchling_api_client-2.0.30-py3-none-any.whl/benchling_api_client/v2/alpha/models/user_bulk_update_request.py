from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.user_bulk_update import UserBulkUpdate
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserBulkUpdateRequest")


@attr.s(auto_attribs=True, repr=False)
class UserBulkUpdateRequest:
    """  """

    _users: Union[Unset, List[UserBulkUpdate]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("users={}".format(repr(self._users)))
        return "UserBulkUpdateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        users: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._users, Unset):
            users = []
            for users_item_data in self._users:
                users_item = users_item_data.to_dict()

                users.append(users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def get_users() -> Union[Unset, List[UserBulkUpdate]]:
            users = []
            _users = d.pop("users")
            for users_item_data in _users or []:
                users_item = UserBulkUpdate.from_dict(users_item_data)

                users.append(users_item)

            return users

        users = get_users() if "users" in d else cast(Union[Unset, List[UserBulkUpdate]], UNSET)

        user_bulk_update_request = cls(
            users=users,
        )

        return user_bulk_update_request

    @property
    def users(self) -> List[UserBulkUpdate]:
        if isinstance(self._users, Unset):
            raise NotPresentError(self, "users")
        return self._users

    @users.setter
    def users(self, value: List[UserBulkUpdate]) -> None:
        self._users = value

    @users.deleter
    def users(self) -> None:
        self._users = UNSET
