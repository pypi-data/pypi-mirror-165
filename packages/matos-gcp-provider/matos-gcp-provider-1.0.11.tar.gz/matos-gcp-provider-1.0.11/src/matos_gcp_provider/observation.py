# -*- coding: utf-8 -*-
# pylint: disable-all
import time
from google.cloud import monitoring_v3
from google.protobuf.json_format import MessageToDict
import json
from matos_gcp_provider.lib.auth import Connection
from matos_gcp_provider.config import GCPConfig
from matos_gcp_provider.lib.utils import Joiners

GCP_METRIC_DETAILS = None
METRIC_DETAILS = None
METRIC_RESOURCE_TYPE = None


class GCPObservation(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = None

    @property
    def client(self):

        if self._client is not None:
            return self._client

        self._client = monitoring_v3.MetricServiceClient(credentials=self.credentials)

        return self._client

    def build_filter_query(
        self,
        queries: list,
        operator="AND",
        quoted=True,
    ):
        """
        In order to apply filter to metrices, we need to build a string query
        and send it as a param to gcp APIs, which is build here.
        """

        query_list = []

        queries = (
            [(x, y) for x, y in queries.items()]
            if isinstance(queries, dict)
            else queries
        )

        for q in queries:
            if isinstance(q, (tuple, list, dict)):
                key, value = tuple(q.items())[0] if isinstance(q, dict) else q
                value = f'"{value}"' if quoted else value
                query_list.append(f"{key} = {value}")
            else:
                query_list.append(q)

        op = f" {operator} " if operator.strip() else operator
        return op.join(query_list)

    def get_metric_descriptors(
        self,
        project_id,
    ):
        """
        Used to call metric_descriptors API of GCP which returns
        all metric related filters list applicable to different metrices
        i.e. metric.type, instance_id
        """

        response = self.client.list_metric_descriptors(name=f"projects/{project_id}")

        return [MessageToDict(x) for x in response]

    def get_resource_descriptors(
        self,
        project_id,
    ):
        """
        Used to call resource_descriptors API of GCP which returns
        all resource related filters list applicable to different metrices
        i.e. cluster_name, node_name
        """

        response = self.client.list_monitored_resource_descriptors(
            name=f"projects/{project_id}"
        )

        return [MessageToDict(x) for x in response]

    def extract_metric_type_and_filters(
        self,
        metric_descriptors,
        resource_descriptors=None,
    ):
        """
        Metric details are fetched from GCP which contains valueType
        and filters for that metric. Here it's parsed which is eventually
        saved as a global variable.
        """

        metric_configs = {}
        resource_configs = {}
        combined = {}

        for metric in metric_descriptors:
            config = {
                "metric_kind": metric["metricKind"],
                "value_type": metric["valueType"],
            }

            if "labels" in metric:
                config.update(labels=[label["key"] for label in metric["labels"]])

            metric_configs[metric["type"]] = config

        for resource in resource_descriptors or []:
            config = {
                "display_name": resource["displayName"],
                "description": resource["description"],
            }

            if "labels" in resource:
                config.update(labels=[label["key"] for label in resource["labels"]])

            resource_configs[resource["type"]] = config

        for metric_name, metric_config in (METRIC_RESOURCE_TYPE or {}).items():

            resource_types = metric_config["target_resource_types"]
            metric = metric_configs.get(metric_name)
            resources = [resource_configs.get(r) for r in resource_types]
            resources = [r for r in resources if r]

            if not (metric and resources):
                continue

            resource_labels = set()

            for resource in resources:
                resource_labels.update(resource.get("labels", []))

            new = metric.copy()
            new["resource_types"] = resource_types
            new["metric_labels"] = metric.get("labels", [])
            new["resource_labels"] = list(resource_labels)
            new.pop("labels", None)

            combined[metric_name] = new

        return {
            "metrics": metric_configs,
            "resources": resource_configs,
            "merged": combined,
        }

    def read_metrics_file(
        self,
        filename,
    ):
        with open(filename, "r") as f:
            data = json.load(f)

        metric_to_resource_type = {}

        for source_info in data.values():

            if "gcp" not in source_info["providers"]:
                continue

            gcp_metric = source_info["providers"]["gcp"]
            metric_to_resource_type[gcp_metric["metric"]] = gcp_metric

        return data, metric_to_resource_type

    def get_metric_details(
        self,
        project_id: str,
    ):
        """
        used to fetch metrics details (value type, available filters)
        by metric names, from GCP.
        """

        metric_descriptors = self.get_metric_descriptors(project_id)
        resource_descriptors = self.get_resource_descriptors(project_id)

        retval = self.extract_metric_type_and_filters(
            metric_descriptors,
            resource_descriptors,
        )

        return retval

    def get_time_interval(
        self,
        t,
    ):
        """
        returns a GCP time interval (from current_time seconds
        to current_time-t seconds)
        """

        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        interval = monitoring_v3.TimeInterval(
            {
                "end_time": {"seconds": seconds, "nanos": nanos},
                "start_time": {"seconds": (seconds - t), "nanos": nanos},
            }
        )

        return interval

    def build_aggregator(
        self,
        metric,
        align=True,
        alignment_period=60,
        reduce=True,
        group_by=None,
    ):
        """
        Time series aggregation happens to squeeze time series data
        and take a single value output by applying some statistics method
        i.e. mean, max etc.
        GCP has its own method to do at their end itself, but in order to do
        that we pass a parameter which defines how it needs to be done which
        is defined here.
        """

        aggregator = {}
        metric_details = GCP_METRIC_DETAILS["metrics"][metric]

        metric_kind, value_type = (
            metric_details["metric_kind"],
            metric_details["value_type"],
        )

        aligner, reducer = GCPConfig.aggregation_map.get(
            (metric_kind, value_type), (None, None)
        )

        if align and aligner:
            aggregator.update(
                per_series_aligner=aligner,
                alignment_period={"seconds": alignment_period},
            )

            if reduce and reducer:
                aggregator.update(cross_series_reducer=reducer)

                if group_by:
                    group_by = group_by.copy()
                    group_by = [group_by] if isinstance(group_by, str) else group_by
                    group_by = self.convert_filter_names(group_by)
                    aggregator.update(group_by_fields=group_by)

        return aggregator

    def convert_filter_names(
        self,
        filters,
    ):
        """
        filter names are made generic in our system like cluster, node etc.
        But these filter have different alias for different cloud provider.
        Here we convert generalized name to provider (i.e. GCP) specific name
        i.e cluster -> resource.labels.cluster_name
        """

        is_dict = isinstance(filters, dict)

        new = {} if is_dict else []

        for key in filters:
            target_name = GCPConfig.filter_name_map.get(key)

            if is_dict:
                new[(target_name or key)] = filters[key]
            else:
                new.append((target_name or key))

        return new

    def extract_values(
        self,
        metric,
    ):
        """
        Used to extract value from GCP Metrics depending on it's
        value type
        """

        value_type = GCPConfig.value_type_map[metric.value_type]
        value_key = value_type.lower() + "_value"

        values = []

        for point in metric.points:
            value = getattr(point.value, value_key)

            if value_type == "DISTRIBUTION":
                value = value.mean

            values.append(value)

        return values

    def parse_group_values(
        self,
        metric,
        group_by=None,
    ):
        """
        single metric can have different groups as per their properties
        like cluster, node etc. These group values need to parsed from
        time serires which happens here.
        """

        filter_name_map_inverted = {x: y for y, x in GCPConfig.filter_name_map.items()}

        def get_labels_dict(metric, category):
            return MessageToDict(getattr(metric, category)).get("labels", {})

        def pick_keys(d, keys, category):
            def filter_name(k):
                return f"{category}.labels.{k}"

            return {
                (filter_name_map_inverted.get(filter_name(k)) or k): v
                for k, v in d.items()
                if filter_name(k) in keys
            }

        keys = [(GCPConfig.filter_name_map.get(key) or key) for key in (group_by or [])]

        resource_labels = get_labels_dict(metric, "resource")
        metric_labels = get_labels_dict(metric, "metric")

        combined = {}

        if keys:
            resource_values = pick_keys(resource_labels, keys, "resource")
            metric_values = pick_keys(metric_labels, keys, "metric")

            combined = {**resource_values, **metric_values}

        if not combined:
            combined = {**resource_labels, **metric_labels}

        return combined

    def parse_values(
        self, metric_results, align=True, aligner="mean", group_by=None, filters={}
    ):
        """
        Parsed the values from a time series, and return either list of values
        or a single value, depending on if align is True.
        """
        retlist = []

        for metric in metric_results:

            d = {}
            values = self.extract_values(metric)

            if align:
                aligner_method = getattr(Joiners, aligner)
                d.update(value=aligner_method(values))
            else:
                d.update(values=values)

            d.update(filters)
            d.update(self.parse_group_values(metric, group_by))
            retlist.append(d)

        return retlist

    def get_time_series(
        self,
        project_id,
        metric,
        filters={},
        time_period=60,
        align=True,
        alignment_period=60,
        reduce=True,
        group_by=None,
    ):
        """
        Returns Observed Time series data for given metric.
        PARAMS:
            metric: metric type to be fetched e.g
                    metric='loadbalancing.googleapis.com/https/latencies'
            filters: filters related to that metric type e.g. cluster=some
            time_period: time series range period
            align: Whether to squeeze the time series into one value
            alignment_period: Squeeze period
            reduce: reduce can be used to squeeze time serires based on
                    their properties and make sub-aggregations
            group_by: filter name by which reduction to happen
        """

        interval = self.get_time_interval(time_period)
        aggregator = self.build_aggregator(
            metric=metric,
            align=align,
            alignment_period=alignment_period,
            reduce=reduce,
            group_by=group_by,
        )

        modified_filters = filters.copy()
        modified_filters["metric.type"] = metric
        modified_filters = self.convert_filter_names(modified_filters)
        filter_query = self.build_filter_query(modified_filters)

        request = {
            "name": f"projects/{project_id}",
            "filter": filter_query,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }

        if aggregator:
            aggregation = monitoring_v3.Aggregation(aggregator)
            request.update(aggregation=aggregation)

        results = self.client.list_time_series(request=request)

        parse_request = dict(
            metric_results=list(results),
            align=align,
            group_by=group_by,
            filters=filters,
        )

        aligner = METRIC_RESOURCE_TYPE[metric].get("aligner")
        if aligner:
            parse_request.update(aligner=aligner, align=True)

        return self.parse_values(**parse_request)

    def load_configurations(
        self,
        project_id,
    ):
        """
        load configurations from file and gcp, to global variables.
        """

        global GCP_METRIC_DETAILS
        global METRIC_DETAILS
        global METRIC_RESOURCE_TYPE

        if not METRIC_DETAILS:
            METRIC_DETAILS, METRIC_RESOURCE_TYPE = self.read_metrics_file(
                "common/assets/metrics.json"
            )

        if not GCP_METRIC_DETAILS:
            GCP_METRIC_DETAILS = self.get_metric_details(project_id)

    def get_metrics_observation(
        self,
        project_id: str,
        metric_with_filters: dict,
        time_period=300,
    ):

        self.load_configurations(project_id)

        metric_results = {}

        for metric, filters in metric_with_filters.items():

            if metric in METRIC_DETAILS:
                metric_config = METRIC_DETAILS[metric]["providers"]["gcp"]
                metric_type = metric_config["metric"]
                default_filters = metric_config.get("filters", {})
                align = False if "aligner" in metric_config else True
                base_resource_type = metric.split(".")[0]
                group_by = [base_resource_type]
                filters.update(default_filters)
                metric_results[metric] = self.get_time_series(
                    project_id=project_id,
                    metric=metric_type,
                    filters=filters,
                    align=align,
                    time_period=time_period,
                    alignment_period=time_period,
                    group_by=group_by,
                )
            else:
                metric_results[metric] = self.get_time_series(
                    project_id=project_id,
                    metric=metric,
                    time_period=time_period,
                    alignment_period=time_period,
                )

        return metric_results
