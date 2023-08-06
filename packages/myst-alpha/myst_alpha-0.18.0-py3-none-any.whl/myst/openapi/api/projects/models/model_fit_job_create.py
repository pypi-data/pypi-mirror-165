from myst.client import Client
from myst.openapi.models.model_fit_job_get import ModelFitJobGet
from myst.openapi.models.node_job_create import NodeJobCreate


def request_sync(client: Client, project_uuid: str, uuid: str, json_body: NodeJobCreate) -> ModelFitJobGet:
    """Create an ad hoc fit job for a model."""

    return client.request(
        method="post",
        path=f"/projects/{project_uuid}/models/{uuid}:fit",
        response_class=ModelFitJobGet,
        request_model=json_body,
    )
