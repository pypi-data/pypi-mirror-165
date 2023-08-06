from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserCreate")


@attr.s(auto_attribs=True, repr=False)
class UserCreate:
    """  """

    _email: str
    _handle: str
    _name: str

    def __repr__(self):
        fields = []
        fields.append("email={}".format(repr(self._email)))
        fields.append("handle={}".format(repr(self._handle)))
        fields.append("name={}".format(repr(self._name)))
        return "UserCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        email = self._email
        handle = self._handle
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "email": email,
                "handle": handle,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def get_email() -> str:
            email = d.pop("email")
            return email

        email = get_email() if "email" in d else cast(str, UNSET)

        def get_handle() -> str:
            handle = d.pop("handle")
            return handle

        handle = get_handle() if "handle" in d else cast(str, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        name = get_name() if "name" in d else cast(str, UNSET)

        user_create = cls(
            email=email,
            handle=handle,
            name=name,
        )

        return user_create

    @property
    def email(self) -> str:
        """ Email of the User """
        if isinstance(self._email, Unset):
            raise NotPresentError(self, "email")
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    @property
    def handle(self) -> str:
        """ Handle of the User """
        if isinstance(self._handle, Unset):
            raise NotPresentError(self, "handle")
        return self._handle

    @handle.setter
    def handle(self, value: str) -> None:
        self._handle = value

    @property
    def name(self) -> str:
        """ Name of the User """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
