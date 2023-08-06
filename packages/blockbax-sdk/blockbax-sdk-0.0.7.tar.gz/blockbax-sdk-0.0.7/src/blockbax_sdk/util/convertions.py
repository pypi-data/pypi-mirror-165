from typing import List, Optional, Tuple, cast, Union
from numbers import Number
import decimal

from dateutil import parser as date_parser
import pytz
import datetime

from blockbax_sdk import types

import logging

logger = logging.getLogger(__name__)

# number convertions


def normalize_and_remove_exponent(d: decimal.Decimal) -> decimal.Decimal:
    return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()


def convert_number_to_decimal(v: types.AnyNumber) -> decimal.Decimal:
    try:
        # decimal says you can pass an int but mypy disagrees, thats why we ignore the type here
        # https://docs.python.org/3/library/decimal.html#:~:text=Q.%20Some%20decimal,3%27))%0ADecimal(%275000%27)
        return normalize_and_remove_exponent(decimal.Decimal(v).quantize(decimal.Decimal(10) ** -8))  # type: ignore
    except decimal.InvalidOperation as e:
        numeric_convertion_error = f"Could not convert: {v}, make sure that numbers do not have more than 20 digits before and 8 digits after the decimal point"
        raise ValueError(numeric_convertion_error)


# date convertions


def convert_string_to_datetime(date: str):
    return date_parser.parse(date).replace(tzinfo=pytz.utc)


def convert_unix_to_datetime(date: Number) -> datetime.datetime:
    try:
        return datetime.datetime.fromtimestamp(cast(float, date))
    except ValueError:
        return datetime.datetime.fromtimestamp(
            cast(float, date) / 1000
        )  # in case of timestamp with milliseconds


def convert_any_date_to_datetime(date: types.AnyDate) -> datetime.datetime:
    if isinstance(date, str):
        return convert_string_to_datetime(date)
    elif isinstance(date, Number):
        return convert_unix_to_datetime(date)
    elif isinstance(date, datetime.datetime):
        return date
    else:
        cannot_convert_error = f"Cannot convert date: {date}"
        raise ValueError(cannot_convert_error)


def convert_any_date_to_unix_millis(date: types.AnyDate) -> int:
    return int(convert_any_date_to_datetime(date).timestamp() * 1000)


def convert_datetime_to_iso8601(date: datetime.datetime):
    return date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+00:00"


def convert_any_date_to_iso8601(date: types.AnyDate):
    if isinstance(date, datetime.datetime):
        return convert_datetime_to_iso8601(date)
    elif isinstance(date, str):
        return convert_datetime_to_iso8601(convert_string_to_datetime(date))
    elif isinstance(date, Number):
        return convert_datetime_to_iso8601(convert_unix_to_datetime(date))
    else:
        cannot_convert_error = f"Cannot convert date: {date}"
        raise ValueError(cannot_convert_error)


# Other convertions


def convert_name_to_external_id(name: str):
    lower_case_name = name.lower()
    external_id = lower_case_name.replace(" ", "-").strip()
    return external_id


def convert_property_value_ids_to_query_filter(
    property_value_ids: Union[Tuple[str], List[str], str, None]
) -> Optional[str]:
    if isinstance(property_value_ids, (tuple, list)):
        seperator = "," if isinstance(property_value_ids, tuple) else ";"
        return seperator.join(
            [
                id_
                if isinstance(id_, str)
                else cast(str, convert_property_value_ids_to_query_filter(id_))
                for id_ in property_value_ids
            ]
        )
    elif isinstance(property_value_ids, str):
        return property_value_ids
    return None
