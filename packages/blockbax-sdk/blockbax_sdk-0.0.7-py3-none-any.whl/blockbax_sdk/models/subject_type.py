import copy
from typing import List, Optional

from blockbax_sdk.util import convertions

import datetime
import dataclasses

import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class SubjectType:
    name: str
    id: str
    created_date: datetime.datetime
    updated_date: Optional[datetime.datetime] = dataclasses.field(default=None)
    parent_id: Optional[str] = dataclasses.field(default=None)
    primary_location: Optional[dict] = dataclasses.field(default_factory=dict)
    property_types: Optional[List[dict]] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if self.created_date:
            self.created_date = convertions.convert_any_date_to_datetime(
                self.created_date
            )
        if self.updated_date:
            self.updated_date = convertions.convert_any_date_to_datetime(
                self.updated_date
            )

    @classmethod
    def from_api_response(cls, api_response: dict):
        # because this is a list of dictionary's who are both mutable we want to deepcopy this list to prevent any unexpected behavior
        property_types = copy.deepcopy(api_response.get("propertyTypes"))
        # mutable object only needs shallow copy
        primary_location = copy.copy(api_response.get("primaryLocation"))
        return cls(
            name=api_response.get("name"),
            id=api_response.get("id"),
            created_date=api_response.get("createdDate"),
            updated_date=api_response.get("updatedDate"),
            parent_id=api_response.get("parentSubjectTypeId"),
            primary_location=primary_location or {},
            property_types=property_types or [],
        )

    def contains_property_type(self, property_type_id: str) -> bool:
        return any(
            property_type_id == property_type["id"]
            for property_type in self.property_types
        )

    def add_property_types(self, property_types: List[dict]) -> None:
        """Adds new property types to its property_types attribute."""
        self.property_types.extend(property_types)

    def remove_property_types(self, property_type_ids: List[str]) -> None:
        """Removes property types from its property_types attribute by Id."""
        for property_type in enumerate(self.property_types):
            if property_type.get("id") in property_type_ids:
                self.values.remove(property_type)
