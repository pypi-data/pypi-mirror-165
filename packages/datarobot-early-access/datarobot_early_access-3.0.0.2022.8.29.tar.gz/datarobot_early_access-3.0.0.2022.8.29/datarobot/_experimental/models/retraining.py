#
# Copyright 2021-2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import List, Optional

import trafaret as t

from datarobot._compat import String
from datarobot.helpers.deployment_monitoring import DeploymentQueryBuilderMixin
from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate


class RetrainingPolicy(APIObject, DeploymentQueryBuilderMixin):
    """Retraining Policy.

    Attributes
    ----------
    policy_id : str
        ID of the retraining policy
    name : str
        Name of the retraining policy
    description : str
        Description of the retraining policy
    """

    _path = "deployments/{}/retrainingPolicies/"

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("name", optional=True): String(),
            t.Key("description", optional=True): String(allow_blank=True),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.id or self.name)

    @classmethod
    def list(cls, deployment_id: str) -> List[RetrainingPolicy]:
        """Lists all retraining policies associated with a deployment

        Parameters
        ----------
        deployment_id : str
            Id of the deployment

        Returns
        -------
        policies : list
            List of retraining policies associated with a deployment

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            from datarobot._experimental.models.retraining import RetrainingPolicy
            deployment = Deployment.get(deployment_id='620ed0e37b6ce03244f19631')
            RetrainingPolicy.list(deployment.id)
            >>> [RetrainingPolicy('620ed248bb0a1f5889eb6aa7'), RetrainingPolicy('624f68be8828ed81bf487d8d')]

        """

        path = cls._path.format(deployment_id)
        data = unpaginate(path, None, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, deployment_id: str, retraining_policy_id: str) -> "RetrainingPolicy":
        """Retrieves a retraining policy associated with a deployment

        Parameters
        ----------
        deployment_id : str
            Id of the deployment
        retraining_policy_id : str
            Id of the policy

        Returns
        -------
        retraining_policy : Retraining Policy
            Retraining policy

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.retraining import RetrainingPolicy
            policy = RetrainingPolicy.get(
                deployment_id='620ed0e37b6ce03244f19631',
                retraining_policy_id='624f68be8828ed81bf487d8d'
            )
            policy.id
            >>>'624f68be8828ed81bf487d8d'
            policy.name
            >>>'PolicyA'

        """

        path = "{}{}/".format(cls._path.format(deployment_id), retraining_policy_id)
        data = cls._client.get(path).json()
        return cls.from_server_data(data)

    @classmethod
    def delete(cls, deployment_id: str, retraining_policy_id: str) -> None:
        """Deletes a retraining policy associated with a deployment

        Parameters
        ----------
        deployment_id : str
            Id of the deployment
        retraining_policy_id : str
            Id of the policy

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.retraining import RetrainingPolicy
            RetrainingPolicy.delete(
                deployment_id='620ed0e37b6ce03244f19631',
                retraining_policy_id='624f68be8828ed81bf487d8d'
            )
        """

        path = "{}{}/".format(cls._path.format(deployment_id), retraining_policy_id)
        cls._client.delete(path)
