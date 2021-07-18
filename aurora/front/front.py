import logging
import starlette.status as status

from typing import cast, List, Optional
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException, Form
from starlette.templating import Jinja2Templates

from aurora.core import karton
from aurora.core import search
from aurora.core import network as net
from aurora.core.utils import get_magic, get_sha256
from aurora.database import get_db, queries, models, schemas

templates = Jinja2Templates(directory="aurora/front/templates/")

router = APIRouter()


logger = logging.getLogger(__name__)


@router.get("/", response_class=HTMLResponse)
def index(request: Request, offset: int = 0, db=Depends(get_db)):
    samples = queries.sample.get_samples(db, offset=offset)

    samples_with_info = []
    for sample in samples:
        samples_with_info.append(
            {
                "sample": sample,
                "rel_size": len(queries.sample.get_sample_related(db, sample)),
            }
        )

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "samples_with_info": samples_with_info, "offset": offset},
    )


@router.get("/upload", response_class=HTMLResponse)
def get_upload(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/upload", response_class=RedirectResponse)
def post_upload(file: UploadFile = File(...), db=Depends(get_db)):
    sha256 = get_sha256(file.file)
    sample = queries.sample.get_sample_by_sha256(db, sha256)
    if not sample:
        sample = queries.sample.add_sample(db, file)

    if not sample.ssdeep:
        ssdeep = queries.ssdeep.add_ssdeep(db, file)
        sample.ssdeep = ssdeep

        try:
            karton.push_ssdeep(sample.sha256, ssdeep.chunksize, ssdeep.ssdeep)
        except RuntimeError:
            logger.exception(f"Couldn't push Sample to karton. Sample {sample.sha256}")

    db.commit()

    try:
        sample_mime = get_magic(file.file, mimetype=True)
        karton.push_file(file, sample_mime, sample.sha256)
    except RuntimeError:
        pass

    return RedirectResponse(f"/sample/{sha256}", status_code=status.HTTP_302_FOUND)


@router.get("/sample/{sha256}", response_class=HTMLResponse)
def sample_index(request: Request, sha256: str, db=Depends(get_db)):
    sample = queries.sample.get_sample_by_sha256(db, sha256)

    if not sample:
        raise HTTPException(status_code=404, detail=f"Sample {sha256} not found.")

    sample_ssdeep = sample.ssdeep.ssdeep
    related_samples = list(queries.sample.get_sample_related(db, sample))

    db_relations = queries.relation.get_relations_by_hash(db, sample)

    nodes, edges = net.prepare_sample_graph(db_relations)

    return templates.TemplateResponse(
        "sample/related.html",
        {
            "request": request,
            "sample": sample,
            "sample_ssdeep": sample_ssdeep,
            "related_samples": related_samples,
            "nodes": nodes,
            "edges": edges,
        },
    )


@router.get("/sample/{sha256}/relations", response_class=HTMLResponse)
def get_sample_relations(request: Request, sha256: str, db=Depends(get_db)):
    sample = queries.sample.get_sample_by_sha256(db, sha256)

    if not sample:
        raise HTTPException(status_code=404, detail=f"Sample {sha256} not found.")

    sample_ssdeep = sample.ssdeep.ssdeep
    db_relations = queries.relation.get_relations_by_hash(db, sample)

    nodes, edges = net.prepare_sample_graph(db_relations)

    return templates.TemplateResponse(
        "sample/relations.html",
        {
            "request": request,
            "sample": sample,
            "sample_ssdeep": sample_ssdeep,
            "relations": db_relations,
            "nodes": nodes,
            "edges": edges,
        },
    )


@router.get("/sample/{sha256}/strings", response_class=HTMLResponse)
def get_sample_strings(request: Request, sha256: str, db=Depends(get_db)):
    sample = queries.sample.get_sample_by_sha256(db, sha256)

    if not sample:
        raise HTTPException(status_code=404, detail=f"Sample {sha256} not found.")

    sample_ssdeep = sample.ssdeep.ssdeep
    strings = sample.strings

    db_relations = queries.relation.get_relations_by_hash(db, sample)

    nodes, edges = net.prepare_sample_graph(db_relations)

    return templates.TemplateResponse(
        "sample/strings.html",
        {
            "request": request,
            "sample": sample,
            "sample_ssdeep": sample_ssdeep,
            "strings": strings,
            "nodes": nodes,
            "edges": edges,
        },
    )


@router.get("/sample/{sha256}/network", response_class=HTMLResponse)
def get_sample_network(request: Request, sha256: str, db=Depends(get_db)):
    sample = queries.sample.get_sample_by_sha256(db, sha256)

    if not sample:
        raise HTTPException(status_code=404, detail=f"Sample {sha256} not found.")

    db_relations = queries.relation.get_relations_by_hash(db, sample)

    nodes, edges = net.prepare_sample_graph(db_relations)

    return templates.TemplateResponse(
        "network.html",
        {"request": request, "nodes": nodes, "edges": edges},
    )


@router.get("/string", response_class=HTMLResponse)
def get_strings(request: Request, offset: int = 0, db=Depends(get_db)):
    strings = queries.string.get_unique_strings(db, offset=offset)

    return templates.TemplateResponse(
        "string/strings.html",
        {"request": request, "offset": offset, "strings": strings},
    )


@router.get("/string/{sha256}", response_class=HTMLResponse)
def get_string(request: Request, sha256: str, db=Depends(get_db)):
    string = queries.string.get_string_by_sha256(db, sha256)

    if not string:
        raise HTTPException(status_code=404, detail=f"String {sha256} not found.")

    string_samples = queries.sample.get_samples_with_string(db, string)

    return templates.TemplateResponse(
        "string/index.html",
        {"request": request, "string": string, "related_samples": string_samples},
    )


@router.get("/relations", response_class=HTMLResponse)
def get_relations(request: Request, offset: int = 0, db=Depends(get_db)):
    relations = queries.relation.get_relations(db, offset=offset)

    return templates.TemplateResponse(
        "relations.html", {"request": request, "offset": offset, "relations": relations}
    )


@router.post("/search", response_class=HTMLResponse)
def post_search(request: Request, query: str = Form(...), db=Depends(get_db)):
    prefix, term = search.prepare_search(query)
    if not prefix or not term:
        return None

    try:
        prefix, attribute = prefix.split(".")
    except ValueError:
        logger.warning(f"Couldn't split {prefix}.")
        return None

    if prefix.startswith("string"):
        strings = cast(models.String, search.string_search(db, attribute, term))

        return templates.TemplateResponse("string/strings.html", {"request": request, "strings": strings, "offset": 0})

    elif prefix.startswith("sample"):
        samples = cast(models.Sample, search.sample_search(db, attribute, term))
        samples_with_info = []
        for sample in samples:
            samples_with_info.append(
                {
                    "sample": sample,
                    "rel_size": len(queries.sample.get_sample_related(db, sample)),
                }
            )

        return templates.TemplateResponse("index.html",
                                        {"request": request, "samples_with_info": samples_with_info, "offset": 0})