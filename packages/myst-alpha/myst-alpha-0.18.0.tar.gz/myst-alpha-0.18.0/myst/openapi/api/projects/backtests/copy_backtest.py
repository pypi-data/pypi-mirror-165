from myst.client import Client
from myst.openapi.models.backtest_get import BacktestGet


def request_sync(client: Client, project_uuid: str, uuid: str) -> BacktestGet:
    """Copies a backtest."""

    return client.request(
        method="post", path=f"/projects/{project_uuid}/backtests/{uuid}:copy", response_class=BacktestGet
    )
