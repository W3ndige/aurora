from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates

from aurora.core import network as net
from aurora.database import get_db, queries, schemas, models

templates = Jinja2Templates(directory="aurora/front/templates/")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request, offset: int = 0, db=Depends(get_db)):
    samples = queries.sample.get_samples(db, offset=offset)

    return templates.TemplateResponse(
        "index.html", {"request": request, "samples": samples, "offset": offset}
    )


@router.get("/network", response_class=HTMLResponse)
def index(
    request: Request,
    relation_type: Optional[str] = None,
    confidence: Optional[str] = None,
    db=Depends(get_db)
):
    if relation_type:
        relation_type = models.RelationType[relation_type]

    filters = schemas.RelationFilter(
        relation_type=relation_type,
        confidence=confidence
    )

    relations = queries.relation.get_simplified_relations(db, filters)
    network = net.create_simplified_graph(relations)

    nodes, edges, heading, height, width, options = network.get_network_data()

    return templates.TemplateResponse(
        "network.html", {
            "request": request,
            "nodes": nodes,
            "edges": edges,
            "options": options
        }
    )


@router.get("/sample/{sha256}/network", response_class=HTMLResponse)
def index(request: Request, sha256: str, db=Depends(get_db)):

    sample = queries.sample.get_sample_by_sha256(db, sha256)
    sample_relations = queries.relation.get_relations_by_hash(db, sample)

    network = net.create_network(sample_relations)

    nodes, edges, heading, height, width, options = network.get_network_data()

    return templates.TemplateResponse(
        "network.html", {
            "request": request,
            "nodes": nodes,
            "edges": edges,
            "options": options
        }
    )