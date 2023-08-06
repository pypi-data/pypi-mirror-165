from typing import List

from blockbax_sdk import errors
from . import measurement

import dataclasses
import datetime

import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Series:
    subject_id: str
    metric_id: str
    measurements: List[measurement.Measurement]

    def __iter__(self):
        return iter(self.measurements)

    @classmethod
    def from_api_response(cls, api_response):
        # Because we are constructing a new list there is no need to copy
        measurements = []
        for measurement_response in api_response.get("measurements"):
            try:
                measurements.append(measurement.from_dict(measurement_response))
            except errors.ValidationError:
                pass

        return cls(
            subject_id=api_response.get("subjectId"),
            metric_id=api_response.get("metricId"),
            measurements=measurements,
        )

    @property
    def latest_date(self) -> datetime:
        latest_date = 0
        for measurement in self.measurements:
            latest_date = (
                measurement.date if measurement.date > latest_date else latest_date
            )
        return latest_date
