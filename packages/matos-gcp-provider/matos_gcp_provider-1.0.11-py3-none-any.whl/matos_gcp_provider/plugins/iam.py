# -*- coding: utf-8 -*-
# pylint: disable=E1101
from typing import Any, Dict
from collections import defaultdict
from googleapiclient import discovery
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider


class IAM(BaseProvider):
    """GCP cloud iam class

    Args:
        BaseProvider (Class): Base provider class
    """

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct IAM service
        """
        self.resource = resource
        self.resource_type = "iam"
        self.project_id = resource.pop("project_id")
        super().__init__(**kwargs)

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        service = discovery.build(
            "cloudresourcemanager", "v1", credentials=self.credentials
        )

        iam_policies = service.projects().getIamPolicy(resource=self.project_id).execute()# pylint: disable=duplicate-code
        identies = defaultdict(list)
        [[identies[identity].append(roles.get('role')) for identity in roles.get('members') if 'deleted' not in identity ] for roles in iam_policies.get("bindings")]# pylint: disable=expression-not-assigned
        iam_bindings= []
        for identity in identies:
            iam_bindings.append({'type': self.resource_type, 'principal': identity, 'roles': identies[identity]})
        return iam_bindings

def register() -> Any:
    """Register plugins type"""
    factory.register("iam", IAM)
