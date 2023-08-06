from typing import List, Optional, Any

from blockbax_sdk.util import convertions
from blockbax_sdk import errors, types

from . import property_value

import datetime
import dataclasses

import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class PropertyType:
    name: str
    external_id: str
    id: str
    created_date: datetime.datetime
    data_type: str
    predefined_values: bool
    updated_date: Optional[datetime.datetime] = dataclasses.field(default=None)
    values: List[property_value.PropertyValue] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if self.created_date:
            self.created_date = convertions.convert_any_date_to_datetime(
                self.created_date
            )
        if self.updated_date:
            self.updated_date = convertions.convert_any_date_to_datetime(
                self.updated_date
            )

        if self.predefined_values:
            self.values = [
                property_value.from_dict(
                    {types.PropertyDataTypes(self.data_type).value: value}
                )
                if not isinstance(value, property_value.PropertyValue)
                else value
                for value in self.values
            ]
        else:
            self.values = []

    @classmethod
    def from_api_response(cls, api_response: dict):
        values = []
        for property_value_response in api_response.get("values"):
            new_property_value = property_value.from_dict(
                property_value_response, skip_unexpected=True
            )
            if new_property_value is not None:
                values.append(new_property_value)

        return cls(
            name=api_response.get("name"),
            external_id=api_response.get("externalId"),
            id=api_response.get("id"),
            created_date=api_response.get("createdDate"),
            updated_date=api_response.get("updatedDate"),
            data_type=api_response.get("dataType"),
            predefined_values=api_response.get("predefinedValues"),
            values=values,
        )

    def contains_value(self, value: Any) -> bool:
        """ "Returns `True` if Property type has a Property value with given value"""
        return any(property_value == value for property_value in self.values)

    def add_value(self, value: Any, caption: Optional[str] = None) -> None:
        if self.predefined_values:
            new_property_value = property_value.from_dict(
                {
                    types.PropertyDataTypes(self.data_type).value: value,
                    "caption": caption,
                }
            )
            if new_property_value is not None:
                self.values.append(new_property_value)
        else:
            predefined_values_not_permitted_error = "You cannot add values to a property type with predefined values set to False"
            raise ValueError(predefined_values_not_permitted_error)

    def change_value(self, old_value: Any, new_value: Any) -> None:
        """Changes the value of an already existing property value"""
        if self.predefined_values:
            for property_value in self.values:
                if property_value._has_value(old_value):
                    property_value._set_value(new_value=new_value)
        else:
            predefined_values_not_permitted_error = "You cannot change values of a property type with predefined values set to False"
            raise ValueError(predefined_values_not_permitted_error)

    def change_caption(self, value: Any, caption: str):
        if self.predefined_values:
            for property_value in self.values:
                if property_value._has_value(value):
                    property_value.caption = caption
        else:
            predefined_values_not_permitted_error = "You cannot change captions of a property type with predefined values set to False"
            raise ValueError(predefined_values_not_permitted_error)

    def remove_value(self, value: Any) -> None:
        if self.predefined_values:
            for property_value in self.values:
                if property_value._has_value(value):
                    self.values.remove(property_value)
                    break
        else:
            predefined_values_not_permitted_error = "You cannot remove values from a property type with predefined values set to False"
            raise ValueError(predefined_values_not_permitted_error)
