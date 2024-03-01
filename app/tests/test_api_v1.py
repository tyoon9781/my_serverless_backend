import unittest
from fastapi.testclient import TestClient
from app.database.crud import ItemCrud
from app.database.schemas import ItemSchema
from app.database.models import ItemModel
from fastapi import status
from app.database.connection import Base, local_engine, get_db
import main_app

import json

## ignore httpx deprecated warning
import warnings
from httpx import _transports
warnings.filterwarnings("ignore", category=DeprecationWarning, module=_transports.__name__)


class DummyItem:
    title = "Test Item"
    description = "This is a test item"

    @classmethod
    def get_title(cls, number=None):
        return f"{cls.title}" if number is None else f"{number}_{cls.title}"
    
    @classmethod
    def get_description(cls, number=None):
        return f"{cls.description}" if number is None else f"{number}_{cls.description}"
    
    @classmethod
    def to_dict(cls, number=None):
        return {"title": cls.get_title(number), "description": cls.get_description(number)}

    @classmethod
    def dump_json(cls, number=None):
        return json.dumps(cls.to_dict(number))
    

class TestCaseV1(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=local_engine)
        self.client = TestClient(main_app.app_instance, base_url="http://localhost:8881/api/v1")

    def tearDown(self):
        ## delete table data
        session = next(get_db())
        session.query(ItemModel).delete()
        session.commit()

    def test_health_check(self):
        ## health check
        response = self.client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok"}

    def test_create_item(self):
        ## create api check
        response = self.client.post("/items", json=DummyItem.to_dict())
        assert response.status_code == status.HTTP_200_OK

        ## item exist check
        item_id = response.json()["id"]
        db_item = ItemCrud.read_item(item_id, next(get_db()))
        assert db_item.title == DummyItem.title
        assert db_item.description == DummyItem.description

    def test_read_item(self):
        ## read not exist item
        response = self.client.get("/items/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        ## create and read
        db_item = ItemCrud.create_item(ItemSchema.NeedCreate(**DummyItem.to_dict()), next(get_db()))
        response = self.client.get(f"/items/{db_item.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == DummyItem.title

    def test_read_items(self):
        ## parameter
        CREATE_ITEMS = 1000
        SKIP = 100
        LIMIT = 200
        assert CREATE_ITEMS - SKIP > LIMIT

        ## read empty table
        response = self.client.get("/items")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

        ## create items and read from skip to limit
        items = [ItemSchema.NeedCreate(**DummyItem.to_dict(i)) for i in range(CREATE_ITEMS)]
        db_items = ItemCrud._create_items(items, next(get_db()))
        response = self.client.get("/items", params={"skip": SKIP, "limit": LIMIT})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["title"] == db_items[SKIP].title
        assert response.json()[-1]["title"] == db_items[SKIP + LIMIT - 1].title
        
        ## read table default
        response = self.client.get("/items")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 100  ## default limit

        ## wrong skip and limit
        response = self.client.get("/items", params={"skip": 2, "limit": "a"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_item_title(self):
        ## create and update no title
        db_item = ItemCrud.create_item(ItemSchema.NeedCreate(**DummyItem.to_dict()), next(get_db()))
        response = self.client.put(f"/items/{db_item.id}", params={"new_title": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        ## update title
        new_title = "New Title"
        response = self.client.put(f"/items/{db_item.id}", params={"new_title": new_title})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == new_title
        
    def test_delete_item(self):
        ## delete not exist item
        response = self.client.delete("/items/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        ## delete exist item
        db_item = ItemCrud.create_item(ItemSchema.NeedCreate(**DummyItem.to_dict()), next(get_db()))
        response = self.client.delete(f"/items/{db_item.id}")
        assert response.status_code == status.HTTP_200_OK

        ## Verify item is deleted
        response = self.client.get(f"/items/{db_item.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND


if __name__ == "__main__":
    unittest.main()