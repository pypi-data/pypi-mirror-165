"""
Main interface for controltower service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_controltower import (
        Client,
        ControlTowerClient,
        ListEnabledControlsPaginator,
    )

    session = Session()
    client: ControlTowerClient = session.client("controltower")

    list_enabled_controls_paginator: ListEnabledControlsPaginator = client.get_paginator("list_enabled_controls")
    ```
"""
from .client import ControlTowerClient
from .paginator import ListEnabledControlsPaginator

Client = ControlTowerClient


__all__ = ("Client", "ControlTowerClient", "ListEnabledControlsPaginator")
