from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .schemas import ItemSchema
from .models import ItemModel


class ItemCrud:
    @classmethod
    def create_item(cls, item:ItemSchema.NeedCreate, db:Session) -> ItemSchema.All:
        db_item = ItemModel(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @classmethod
    def _create_items(cls, items:list[ItemSchema.NeedCreate], db:Session) -> list[ItemSchema.All]:
        db_items = [ItemModel(**item.model_dump()) for item in items]
        db.add_all(db_items)
        db.commit()
        [db.refresh(db_item) for db_item in db_items]
        return db_items

    @classmethod
    def read_item(cls, item_id:int, db:Session) -> ItemSchema.All:
        return cls._get_exist_item(item_id, db)

    @classmethod
    def read_items(cls, skip:int, limit:int, db:Session) -> list[ItemSchema.All]:
        return db.query(ItemModel).offset(skip).limit(limit).all()

    @classmethod
    def update_item_title(cls, item_id:int, new_title:str, db:Session) -> ItemSchema.All:
        item = cls._get_exist_item(item_id, db)
        item.title = new_title
        db.commit()
        return item

    @classmethod
    def delete_item(cls, item_id:int, db:Session) -> ItemSchema.All:
        item = cls._get_exist_item(item_id, db)
        db.delete(item)
        db.commit()
        return item
    
    @staticmethod
    def _get_exist_item(item_id:int, db:Session):
        item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item not found. ({item_id=})")
        return item
