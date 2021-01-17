from fastapi import APIRouter, UploadFile, File

from aurora.core import karton

router = APIRouter(
    prefix="/sample",
    tags=["sample"],
)


@router.get("/")
def get_samples():
    return


@router.post("/")
def upload_sample(file: UploadFile = File(...)):
    karton.push_file(file, "123")

    return
