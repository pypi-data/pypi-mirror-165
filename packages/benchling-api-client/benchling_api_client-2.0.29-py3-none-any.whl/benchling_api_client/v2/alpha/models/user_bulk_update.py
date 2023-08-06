from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserBulkUpdate")


@attr.s(auto_attribs=True, repr=False)
class UserBulkUpdate:
    """  """

    _id: str
    _email: Union[Unset, str] = UNSET
    _handle: Union[Unset, str] = UNSET
    _is_suspended: Union[Unset, bool] = UNSET
    _name: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("email={}".format(repr(self._email)))
        fields.append("handle={}".format(repr(self._handle)))
        fields.append("is_suspended={}".format(repr(self._is_suspended)))
        fields.append("name={}".format(repr(self._name)))
        return "UserBulkUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        email = self._email
        handle = self._handle
        is_suspended = self._is_suspended
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if handle is not UNSET:
            field_dict["handle"] = handle
        if is_suspended is not UNSET:
            field_dict["isSuspended"] = is_suspended
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def get_id() -> str:
            id = d.pop("id")
            return id

        id = get_id() if "id" in d else cast(str, UNSET)

        def get_email() -> Union[Unset, str]:
            email = d.pop("email")
            return email

        email = get_email() if "email" in d else cast(Union[Unset, str], UNSET)

        def get_handle() -> Union[Unset, str]:
            handle = d.pop("handle")
            return handle

        handle = get_handle() if "handle" in d else cast(Union[Unset, str], UNSET)

        def get_is_suspended() -> Union[Unset, bool]:
            is_suspended = d.pop("isSuspended")
            return is_suspended

        is_suspended = get_is_suspended() if "isSuspended" in d else cast(Union[Unset, bool], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        name = get_name() if "name" in d else cast(Union[Unset, str], UNSET)

        user_bulk_update = cls(
            id=id,
            email=email,
            handle=handle,
            is_suspended=is_suspended,
            name=name,
        )

        return user_bulk_update

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def email(self) -> str:
        """ Email of the User """
        if isinstance(self._email, Unset):
            raise NotPresentError(self, "email")
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    @email.deleter
    def email(self) -> None:
        self._email = UNSET

    @property
    def handle(self) -> str:
        """ Handle of the User """
        if isinstance(self._handle, Unset):
            raise NotPresentError(self, "handle")
        return self._handle

    @handle.setter
    def handle(self, value: str) -> None:
        self._handle = value

    @handle.deleter
    def handle(self) -> None:
        self._handle = UNSET

    @property
    def is_suspended(self) -> bool:
        """ Suspended status of the User """
        if isinstance(self._is_suspended, Unset):
            raise NotPresentError(self, "is_suspended")
        return self._is_suspended

    @is_suspended.setter
    def is_suspended(self, value: bool) -> None:
        self._is_suspended = value

    @is_suspended.deleter
    def is_suspended(self) -> None:
        self._is_suspended = UNSET

    @property
    def name(self) -> str:
        """ Name of the User """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
