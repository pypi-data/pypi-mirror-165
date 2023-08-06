from myst.client import Client
from myst.openapi.models.node_job_create import NodeJobCreate
from myst.openapi.models.node_run_job_get import NodeRunJobGet


def request_sync(client: Client, project_uuid: str, uuid: str, json_body: NodeJobCreate) -> NodeRunJobGet:
    """Create an ad hoc run job for a time series."""

    return client.request(
        method="post",
        path=f"/projects/{project_uuid}/time_series/{uuid}:run",
        response_class=NodeRunJobGet,
        request_model=json_body,
    )
