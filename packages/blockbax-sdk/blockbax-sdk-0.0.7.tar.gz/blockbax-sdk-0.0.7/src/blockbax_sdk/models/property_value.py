from typing import Any, Optional, Union, Optional, Dict
from numbers import Number
import decimal

import abc
import dataclasses

from blockbax_sdk.util import validation
from blockbax_sdk import types
from blockbax_sdk import errors

import logging

logger = logging.getLogger(__name__)


class PropertyValueABC(abc.ABC):
    @abc.abstractmethod
    def get_value(self) -> Optional[Union[str, dict, decimal.Decimal]]:
        return None

    @classmethod
    @abc.abstractmethod
    def get_data_type(cls) -> str:
        pass

    @abc.abstractmethod
    def _has_value(self, value: Any) -> bool:
        pass

    @abc.abstractmethod
    def _set_value(self, new_value: Any):
        pass


@dataclasses.dataclass(eq=False)
class PropertyValue(PropertyValueABC):
    id: Optional[str] = dataclasses.field(default=None)
    caption: Optional[str] = dataclasses.field(default=None)
    inherit: Optional[bool] = dataclasses.field(default=None)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PropertyValue):
            return other.get_value() == self.get_value() and (
                other.id == self.id if self.id and other.id else True
            )
        else:
            return self._has_value(other)

    def get_value(self) -> Optional[Union[str, dict, decimal.Decimal]]:
        return None

    @classmethod
    def get_data_type(cls) -> str:
        return None

    def _has_value(self, value: Any) -> bool:
        return False

    def _set_value(self, new_value: Any):
        pass


@dataclasses.dataclass(eq=False)
class NumberPropertyValue(PropertyValue):
    number: decimal.Decimal = dataclasses.field(default=None)

    def get_value(self) -> Optional[decimal.Decimal]:
        return self.number

    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.NUMBER.value

    def _has_value(self, value: Any) -> bool:
        if isinstance(value, (int, float, decimal.Decimal)):
            return self.number == validation.check_number_and_convert_to_decimal(value)
        return self.number == value

    def _set_value(self, new_value: Any):
        self.number = new_value


@dataclasses.dataclass(eq=False)
class TextPropertyValue(PropertyValue):
    text: str = dataclasses.field(default=None)

    def get_value(self) -> Optional[str]:
        return self.text

    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.TEXT.value

    def _has_value(self, value: str) -> bool:
        return self.text == value

    def _set_value(self, new_value: str):
        self.text = new_value


@dataclasses.dataclass(eq=False)
class LocationPropertyValue(PropertyValue):
    location: dict = dataclasses.field(default=None)

    def get_value(self) -> Optional[dict]:
        return self.location

    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.LOCATION.value

    def _has_value(self, value: dict) -> bool:
        if isinstance(value, dict):
            return self.location == validation.check_location_and_convert(value)
        return self.location == value

    def _set_value(self, new_value: dict):
        self.location = new_value


@dataclasses.dataclass(eq=False)
class MapLayerPropertyValue(PropertyValue):
    map_layer: dict = dataclasses.field(default=None)

    def get_value(self) -> Optional[dict]:
        return self.map_layer

    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.MAP_LAYER.value

    def _has_value(self, value: dict) -> bool:
        if isinstance(value, dict):
            return self.map_layer == validation.check_map_layer_and_convert(
                self.map_layer
            )
        return self.map_layer == value

    def _set_value(self, new_value: dict):
        self.map_layer = new_value


@dataclasses.dataclass(eq=False)
class ImagePropertyValue(PropertyValue):
    image: dict = dataclasses.field(default=None)

    def get_value(self) -> Optional[dict]:
        return self.image

    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.IMAGE.value

    def _has_value(self, value: str) -> bool:
        return self.image == value

    def _set_value(self, new_value: dict):
        self.image = new_value


@dataclasses.dataclass(eq=False)
class AreaPropertyValue(PropertyValue):
    area: dict = dataclasses.field(default=None)

    def get_value(self) -> Optional[dict]:
        return self.area

    @classmethod
    def get_data_type(cls) -> str:
        return types.PropertyDataTypes.AREA.value

    def _has_value(self, value: str) -> bool:
        return self.area == value

    def _set_value(self, new_value: dict):
        self.area = new_value


def new(
    id: Optional[str] = None,
    caption: Optional[str] = None,
    inherit: Optional[bool] = None,
    number: Optional[Union[decimal.Decimal, Number]] = None,
    location: Optional[Dict[str, Union[decimal.Decimal, Number, str]]] = None,
    text: Optional[str] = None,
    map_layer: Optional[dict] = None,
    image: Optional[dict] = None,
    area: Optional[dict] = None,
    **kwargs,
) -> Optional[PropertyValue]:
    values: dict = {
        "number": number,
        "location": location,
        "text": text,
        "map_layer": map_layer,
        "image": image,
        "area": area,
    }

    if not validation.list_contains_single_value(values.values()) and not inherit:
        to_many_arguments_error = (
            f"PropertyValue takes exactly a single data type, values given: {values}"
        )
        raise errors.ValidationError(to_many_arguments_error)

    if number is not None:
        return NumberPropertyValue(
            id, caption, inherit, validation.check_number_and_convert_to_decimal(number)
        )
    elif location is not None:
        return LocationPropertyValue(
            id, caption, inherit, validation.check_location_and_convert(location)
        )
    elif text is not None:
        return TextPropertyValue(id, caption, inherit, validation.check_text(text))
    elif map_layer is not None:
        return MapLayerPropertyValue(
            id, caption, inherit, validation.check_map_layer_and_convert(map_layer)
        )
    elif image is not None:
        return ImagePropertyValue(id, caption, inherit, validation.check_image(image))
    elif area is not None:
        return AreaPropertyValue(
            id, caption, inherit, validation.check_area_and_convert(area)
        )
    else:
        return PropertyValue(id, caption, inherit)


def from_dict(kwargs: dict, skip_unexpected: bool = False) -> Optional[PropertyValue]:
    aliases = {"mapLayer": "map_layer", "valueId": "id"}
    # fixes some aliases
    for alias, wanted in aliases.items():
        if alias in kwargs:
            kwargs[wanted] = kwargs[alias]
            del kwargs[alias]
    try:
        return new(**kwargs)
    except errors.ValidationError as e:
        if not skip_unexpected:
            raise e
