from blockbax_sdk.util import convertions

import datetime
import dataclasses

import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Metric:
    subject_type_id: str
    name: str
    id: str
    external_id: str
    data_type: str
    type: str
    mapping_level: str = dataclasses.field(default=None)
    created_date: datetime.datetime = dataclasses.field(default=None)
    updated_date: datetime.datetime = dataclasses.field(default=None)
    discrete: bool = dataclasses.field(default=False)
    unit: str = dataclasses.field(default_factory=str)
    precision: str = dataclasses.field(default_factory=str)
    visible: bool = dataclasses.field(default_factory=bool)

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
        visible = api_response.get("visible")
        return cls(
            subject_type_id=api_response.get("subjectTypeId"),
            name=api_response.get("name"),
            id=api_response.get("id"),
            external_id=api_response.get("externalId"),
            type=api_response.get("type"),
            mapping_level=api_response.get("mappingLevel"),
            created_date=api_response.get("createdDate"),
            updated_date=api_response.get("updatedDate"),
            discrete=api_response.get("discrete"),
            data_type=api_response.get("dataType"),
            precision=api_response.get("precision") or "",
            unit=api_response.get("unit") or "",
            visible=visible if visible is not None else True,  # default if not present
        )
