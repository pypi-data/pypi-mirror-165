from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_config_field_type import AppConfigFieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTaskSchemaDependencyOutputFieldDefinitionsItem")


@attr.s(auto_attribs=True, repr=False)
class WorkflowTaskSchemaDependencyOutputFieldDefinitionsItem:
    """  """

    _name: str
    _is_multi: Union[Unset, None, bool] = UNSET
    _is_required: Union[Unset, None, bool] = UNSET
    _type: Union[Unset, AppConfigFieldType] = UNSET
    _description: Union[Unset, None, str] = UNSET
    _required_config: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("name={}".format(repr(self._name)))
        fields.append("is_multi={}".format(repr(self._is_multi)))
        fields.append("is_required={}".format(repr(self._is_required)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("required_config={}".format(repr(self._required_config)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WorkflowTaskSchemaDependencyOutputFieldDefinitionsItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        name = self._name
        is_multi = self._is_multi
        is_required = self._is_required
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        description = self._description
        required_config = self._required_config

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if is_multi is not UNSET:
            field_dict["isMulti"] = is_multi
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if required_config is not UNSET:
            field_dict["requiredConfig"] = required_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def get_name() -> str:
            name = d.pop("name")
            return name

        name = get_name() if "name" in d else cast(str, UNSET)

        def get_is_multi() -> Union[Unset, None, bool]:
            is_multi = d.pop("isMulti")
            return is_multi

        is_multi = get_is_multi() if "isMulti" in d else cast(Union[Unset, None, bool], UNSET)

        def get_is_required() -> Union[Unset, None, bool]:
            is_required = d.pop("isRequired")
            return is_required

        is_required = get_is_required() if "isRequired" in d else cast(Union[Unset, None, bool], UNSET)

        def get_type() -> Union[Unset, AppConfigFieldType]:
            type = None
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = AppConfigFieldType(_type)
                except ValueError:
                    type = AppConfigFieldType.of_unknown(_type)

            return type

        type = get_type() if "type" in d else cast(Union[Unset, AppConfigFieldType], UNSET)

        def get_description() -> Union[Unset, None, str]:
            description = d.pop("description")
            return description

        description = get_description() if "description" in d else cast(Union[Unset, None, str], UNSET)

        def get_required_config() -> Union[Unset, bool]:
            required_config = d.pop("requiredConfig")
            return required_config

        required_config = get_required_config() if "requiredConfig" in d else cast(Union[Unset, bool], UNSET)

        workflow_task_schema_dependency_output_field_definitions_item = cls(
            name=name,
            is_multi=is_multi,
            is_required=is_required,
            type=type,
            description=description,
            required_config=required_config,
        )

        workflow_task_schema_dependency_output_field_definitions_item.additional_properties = d
        return workflow_task_schema_dependency_output_field_definitions_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def is_multi(self) -> Optional[bool]:
        """ Schema field's isMulti property, or null for either. """
        if isinstance(self._is_multi, Unset):
            raise NotPresentError(self, "is_multi")
        return self._is_multi

    @is_multi.setter
    def is_multi(self, value: Optional[bool]) -> None:
        self._is_multi = value

    @is_multi.deleter
    def is_multi(self) -> None:
        self._is_multi = UNSET

    @property
    def is_required(self) -> Optional[bool]:
        """ Schema field's isRequired property, or null for either. """
        if isinstance(self._is_required, Unset):
            raise NotPresentError(self, "is_required")
        return self._is_required

    @is_required.setter
    def is_required(self, value: Optional[bool]) -> None:
        self._is_required = value

    @is_required.deleter
    def is_required(self) -> None:
        self._is_required = UNSET

    @property
    def type(self) -> AppConfigFieldType:
        """ Schema field's type, or null for Any. """
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AppConfigFieldType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def description(self) -> Optional[str]:
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def required_config(self) -> bool:
        if isinstance(self._required_config, Unset):
            raise NotPresentError(self, "required_config")
        return self._required_config

    @required_config.setter
    def required_config(self, value: bool) -> None:
        self._required_config = value

    @required_config.deleter
    def required_config(self) -> None:
        self._required_config = UNSET
