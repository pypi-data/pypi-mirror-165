from typing import Optional, List, Dict

from . import property_value
from blockbax_sdk.util import convertions
from blockbax_sdk import errors

import datetime
import dataclasses
import copy

import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Subject:
    name: str
    id: str
    subject_type_id: str
    external_id: str
    created_date: datetime.datetime
    updated_date: datetime.datetime = dataclasses.field(default=None)
    parent_id: Optional[str] = dataclasses.field(default=None)
    ingestion_ids: List[dict] = dataclasses.field(default_factory=list)
    properties: Dict[str, property_value.PropertyValue] = dataclasses.field(
        default_factory=dict
    )

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
        ingestion_ids = copy.deepcopy(api_response.get("ingestionIds"))

        # Because we are constructing a new dict there is no need to copy
        properties = {}
        for property_response in api_response.get("properties") or []:
            property_copy = copy.deepcopy(property_response)
            del property_copy["typeId"]

            new_property_value = property_value.from_dict(
                property_copy, skip_unexpected=True
            )
            if new_property_value is not None:
                properties[property_response["typeId"]] = new_property_value

        return cls(
            subject_type_id=api_response.get("subjectTypeId"),
            parent_id=api_response.get("parentSubjectId"),
            name=api_response.get("name"),
            id=api_response.get("id"),
            external_id=api_response.get("externalId"),
            created_date=api_response.get("createdDate"),
            updated_date=api_response.get("updatedDate"),
            ingestion_ids=ingestion_ids or [],
            properties=properties,
        )

    def set_properties(self, properties: List[dict]) -> None:
        """Store a property values in properties attribute."""
        for property_ in properties:
            property_copy = copy.deepcopy(property_)
            del property_copy["typeId"]
            new_property_value = property_value.from_dict(property_copy)
            if new_property_value is not None:
                self.properties[property_["typeId"]] = new_property_value

    def remove_properties(self, property_type_ids: List[str]) -> None:
        """Remove a property value from properties attribute."""
        for property_type_id in property_type_ids:
            del self.properties[property_type_id]

    def override_ingestion_id(self, metric_id: str, ingestion_id: str) -> None:
        """Stored an ingestion ID to override in ingestion_ids attribute per metric ID and sets deriveIngestionId to False."""
        for ingestion in self.ingestion_ids:
            if metric_id == ingestion.get("metricId"):
                ingestion["ingestionId"] = ingestion_id
                ingestion["deriveIngestionId"] = False

    def derive_ingestion_id(self, metric_id: str):
        """Remove an ingestion ID to override in ingestion_ids attribute per metric ID and sets deriveIngestionId to True."""
        for ingestion in self.ingestion_ids:
            if metric_id == ingestion.get("metricId"):
                if "ingestionId" in ingestion:
                    del ingestion["ingestionId"]
                ingestion["deriveIngestionId"] = True

    def get_ingestion_id(self, metric_id: str) -> Optional[str]:
        for ingestion in self.ingestion_ids:
            if metric_id == ingestion["metricId"]:
                return ingestion["ingestionId"]
        return None

    def has_ingestion_id(self, ingestion_id: str = "") -> bool:
        for ingestion in self.ingestionIds:
            if ingestion_id == ingestion["ingestionId"]:
                return True
        return False

    def has_metric_id(self, metric_id: str = ""):
        for ingestion in self.ingestionIds:
            if metric_id == ingestion["metricId"]:
                return True
        return False

    def get_metric_id(self, ingestion_id: str = "") -> Optional[str]:
        for ingestion in self.ingestion_ids:
            if ingestion_id == ingestion["ingestionId"]:
                return ingestion["metricId"]
        return None

    def has_ingestion_ids(self, ingestion_ids: List[str]) -> bool:
        return all(
            ingestion_id
            in [
                known_ingestion["ingestionId"] for known_ingestion in self.ingestion_ids
            ]
            for ingestion_id in ingestion_ids
        )

    def has_ingestion_id(self, ingestion_id: str) -> bool:
        return any(
            ingestion_id == ingestion["ingestionId"] for ingestion in self.ingestion_ids
        )

    def has_metric_id(self, metric_id: str = "") -> bool:
        return any(
            metric_id == ingestion["metricId"] for ingestion in self.ingestion_ids
        )
