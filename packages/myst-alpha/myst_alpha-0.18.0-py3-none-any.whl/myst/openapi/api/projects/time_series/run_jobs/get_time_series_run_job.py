from myst.client import Client
from myst.openapi.models.node_run_job_get import NodeRunJobGet


def request_sync(client: Client, project_uuid: str, time_series_uuid: str, uuid: str) -> NodeRunJobGet:
    """Gets a time series run job by its unique identifier."""

    return client.request(
        method="get",
        path=f"/projects/{project_uuid}/time_series/{time_series_uuid}/run_jobs/{uuid}",
        response_class=NodeRunJobGet,
    )
