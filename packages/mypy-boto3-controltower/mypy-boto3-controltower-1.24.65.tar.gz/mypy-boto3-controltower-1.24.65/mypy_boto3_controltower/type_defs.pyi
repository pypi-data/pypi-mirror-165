"""
Type annotations for controltower service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controltower/type_defs/)

Usage::

    ```python
    from mypy_boto3_controltower.type_defs import ControlOperationTypeDef

    data: ControlOperationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

from .literals import ControlOperationStatusType, ControlOperationTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ControlOperationTypeDef",
    "DisableControlInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "EnableControlInputRequestTypeDef",
    "EnabledControlSummaryTypeDef",
    "GetControlOperationInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListEnabledControlsInputRequestTypeDef",
    "DisableControlOutputTypeDef",
    "EnableControlOutputTypeDef",
    "GetControlOperationOutputTypeDef",
    "ListEnabledControlsOutputTypeDef",
    "ListEnabledControlsInputListEnabledControlsPaginateTypeDef",
)

ControlOperationTypeDef = TypedDict(
    "ControlOperationTypeDef",
    {
        "endTime": datetime,
        "operationType": ControlOperationTypeType,
        "startTime": datetime,
        "status": ControlOperationStatusType,
        "statusMessage": str,
    },
    total=False,
)

DisableControlInputRequestTypeDef = TypedDict(
    "DisableControlInputRequestTypeDef",
    {
        "controlIdentifier": str,
        "targetIdentifier": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

EnableControlInputRequestTypeDef = TypedDict(
    "EnableControlInputRequestTypeDef",
    {
        "controlIdentifier": str,
        "targetIdentifier": str,
    },
)

EnabledControlSummaryTypeDef = TypedDict(
    "EnabledControlSummaryTypeDef",
    {
        "controlIdentifier": str,
    },
    total=False,
)

GetControlOperationInputRequestTypeDef = TypedDict(
    "GetControlOperationInputRequestTypeDef",
    {
        "operationIdentifier": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListEnabledControlsInputRequestTypeDef = TypedDict(
    "_RequiredListEnabledControlsInputRequestTypeDef",
    {
        "targetIdentifier": str,
    },
)
_OptionalListEnabledControlsInputRequestTypeDef = TypedDict(
    "_OptionalListEnabledControlsInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListEnabledControlsInputRequestTypeDef(
    _RequiredListEnabledControlsInputRequestTypeDef, _OptionalListEnabledControlsInputRequestTypeDef
):
    pass

DisableControlOutputTypeDef = TypedDict(
    "DisableControlOutputTypeDef",
    {
        "operationIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableControlOutputTypeDef = TypedDict(
    "EnableControlOutputTypeDef",
    {
        "operationIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetControlOperationOutputTypeDef = TypedDict(
    "GetControlOperationOutputTypeDef",
    {
        "controlOperation": ControlOperationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnabledControlsOutputTypeDef = TypedDict(
    "ListEnabledControlsOutputTypeDef",
    {
        "enabledControls": List[EnabledControlSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListEnabledControlsInputListEnabledControlsPaginateTypeDef = TypedDict(
    "_RequiredListEnabledControlsInputListEnabledControlsPaginateTypeDef",
    {
        "targetIdentifier": str,
    },
)
_OptionalListEnabledControlsInputListEnabledControlsPaginateTypeDef = TypedDict(
    "_OptionalListEnabledControlsInputListEnabledControlsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListEnabledControlsInputListEnabledControlsPaginateTypeDef(
    _RequiredListEnabledControlsInputListEnabledControlsPaginateTypeDef,
    _OptionalListEnabledControlsInputListEnabledControlsPaginateTypeDef,
):
    pass
