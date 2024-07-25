from datetime import datetime
import os
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, status, Form, UploadFile
from sqlalchemy.orm import Session
# from core.config import settings
from ..core.config import settings
from ..database import  crud
from ..dependencies import dependencies
from ..pydantics.tune import TuneCreate, Tune, TuneUpdate

router = APIRouter(
    tags=['Tunes'],
    prefix="/tunes"
)
default_url = settings.default_url
uploads_dir =  default_url + "uploads"


@router.post("/", response_model=Tune)
async def create_tune(
    name: str = Form(...),
    code: int = Form(...),
    file: UploadFile = File(...),
    user_id: int = Form(...),
    db: Session = Depends(dependencies.get_db)
):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_extension = os.path.splitext(file.filename)[1]
    cleaned_name = name.replace(" ", "")
    formatted_name = f"{cleaned_name}_{timestamp}{file_extension}"
    contents = await file.read()
    tune_data = TuneCreate(name=name, code=code, user_id=user_id, file_name=formatted_name)
    db_tune = crud.create_tune(db=db, tune=tune_data)
    file_path = f"uploads/{formatted_name}"
    with open(file_path, "wb") as f:
        f.write(contents)
    return db_tune

@router.get("/")
async def read_tunes(skip: int = 0, limit: int = 100, searchText:Optional[str]='', db: Session = Depends(dependencies.get_db)):
    tunes_indb = crud.get_tunes(db, skip=skip, limit=limit, search=searchText)
    if not tunes_indb:
        raise HTTPException(status_code=404, detail="No SKiza tunes found")
    tunes = []
    for tune in tunes_indb:
        file_name = tune.file_name
        if file_name:
            file_path = os.path.join(uploads_dir, tune.file_name)
            print(file_path)
            file_info = {
                "id":tune.id,
                "name":tune.name,
                "code":tune.code,
                "file_path":file_path,
                "fileName":file_name
            }
            tunes.append(file_info) 
        else:
            print("Skipping tune with no file_name")
    return tunes

@router.delete("/{tune_id}")
def delete_tune(tune_id: int,  db: Session = Depends(dependencies.get_db)):
    db_tune = crud.delete_tune(db=db, tune_id=tune_id)
    if db_tune is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"tune not found!"})
    return db_tune

@router.put("/{tune_id}", response_model=Tune)
async def edit_tune(
    tune_id: int,
    name: str = Form(...),
    code: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(dependencies.get_db)
):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_extension = os.path.splitext(file.filename)[1]
    cleaned_name = name.replace(" ", "")
    formatted_name = f"{cleaned_name}_{timestamp}{file_extension}"
    contents = await file.read()
    file_path = f"uploads/{formatted_name}"

    with open(file_path, "wb") as f:
        f.write(contents)

    tune_data = TuneUpdate(name=name, code=code, file_name=formatted_name)
    updated_tune = crud.update_tune(db=db, id=tune_id, tune=tune_data)

    if not updated_tune:
        raise HTTPException(status_code=404, detail="Tune not found")
    
    return updated_tune