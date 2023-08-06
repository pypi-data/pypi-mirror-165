from __future__ import annotations

from enum import Enum

from patterns.cli.services.api import Endpoints, post_for_json


def trigger_node(
    node_id: str,
    graph_version_uid: str,
    environment_uid: str,
    execution_type: str,
) -> list[dict]:
    return post_for_json(
        Endpoints.DEPLOYMENTS_TRIGGER_NODE,
        json={
            "node_id": node_id,
            "environment_uid": environment_uid,
            "graph_version_uid": graph_version_uid,
            "execution_type": execution_type,
        },
    )
