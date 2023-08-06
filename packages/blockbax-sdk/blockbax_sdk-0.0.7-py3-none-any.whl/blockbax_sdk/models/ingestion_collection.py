from typing import Dict, List, Optional

from . import ingestions_utils
from . import ingestion
from . import subject

import logging

logger = logging.getLogger(__name__)


class IngestionCollection:
    __ingestions: Dict[str, ingestion.Ingestion]

    def __init__(self):
        self.__ingestions = {}

    def __getitem__(self, ingestion_id: str) -> ingestion.Ingestion:
        return self.__ingestions.get(ingestion_id)

    def __setitem__(self, ingestion_id: str, ingestion: ingestion.Ingestion):
        self.__ingestions[ingestion_id] = ingestion

    def get_all_ids(self) -> List[str]:
        return list(self.__ingestions.keys())

    def create_series_to_send(
        self,
        subjects: List[subject.Subject],
        auto_create_subjects: bool,
        ingestion_ids: Optional[List[str]] = [],
    ) -> List:
        if ingestion_ids:
            ingestions_to_send = (
                self.__ingestions[ingestion_id]
                for ingestion_id in ingestion_ids
                if ingestion_id in self.__ingestions
            )
        else:
            ingestions_to_send = (
                ingestion for _, ingestion in self.__ingestions.items()
            )

        return ingestions_utils.create_series_batches(
            ingestions=ingestions_to_send,
            subjects=subjects,
            auto_create_subjects=auto_create_subjects,
        )

    def clear_all(self):
        for _, ingestion in self.__ingestions.items():
            ingestion.clear()
