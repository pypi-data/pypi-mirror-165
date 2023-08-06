from typing import Dict, Iterator, List, Tuple

from . import subject
from . import ingestion
from . import measurement
import collections

import logging

logger = logging.getLogger(__name__)


def split_list(data, length):
    return [data[x : x + length] for x in range(0, len(data), length)]


def create_series_batches(
    ingestions: Iterator[ingestion.Ingestion],
    subjects: List[subject.Subject],
    auto_create_subjects: bool,
) -> List[dict]:
    grouped_ingestions = group_ingestions_per_subject(
        ingestions, subjects, auto_create_subjects
    )
    json_batches = []
    for ingestions_per_subject in grouped_ingestions:
        measurements_to_send = collections.defaultdict(list)

        batches_to_send = batch_measurements_by_date(ingestions_per_subject)

        for batch in batches_to_send:
            # group measurements by ingestion_id
            for measurement in batch:
                measurements_to_send[measurement[0]].append(
                    {
                        "date": measurement[1].date,
                        measurement[1].get_data_type(): measurement[1].get_value(),
                    }
                )

            series = []
            for ingestion_id, measurements in measurements_to_send.items():
                series.append(
                    {"ingestionId": ingestion_id, "measurements": measurements}
                )

            json_batches.append(series)
            measurements_to_send.clear()

    return json_batches


def group_ingestions_per_subject(
    ingestions: Iterator[ingestion.Ingestion],
    subjects: List[subject.Subject],
    auto_create_subjects: bool,
) -> List[List[ingestion.Ingestion]]:
    """Creates a list containing lists of ingestions grouped per subject"""
    # assign each ingestion without subject
    grouped_ingestions_dict: Dict[str, list] = {}
    for ingestion in ingestions:
        for subject in subjects:
            if subject.has_ingestion_id(ingestion.id):
                grouped_ingestions_dict.setdefault(subject.id, []).append(ingestion)
                break
        else:
            # not found in known subjects
            if not auto_create_subjects:
                ingestion_id_does_not_warning = f"Ingestion with ID: {ingestion.id} does not exist in existing subjects and 'auto create subjects' is set to false"
                print(f"Warning: {ingestion_id_does_not_warning}")

            grouped_ingestions_dict.setdefault("default", []).append(ingestion)

    return [*grouped_ingestions_dict.values()]  # unpack and return as list


def batch_measurements_by_date(
    ingestions: List[ingestion.Ingestion],
) -> List[List[Tuple[str, measurement.Measurement]]]:
    number_of_measurements = 0
    list_of_measurements = []

    # TODO not sure if this scales well for a very large amount of measurements
    for ingestion in ingestions:
        number_of_measurements += ingestion.get_measurement_count()
        for measurement in ingestion.measurements:
            # list_of_measurements.append((ingestion.id, measurement.date, measurement.get_value()))
            list_of_measurements.append((ingestion.id, measurement))

        # Sort all measurements by date
    if number_of_measurements > 500:
        # TODO make sure the date is datetime object since it should sort on datetime
        sorted_list_of_measurements = sorted(
            list_of_measurements,
            key=lambda measurement_tuple: measurement_tuple[1].date,
        )

        batched_measurements = split_list(sorted_list_of_measurements, 500)
        return batched_measurements

    else:
        return [list_of_measurements]
