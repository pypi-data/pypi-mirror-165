# -*- coding: utf-8 -*-
from typing import Any, Dict
from googleapiclient import discovery
from google.cloud import service_usage_v1
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider


class AuditLogs(BaseProvider):
    """GCP cloud auditlog class

    Args:
        BaseProvider (Class): Base provider class
    """

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct audit logs service
        """
        self.resource = resource
        self.project_id = resource.pop("project_id")
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        service = discovery.build(
            "cloudresourcemanager", "v1", credentials=self.credentials
        )

        iam_policies = (
            service.projects().getIamPolicy(resource=self.project_id).execute()
        )
        client = service_usage_v1.ServiceUsageClient(credentials=self.credentials)

        # Initialize request argument(s)
        request = service_usage_v1.ListServicesRequest(
            parent=f"projects/{self.project_id}", filter="state:ENABLED"
        )
        available_services = client.list_services(request=request)
        enabled_audit_logs = {}
        for auditConfig in iam_policies.get("auditConfigs"):
            enabled_audit_logs[auditConfig.get("service")] = auditConfig.get(
                "auditLogConfigs"
            )
        final_services = []
        for service in available_services:
            auditLogConfigs = []
            if enabled_audit_logs.get(service.config.name):
                auditLogConfigs = enabled_audit_logs.get(service.config.name)
            final_services.append(
                {
                    "type": "AuditLogs",
                    "service": service.config.name,
                    "auditLogConfigs": auditLogConfigs,
                }
            )
        return final_services


def register() -> Any:
    """Register plugins type"""
    factory.register("AuditLogs", AuditLogs)
