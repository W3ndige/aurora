from typing import List, Tuple
from pyvis.network import Network  # type: ignore

from aurora.database import models


def prepare_large_graph(relations: List[models.Relation]) -> Tuple[List, List]:
    nodes = {}
    edges = []
    for relation in relations:
        nodes[relation.parent_id] = {
            "id": relation.parent_id,
            "label": relation.parent.filename,
            "shape": "dot"
        }

        nodes[relation.child_id] = {
            "id": relation.child_id,
            "label": relation.child.filename,
            "shape": "dot"
        }

        edges.append(
            {
                "from": relation.parent_id,
                "to": relation.child_id,
            }
        )

    return (list(nodes.values()), edges)


def prepare_sample_graph(relations: List[models.Relation]) -> Tuple[List, List]:
    nodes = {}
    edges = []
    for relation in relations:
        nodes[relation.parent_id] = {
            "id": relation.parent_id,
            "label": relation.parent.filename,
            "shape": "dot"
        }

        nodes[relation.child_id] = {
            "id": relation.child_id,
            "label": relation.child.filename,
            "shape": "dot"
        }

        edges.append(
            {
                "from": relation.parent_id,
                "to": relation.child_id,
            }
        )

    return (list(nodes.values()), edges)