from typing import List
from pyvis.network import Network

from aurora.database import models


def create_network(relations: List[models.Relation]) -> Network:
    network = Network()
    network.barnes_hut()

    for relation in relations:
        network.add_node(
            relation.parent_id, label=relation.parent.sha256, title=relation.parent.filename
        )

        network.add_node(
            relation.child_id, label=relation.child.sha256, title=relation.child.filename
        )

        network.add_edge(
            relation.parent_id, relation.child_id, title=relation.relation_type.value
        )


    network.set_edge_smooth("dynamic")
    return network



