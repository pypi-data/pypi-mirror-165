# -*- coding: utf-8 -*-
from typing import Any, Dict
from google.cloud import orgpolicy_v2
from google.protobuf.json_format import MessageToDict
from matos_gcp_provider.lib import factory
from matos_gcp_provider.lib.base_provider import BaseProvider

class orgPolicy(BaseProvider):
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
        client = orgpolicy_v2.OrgPolicyClient(credentials=self.credentials)
        # request = orgpolicy_v2.ListConstraintsRequest(
        #     parent="projects/{}".format(self.project_id),
        # )
        # page_result = client.list_constraints(request=request)
        constraints_to_be_evaluate = ['projects/web-application-shared/constraints/iam.allowedPolicyMemberDomains']
        constraints = []
        for constraint in constraints_to_be_evaluate:
            policy_request = orgpolicy_v2.GetEffectivePolicyRequest(
                name=constraint.replace("constraints", "policies"),
            )
            policies = client.get_effective_policy(request=policy_request)
            constraints.append(
                {
                    "type": "orgPolicy",
                    "constraits_name": constraint,
                    "policies": MessageToDict(policies._pb)# pylint: disable=W0212
                }
            )
        return constraints

def register() -> Any:
    """Register plugins type"""
    factory.register("orgPolicy", orgPolicy)
