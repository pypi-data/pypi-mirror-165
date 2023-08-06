# -*- coding: utf-8 -*-
from typing import Any, Dict
from googleapiclient import discovery
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider


class serviceAccount(BaseProvider):
    """GCP service account class

    Args:
        BaseProvider (Class): Base provider class
    """

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct service acounts service
        """
        self.resource = resource
        self.resource_type = "iam.googleapis.com/ServiceAccount"
        self.project_id = resource.pop("project_id")
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        service_accounts = []
        resources = self._get_assets(self.project_id, self.resource_type)
        service = discovery.build("iam", "v1", credentials=self.credentials)
        request = service.projects().serviceAccounts()
        for resource in resources:
            service_accounts.append(
                {
                    "type": "serviceAccount",
                    **resource.get("resource").get("data"),
                    "getPolicy": request.getIamPolicy(
                        resource=resource.get("resource").get("data").get("name")
                    ).execute(),
                    **request.keys()
                    .list(name=resource.get("resource").get("data").get("name"))
                    .execute(),
                }
            )
        return service_accounts


def register() -> Any:
    """Register plugins type"""
    factory.register("serviceAccount", serviceAccount)
