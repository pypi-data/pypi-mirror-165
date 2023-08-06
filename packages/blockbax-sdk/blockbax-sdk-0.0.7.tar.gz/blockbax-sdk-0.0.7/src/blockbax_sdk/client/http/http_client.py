from typing import Any, List, Dict, Optional, Tuple, Union
from numbers import Number
import decimal

from blockbax_sdk import models
from blockbax_sdk.util import convertions
from blockbax_sdk import types
from blockbax_sdk import errors
from .api import api

import datetime
import logging

logger = logging.getLogger(__name__)


class HttpClient:
    __api: api.Api
    __ingestions: models.IngestionCollection

    name: Optional[str]
    creation_date: Optional[datetime.datetime]
    updated_date: Optional[datetime.datetime]
    description: Optional[str]
    timezone_id: Optional[str]
    organization_id: Optional[str]
    project_id: Optional[str]

    def __init__(self, access_token: str, project_id: str):
        self.__ingestions = models.IngestionCollection()
        if access_token and project_id:
            self.project_id = project_id
            self.__api = api.Api(access_token=access_token, project_id=project_id)
        else:
            raise ValueError("Please provide both project ID and Access token!")

    def get_user_agent(self) -> str:
        return self.__api.user_agent

    def get_project_details(self) -> dict:
        project_api_response = self.__api.get_project()
        self.name = project_api_response.get("name")
        creation_date = project_api_response.get("createdDate")
        updated_date = project_api_response.get("updatedDate")
        if creation_date is not None:
            self.created_date = convertions.convert_string_to_datetime(creation_date)
        if updated_date is not None:
            self.updated_date = convertions.convert_string_to_datetime(updated_date)
        self.description = project_api_response.get("description")
        self.timezone_id = project_api_response.get("timezoneId")
        self.organization_id = project_api_response.get("organizationId")
        return project_api_response

    # Methods to create, update, delete and get property types.

    def get_property_types(
        self,
        name: Optional[str] = None,
        external_id: Optional[str] = None,
    ) -> List[models.PropertyType]:
        """Gets property types, optionally with arguments for filtering.

        Arguments:
            name [optional, default=None]: The name of the property type to filter on.

        Returns:
            List of `PropertyType`
        """
        property_type_responses = self.__api.get_property_types(
            name=name, external_id=external_id
        )
        property_type_list = []
        for property_type_response in property_type_responses:
            property_type_list.append(
                models.PropertyType.from_api_response(property_type_response)
            )
        return property_type_list

    def get_property_type(self, id_: str) -> Optional[models.PropertyType]:
        """Gets a specific property type.

        Arguments:
            id_ [required]: Property type ID to fetch.

        Returns: `PropertyType`
        """
        property_type_response = self.__api.get_property_type(property_type_id=id_)
        if property_type_response is None:
            return None
        property_type = models.PropertyType.from_api_response(property_type_response)
        return property_type

    def create_property_type(
        self,
        name: str,
        external_id: str,
        data_type: str,
        predefined_values: bool,
        values: Optional[list] = None,
    ) -> models.PropertyType:
        """Creates a property type

        Arguments:
            name [required]:
                The name of the property type.
            data_type [required]:
                The type of the property type. Can be “TEXT”, “NUMBER” or “LOCATION”.
            predefined_values [required]:
                Defines whether it is possible to create values for this property type in the resource itself (for value true) or they are automatically created when adding a value to a subject (for value false).
            values [optional, default=[] ]:
                List of predefined values. A property type can be created with or without predefined values.
        Returns:
            `PropertyType`
        """
        if values is None:
            values = []
        if not predefined_values and values:
            raise ValueError(
                "Values can only be added to a property type with predefined values"
            )

        property_type_response = self.__api.create_property_type(
            name=name,
            external_id=external_id,
            data_type=data_type,
            predefined_values=predefined_values,
            values=values,
        )

        property_type = models.PropertyType.from_api_response(property_type_response)
        return property_type

    def update_property_type(
        self,
        property_type: models.PropertyType,
    ) -> models.PropertyType:
        """Updates a property type.
        Arguments:
            property_type [required]: Updated `PropertyType`
        Returns:
            `PropertyType`
        """

        property_values = []
        if property_type.predefined_values:
            for property_value in property_type.values:
                property_value_object: Dict[str, Any] = {}
                if property_value.id:
                    property_value_object["id"] = property_value.id
                if property_value.caption:
                    property_value_object["caption"] = property_value.caption
                property_value_object[
                    property_value.get_data_type()
                ] = property_value.get_value()
                property_values.append(property_value_object)

        property_type_response = self.__api.update_property_type(
            property_type_id=property_type.id,
            name=property_type.name,
            external_id=property_type.external_id,
            data_type=property_type.data_type,
            predefined_values=property_type.predefined_values,
            values=property_values,
        )
        property_type = models.PropertyType.from_api_response(property_type_response)
        return property_type

    def delete_property_type(self, id_: str) -> None:
        """Deletes a property type.

        Arguments:
            id_ [required]: Property type ID to delete.

        Returns: `None`
        """
        self.__api.delete_property_type(property_type_id=id_)

    # Methods to create, update, delete and get subject types.

    def get_subject_types(
        self, name: Optional[str] = None, property_type_ids: Optional[List[str]] = None
    ) -> List[models.SubjectType]:
        """Gets subject types, optionally with arguments for filtering.

        Arguments:
            name [optional, default=None]:
                Filter subject types by name.
            property_types_ids [optional, default=None]:
                A list of strings that contain property type IDs to filter on.

        Returns:
            List of `SubjectType`
        """

        subject_type_responses = self.__api.get_subject_types(
            name=name, property_type_ids=property_type_ids
        )
        subject_type_list = []
        for subject_type_response in subject_type_responses:
            subject_type_list.append(
                models.SubjectType.from_api_response(subject_type_response)
            )
        return subject_type_list

    def get_subject_type(self, id_: str) -> Optional[models.SubjectType]:
        """Gets a specific subject type.

        Arguments
            id_ [required]: Subject Type ID to fetch.
        Returns: `SubjectType`
        """

        subject_type_response = self.__api.get_subject_type(subject_type_id=id_)
        if subject_type_response is None:
            return None
        subject_type = models.SubjectType.from_api_response(subject_type_response)

        return subject_type

    def create_subject_type(
        self,
        name: str,
        parent_id: Optional[str] = None,
        primary_location: Optional[Dict] = None,
        property_types: Optional[List[dict]] = None,
    ) -> models.SubjectType:
        """Creates a subject type

        Arguments:
            name [required]:
                The name of the subject type.
            parent_id [optional, default=None]:
                The ID of the parent subject type of this subject type.
            primary_location [optional, default=None ]:
                The primary location metric or property type of this subject type, for displaying the location of subjects on the map.
            property_types [optional, default=None ]:
                List of property type dictionary’s associated with this subject type.

        Returns: `SubjectType`
        """
        subject_type_response = self.__api.create_subject_type(
            name=name,
            parent_id=parent_id,
            primary_location=primary_location,
            property_types=property_types,
        )

        subject_type = models.SubjectType.from_api_response(subject_type_response)

        return subject_type

    def update_subject_type(
        self,
        subject_type: models.SubjectType,
    ) -> models.SubjectType:
        """Updates a subject type.

        Arguments:
            subject_type [required]: Updated `SubjectType`

        Returns: `SubjectType`
        """

        subject_type_response = self.__api.update_subject_type(
            subject_type_id=subject_type.id,
            name=subject_type.name,
            parent_id=subject_type.parent_id,
            property_types=subject_type.property_types,
            primary_location=subject_type.primary_location,
        )

        updated_subject_type = models.SubjectType.from_api_response(
            subject_type_response
        )

        return updated_subject_type

    def delete_subject_type(self, id_: str) -> None:
        """Deletes a subject type.

        Arguments:
            id_ [required]: Subject type ID to delete.
        Returns: `None`
        """

        self.__api.delete_subject_type(subject_type_id=id_)

    # Methods to create, update, delete and get metrics.

    def get_metrics(
        self,
        name: Optional[str] = None,
        metric_external_id: Optional[str] = None,
        subject_type_ids: Optional[List[str]] = None,
    ) -> List[models.Metric]:
        """Gets metrics, optionally with arguments for filtering.

        Arguments:
            name [optional, default=None]:
                Filter property types by name.
            external_id [optional, default=None]:
                Filter metrics by external ID.
            subject_type_ids [optional, default=None]:
                Filter on a list of subject type IDs.
        Returns:
            List of `Metric`
        """

        metric_responses = self.__api.get_metrics(
            name=name,
            metric_external_id=metric_external_id,
            subject_type_ids=subject_type_ids,
        )
        metric_list = []
        for metric_response in metric_responses:
            metric_list.append(models.Metric.from_api_response(metric_response))
        return metric_list

    def get_metric(self, id_: str) -> Optional[models.Metric]:
        """Gets a specific metric.

        Arguments:
            id_ [required]: Metric ID to fetch.

        Returns: `Metric`
        """
        metric_response = self.__api.get_metric(metric_id=id_)
        if metric_response is None:
            return None
        return models.Metric.from_api_response(metric_response)

    def create_metric(
        self,
        subject_type_id: str,
        name: str,
        data_type: str,
        type_: str,
        mapping_level: Optional[str] = None,
        discrete: Optional[bool] = False,
        unit: Optional[str] = None,
        precision: Optional[int] = None,
        visible: Optional[bool] = True,
        external_id: Optional[str] = None,
    ) -> models.Metric:
        """Creates a metric.

        Arguments:
            subject_type_id [required]:
                Subject type ID that this metric belongs to. Determines which subjects, property types and metrics are connected.
            name [required]:
                The name of the metric.
            data_type [required]:
                The data type of the metric. Choose from: NUMBER or LOCATION.
            type_ [required]:
                The type of the metric. Currently only the INGESTED type is supported.
            mapping_level [requied]:
                The level on which the ingestion ID mappings are set. Choose from: OWN or CHILD. In most cases the ingestion ID for a metric is configured on the type's own level, meaning at the subjects containing the metric. However, in some cases it might be useful to do this at child level. If ingestion IDs are derived from the external IDs of a subject and a metric, this makes it possible to move a subject to another parent without having to update the ingestion ID.
            discrete [optional, default=False]
                Whether this metric has discrete values. This is used by the web app to optimize visualization.
            unit [optional, default=None]:
                The unit of the metric.
            precision [optional, default=None]:
                The precision to show in the client for the metric, from 0 to 8.
            visible [optional, default=True]:
                Whether this metric is visible in the client.
            external_id [optional, default=None]:
                The external ID of the subject. This can be used when sending measurements to avoid the source systems (e.g. sensors) need to know which IDs are internally used in the Blockbax Platform. If left empty the external ID will be derived from the given name but it is recommended that one is given.

        Returns: `Metric`
        """

        metric_type = types.MetricTypes(type_)

        if metric_type in [types.MetricTypes.SIMULATED, types.MetricTypes.CALCULATED]:
            metric_type_not_implemented_error = (
                f"Creating metric with type: {type_} is not yet implemented!"
            )
            raise NotImplementedError(metric_type_not_implemented_error)

        if external_id is None:
            external_id = convertions.convert_name_to_external_id(name=name)

        metric_api_response = self.__api.create_metric(
            name=name,
            data_type=data_type,
            external_id=external_id,
            type_=metric_type.value,
            mapping_level=mapping_level,
            discrete=discrete,
            subject_type_id=subject_type_id,
            unit=unit,
            precision=precision,
            visible=visible,
        )

        metric = models.Metric.from_api_response(metric_api_response)

        return metric

    def update_metric(
        self,
        metric: models.Metric,
    ) -> models.Metric:
        """Updates a metric.

        Arguments:
            metric [required]: Updated `Metric`

        Returns: `Metric`
        """
        metric_api_response = self.__api.update_metric(
            metric_id=metric.id,
            name=metric.name,
            data_type=metric.data_type,
            external_id=metric.external_id,
            type_=metric.type,
            mapping_level=metric.mapping_level,
            discrete=metric.discrete,
            subject_type_id=metric.subject_type_id,
            unit=metric.unit,
            precision=int(metric.precision),
            visible=metric.visible,
        )

        metric = models.Metric.from_api_response(metric_api_response)
        return metric

    def delete_metric(self, id_: str):
        """Deletes a metric.

        Arguments:
            id_ [required]: Metric ID to delete

        Returns: `None`
        """
        self.__api.delete_metric(metric_id=id_)

    # Methods to create, update, delete and get subjects.

    def get_subjects(
        self,
        name: Optional[str] = None,
        subject_ids: List[str] = None,
        subject_external_id: Optional[str] = None,
        subject_type_ids: Optional[List[str]] = None,
        property_value_ids: Optional[Union[Tuple[str], List[str], str]] = None,
    ) -> List[models.Subject]:
        """Gets subjects, optionally with arguments for filtering.

        Arguments:
            name: Filter subjects by name.
            external_id: Filter subjects by external ID.
            subject_type_ids: Filter on a list of subject type IDs.
            property_value_ids: Filter property value IDs using a string or a combination of a list with tuples.
                For strings use a ',' separator for OR and ';' for AND, e.g. <A>,<B>;<C> translates to (A OR B) AND C.
                Instead of a string IDs can be encapsulate in a tuple for OR and encapsulate IDs in a list for AND.
                e.g. [('A', 'B'),'C'] translates to <A>,<B>;<C> a.k.a (A OR B) AND C.

        Returns: `Subject`
        """

        property_value_ids = convertions.convert_property_value_ids_to_query_filter(
            property_value_ids
        )

        subject_responses = self.__api.get_subjects(
            name=name,
            subject_ids=subject_ids,
            subject_external_id=subject_external_id,
            subject_type_ids=subject_type_ids,
            property_value_ids=property_value_ids,
        )

        subject_list = []
        for subject_response in subject_responses:
            subject_list.append(models.Subject.from_api_response(subject_response))
        return subject_list

    def get_subject(self, id_: str) -> Optional[models.Subject]:
        """Gets a specific subject.

        Arguments:
            id_ [required]: Subject ID to fetch.

        Returns: `Subject`
        """

        subject_response = self.__api.get_subject(subject_id=id_)
        if subject_response is None:
            return None
        subject = models.Subject.from_api_response(subject_response)
        return subject

    def create_subject(
        self,
        name: str,
        subject_type_id: str,
        parent_id: Optional[str] = None,
        properties: Optional[List[dict]] = None,
        ingestion_id_overrides: Optional[dict] = None,
        external_id: Optional[str] = None,
    ) -> models.Subject:
        """Creates a subject.

        Arguments:
            subject_type_id [required]:
                Subject type that this subjects belongs to. Determines which subjects, property types and metrics are connected.
            name [required]:
                The name of the subject.
            parent_id [optional, default=None]:
                The ID of the parent subject of this subject. Required if the subject type has a parent subject type. Not allowed otherwise.
            properties [optional, default=None]:
                List of the properties of this subject.
            ingestion_id_overrides [optional, default={} ]:
                Dictionary of metric ID ingestion ID pairs, ingestion ID’s belonging to metrics that are defined in the Subject Type but are not defined here will be automatically derived from the subject and metric external ID.
            external_id [optional, default=None]:
                The external ID of the subject. This can be used when sending measurements to avoid the source systems (e.g. sensors) need to know which IDs are internally used in the Blockbax Platform. If left empty the external ID will be derived from the given name but it is recommended that one is given.

        Returns: `Subject`
        """
        if ingestion_id_overrides is None:
            ingestion_id_overrides = {}
        ingestion_ids = []
        for metric_id, ingestion_id in ingestion_id_overrides.items():
            ingestion_ids.append(
                {
                    "metricId": metric_id,
                    "deriveIngestionId": False,
                    "ingestionId": ingestion_id,
                }
            )

        if external_id is None:
            external_id = convertions.convert_name_to_external_id(name=name)

        subject_response = self.__api.create_subject(
            name=name,
            parent_id=parent_id,
            subject_type_id=subject_type_id,
            external_id=external_id,
            ingestion_ids=ingestion_ids,
            properties=properties,
        )

        subject = models.Subject.from_api_response(subject_response)
        return subject

    def update_subject(
        self,
        subject: models.Subject,
    ) -> models.Subject:
        """Updates a subject.

        Arguments:
            subject [required]: Updated `Subject`

        Returns: `Subject`
        """

        properties = []
        for property_type_id, property_value in subject.properties.items():
            # important to note is that instead of giving a property values with an ID you can just give the corresponding value
            # Its better practice to just use value ID's if available and use the data type and value if not
            if property_value.inherit:
                properties.append(
                    {"typeId": property_type_id, "inherit": property_value.inherit}
                )
            elif property_value.id is not None:
                properties.append(
                    {"typeId": property_type_id, "valueId": property_value.id}
                )
            else:
                properties.append(
                    {
                        "typeId": property_type_id,
                        property_value.get_data_type(): property_value.get_value(),
                        "caption": property_value.caption,
                    }
                )

        ingestion_ids = []
        for ingestion in subject.ingestion_ids:
            if ingestion["deriveIngestionId"]:
                ingestion_ids.append(
                    {
                        "metricId": ingestion["metricId"],
                        "deriveIngestionId": ingestion["deriveIngestionId"],
                    }
                )
            else:
                ingestion_ids.append(ingestion)

        subject_response = self.__api.update_subject(
            subject_id=subject.id,
            name=subject.name,
            parent_id=subject.parent_id,
            subject_type_id=subject.subject_type_id,
            external_id=subject.external_id,
            ingestion_ids=ingestion_ids,
            properties=properties,
        )

        updated_subject = models.Subject.from_api_response(subject_response)

        return updated_subject

    def delete_subject(self, id_: str) -> None:
        """Deletes a subject.

        Arguments:
            id_ [required]: Subject ID to delete.

        Returns: `None`
        """

        self.__api.delete_subject(subject_id=id_)

    # Methods to queue, send and get measurements

    def queue_measurement(
        self,
        ingestion_id: str,
        date: Union[datetime.datetime, int, str],
        number: Optional[Union[decimal.Decimal, Number]] = None,
        location: Optional[Dict[str, Union[decimal.Decimal, Number, str]]] = None,
        text: Optional[str] = None,
    ):
        """Queues measurements to send.

        Arguments:
            ingestion_id [required]:
                Ingestion ID
            date [required]:
                `datetime`, Unix timestamp or string parsable by the dateutil.parser
            number [optional, default=None]:
                Decimal number, must be filled if location = None.
            location [optional, default=None]:
                Location dictionary, must be filled if number = None.

        Returns: `None`
        """
        if not self.__ingestions[ingestion_id]:
            self.__ingestions[ingestion_id] = models.Ingestion(id=ingestion_id)
        new_measurement = models.measurement.new(
            date=date, number=number, location=location, text=text
        )
        if new_measurement is not None:
            self.__ingestions[ingestion_id].add_measurement(new_measurement)

    def send_measurements(
        self,
        ingestion_ids: Optional[List[str]] = None,
        auto_create_subjects: bool = False,
    ):
        """Sends queued measurements.

        Arguments:
            ingestion_ids [optional, default=[] ]:
                List of ingestion IDs to send
            auto_create_subjects [optional, default=False]:
                Automatically creates a subject for its external ID derived from ingestionId if the subject does not exist (i.e. for the ingestion ID MyCar$Location a subject with external ID MyCar will be created if the metric with external ID Location can be linked to exactly one subject type).
            reset_on_success [optional, default=True]:
                Option to remove the measurements on success, default will always remove measurements after they have been send

        Returns: `None`
        """
        if ingestion_ids is None:
            ingestion_ids = []
        for series_to_send in self.__ingestions.create_series_to_send(
            ingestion_ids=ingestion_ids,
            subjects=self.get_subjects(),
            auto_create_subjects=auto_create_subjects,
        ):
            if series_to_send != []:
                self.__api.send_measurements(
                    series=series_to_send, auto_create_subjects=auto_create_subjects
                )
                if len(ingestion_ids) > 0:
                    for ingestion_id in ingestion_ids:
                        self.__ingestions[ingestion_id].measurements.clear()
                else:
                    self.__ingestions.clear_all()

    def get_measurements(
        self,
        subject_ids: list = [],
        metric_ids: list = [],
        from_date: Union[datetime.datetime, int, str] = None,
        to_date: Union[datetime.datetime, int, str] = None,
        size: int = None,
        order: str = None,
    ) -> List[models.Series]:
        """Gets measurements with arguments for filtering.

        Arguments:
            subject_ids [optional, default=[] ]:
                List of IDs of the subjects. When passing a fromDate or toDate, this must only contain one subject ID.
            metric_ids [optional, default=[] ]:
                List of IDs of the metrics. When passing a fromDate or toDate, this must only contain one metric ID.
            from_date [optional, default=None]:
                `datetime`, integer unix timestamp or string parsable by the dateutil.parser
            to_date [optional, default=None]:
                `datetime`, integer unix timestamp or string parsable by the dateutil.parser
            order [optional, default=asc]:
                Ordering of measurements based on the date ("asc" or "desc").

        Returns: List of `Series`
        """
        measurements_responses = self.__api.get_measurements(
            subject_ids=",".join(subject_ids) if subject_ids else None,
            metric_ids=",".join(metric_ids) if metric_ids else None,
            from_date=convertions.convert_any_date_to_iso8601(from_date)
            if from_date
            else None,
            to_date=convertions.convert_any_date_to_iso8601(to_date)
            if to_date
            else None,
            size=size,
            order=order,
        )
        series = []
        if measurements_responses is not None:
            for series_response in measurements_responses.get("series") or []:
                series.append(models.Series.from_api_response(series_response))
        return series
