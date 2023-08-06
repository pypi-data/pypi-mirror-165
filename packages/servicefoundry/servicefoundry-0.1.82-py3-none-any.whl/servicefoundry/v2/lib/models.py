import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra


class BuildResponse(BaseModel):
    id: str
    name: str
    # TODO: make status an enum
    status: str
    # TODO: should we just make these fields
    # snake-case and add camelCase aliases?
    deploymentId: str
    componentName: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    fqn: str
    # TODO: Dict -> pydantic model if required
    buildSpecData: Dict[str, Any]
    dockerRegistryId: str
    imageUri: Optional[str]
    failureReason: Optional[str]
    getLogsUrl: str
    tailLogsUrl: str
    logsStartTs: int

    class Config:
        extra = Extra.allow


class Deployment(BaseModel):
    id: str
    fqn: str
    version: str
    # TODO: Dict -> pydantic model if required
    manifest: Dict[str, Any]
    # TODO: make status an enum
    status: str
    createdBy: str
    applicationId: str
    workspaceId: str
    failureReason: Optional[str]
    createdAt: datetime.datetime
    active: int
    updatedAt: datetime.datetime
    # TODO: Dict -> pydantic model if required
    application: Dict[str, Any]
    # TODO: Dict -> pydantic model if required
    workspace: Dict[str, Any]
    baseDomainURL: str
    builds: List[BuildResponse]

    class Config:
        extra = Extra.allow
