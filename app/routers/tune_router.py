from datetime import datetime
import os
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, Request, status, Form, UploadFile
from sqlalchemy.orm import Session
from ..core.config import settings
from ..database import  crud
from ..dependencies import dependencies
from ..pydantics.tune import TuneCreate, Tune, TuneUpdate

router = APIRouter(
    tags=['Tunes'],
    prefix="/tunes"
)

UPLOAD_DIR = "app/uploads/"


@router.post("/", response_model=Tune)
async def create_tune(
    request: Request,
    name: str = Form(...),
    code: int = Form(...),
    file: UploadFile = File(...),
    user_id: int = Form(...),
    db: Session = Depends(dependencies.get_db)
): 
    contents = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    if os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File with the name {file.filename} exits")
    tune_in_db = crud.get_tune(db=db, code=code)
    if tune_in_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Tune with code {code} already exist!")
    
    tune_data =TuneCreate(name=name, code=code, user_id=user_id, file_name=file.filename.strip().replace(" ", "_"))
    db_tune = crud.create_tune(db=db, tune=tune_data)
    
    with open(file_path, "wb") as f:
        f.write(contents)

    return db_tune

@router.get("/")
async def read_tunes(request: Request, skip: int = 0, limit: int = 100, searchText:Optional[str]='', 
                     db: Session = Depends(dependencies.get_db)):
    tunes = crud.get_tunes(db, skip=skip, limit=limit, search=searchText)
    if not tunes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No SKiza tunes found")
    for tune in tunes:
        tune.file_name = f"{request.url.scheme}://{request.url.netloc}/uploads/{tune.file_name}"
    return tunes

@router.delete("/{tune_id}")
def delete_tune(tune_id: int,  db: Session = Depends(dependencies.get_db)):
    db_tune = crud.get_tune_by_id(db=db, tune_id=tune_id)
    if db_tune is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"tune not found!"})
    
    file_path = os.path.join("app/uploads", db_tune.file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
    
    crud.delete_tune(db=db, tune_id=tune_id)
    return db_tune

@router.put("/{tune_id}", response_model=Tune)
async def edit_tune(
    request: Request,
    tune_id: int,
    name: str = Form(...),
    code: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(dependencies.get_db)
):
    base_url = str(request.base_url)  
    cleaned_name = name.replace(" ", "")
    cleaned_name = name.replace(" ", "")
    image_url = f"{base_url}uploads/{cleaned_name}"
    contents = await file.read()
    file_path = os.path.join(UPLOAD_DIR, cleaned_name)

    with open(file_path, "wb") as f:
        f.write(contents)

    tune_data = TuneUpdate(name=name, code=code, file_name=image_url)
    print(tune_data)
    updated_tune = crud.update_tune(db=db, id=tune_id, tune=tune_data)

    if not updated_tune:
        raise HTTPException(status_code=404, detail="Tune not found")
    
    return updated_tune