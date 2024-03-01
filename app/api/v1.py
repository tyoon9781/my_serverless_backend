from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.crud import ItemCrud
from app.database.schemas import ItemSchema
from app.database.connection import get_db

router = APIRouter()


@router.get("/")
async def health_check():
    return {"status": "ok"}

@router.post("/items", response_model=ItemSchema.All)
async def create_item(item:ItemSchema.NeedCreate, db:Session=Depends(get_db)):
    return ItemCrud.create_item(item, db)

@router.get("/items/{item_id}", response_model=ItemSchema.All)
async def read_item(item_id:int, db:Session=Depends(get_db)):
    return ItemCrud.read_item(item_id, db)

@router.get("/items", response_model=list[ItemSchema.All])
async def read_items(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    if not (isinstance(skip, int) and isinstance(limit, int) and skip >= 0 and limit >= 0):
        raise HTTPException(status_code=422, detail=f"parameters invalid. ({skip=}, {limit=})")
    return ItemCrud.read_items(skip, limit, db)

@router.put("/items/{item_id}", response_model=ItemSchema.All)
async def update_item_title(item_id:int, new_title:str, db:Session=Depends(get_db)):
    if len(new_title) == 0:
        raise HTTPException(status_code=422, detail="new title empty")
    return ItemCrud.update_item_title(item_id, new_title, db)

@router.delete("/items/{item_id}", response_model=ItemSchema.All)
async def delete_item(item_id:int, db:Session=Depends(get_db)):
    return ItemCrud.delete_item(item_id, db)