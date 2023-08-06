from typing import Union, Optional, Dict
from numbers import Number
import decimal

from blockbax_sdk.util import validation
from blockbax_sdk import types
from blockbax_sdk import errors

import datetime
import abc
import dataclasses

import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Measurement(abc.ABC):
    date: int = dataclasses.field(default=None)

    @abc.abstractmethod
    def get_value(self) -> Optional[Union[str, dict, decimal.Decimal]]:
        pass

    @classmethod
    @abc.abstractmethod
    def get_data_type(cls) -> str:
        pass


@dataclasses.dataclass
class NumberMeasurement(Measurement):
    number: decimal.Decimal = dataclasses.field(default_factory=decimal.Decimal)

    def get_value(self) -> decimal.Decimal:
        return self.number

    @classmethod
    def get_data_type(cls) -> str:
        return types.MeasurementDataTypes.NUMBER.value


@dataclasses.dataclass
class LocationMeasurement(Measurement):
    location: dict = dataclasses.field(default_factory=dict)

    def get_value(self) -> dict:
        return self.location

    @classmethod
    def get_data_type(cls) -> str:
        return types.MeasurementDataTypes.LOCATION.value


@dataclasses.dataclass
class TextMeasurement(Measurement):
    text: str = dataclasses.field(default_factory=str)

    def get_value(self) -> str:
        return self.text

    @classmethod
    def get_data_type(cls) -> str:
        return types.MeasurementDataTypes.TEXT.value


def new(
    date: Union[datetime.datetime, int, str] = None,
    number: Optional[Union[decimal.Decimal, Number]] = None,
    location: Optional[Dict[str, Union[decimal.Decimal, Number, str]]] = None,
    text: Optional[str] = None,
    **kwargs,
) -> Optional[Measurement]:
    required_attributes: dict = {"date": date}
    values: dict = {"number": number, "location": location, "text": text}

    if any(attr is None for attr in required_attributes.values()):
        missing_required_error = f"Measurement needs to have the following required attributes set: {required_attributes.keys()}"
        raise errors.ValidationError(missing_required_error)

    if not validation.list_contains_single_value(values.values()):
        to_many_arguments_error = (
            f"Measurement takes exactly a single data type, values given: {values}"
        )
        raise errors.ValidationError(to_many_arguments_error)

    if number is not None:
        return NumberMeasurement(
            validation.check_date_and_convert_to_unix(date),
            validation.check_number_and_convert_to_decimal(number),
        )
    elif location is not None:
        return LocationMeasurement(
            validation.check_date_and_convert_to_unix(date),
            validation.check_location_and_convert(location),
        )
    elif text is not None:
        return TextMeasurement(
            validation.check_date_and_convert_to_unix(date), validation.check_text(text)
        )
    else:
        return None


def from_dict(kwargs: dict) -> Optional[Measurement]:
    return new(**kwargs)
