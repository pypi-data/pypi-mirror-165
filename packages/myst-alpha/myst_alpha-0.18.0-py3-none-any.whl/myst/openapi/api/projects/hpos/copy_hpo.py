from myst.client import Client
from myst.openapi.models.hpo_get import HPOGet


def request_sync(client: Client, project_uuid: str, uuid: str) -> HPOGet:
    """Copies an HPO."""

    return client.request(method="post", path=f"/projects/{project_uuid}/hpos/{uuid}:copy", response_class=HPOGet)
