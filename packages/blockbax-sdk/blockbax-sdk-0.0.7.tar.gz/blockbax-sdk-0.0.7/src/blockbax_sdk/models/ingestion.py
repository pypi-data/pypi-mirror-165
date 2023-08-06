from typing import List

from . import measurement

import dataclasses

import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Ingestion:
    id: str
    measurements: List[measurement.Measurement] = dataclasses.field(
        default_factory=list
    )

    def __post_init__(self):
        if not self.id:
            no_ids_given_error = f"Please provide a ingestion ID"
            raise ValueError(no_ids_given_error)

    def add_measurement(self, new_measurement: measurement.Measurement) -> None:
        if (
            len(self.measurements) > 0
            and new_measurement.get_data_type() != self.measurements[-1].get_data_type()
        ):
            inconsistent_use_of_data_type_error = f"Inconsistent use of data types, data type: {new_measurement.get_data_type()} does not equal data type of previous measurement added to this ingestion: {self.measurements[-1].get_data_type()}"
            raise ValueError(inconsistent_use_of_data_type_error)

        self.measurements.append(new_measurement)

    def clear(self):
        self.measurements.clear()

    def get_measurement_count(self):
        return len(self.measurements)
