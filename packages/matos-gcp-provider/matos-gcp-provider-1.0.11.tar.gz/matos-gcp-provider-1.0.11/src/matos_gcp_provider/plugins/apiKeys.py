# -*- coding: utf-8 -*-
from typing import Any, Dict
from google.cloud import api_keys_v2
from google.protobuf.json_format import MessageToDict
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider


class apiKeys(BaseProvider):
    """GCP instance class

    Args:
        BaseProvider (Class): Base provider class
    """

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct instance service
        """
        self.project_id = resource.pop("project_id")
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery for organization policies
        """
        client = api_keys_v2.ApiKeysClient(credentials=self.credentials)
        request = api_keys_v2.ListKeysRequest(
            parent=f"projects/{self.project_id}/locations/global"
        )
        page_result = client.list_keys(request=request)
        api_keys = []
        for response in page_result:
            api_keys.append({"type":"apiKeys", **MessageToDict(response._pb)})# pylint: disable=W0212
        return api_keys

def register() -> Any:
    """Register plugins type"""
    factory.register("apiKeys", apiKeys)
