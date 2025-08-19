import pytest

from app.schemas.advertisement import CategorySchema
from app.schemas.login import LoginSchema

from app.tests.advertisement.mock_advertisement import CategoryFactory, SubCategoryFactory

pytest_plugins = ["pytest_asyncio"]
pytestmark = pytest.mark.asyncio


class TestCategory:
    base_url = "/api/v1/advertisements/category"

    async def test_create_category(self, client, test_db_session):
        data = {
            "name": "test",
        }
        res = await client.post(self.base_url, json=data)

        assert res.status_code == 201
        assert res.json().get("name") == "test"

    async def test_category_list(self, client):
        await CategoryFactory.create_batch_mock_data(size=5)
        response = await client.get(self.base_url)
        assert response.status_code == 200
        assert len(response.json()) == 5

    async def test_get_category(self, client):
        category = await CategoryFactory.create_mock_data()
        response = await client.get(self.base_url+f"/{category.id}")

        assert response.status_code == 200
        assert response.json().get("name") == category.name

    async def test_delete_category(self, client):
        category = await CategoryFactory.create_mock_data()
        response = await client.delete(self.base_url+f"/{category.id}")

        assert response.status_code == 204


class TestSubCategory:
    base_url = "/api/v1/advertisements/subcategory"

    async def test_create_subcategory(self, client, test_db_session):
        category = await CategoryFactory.create_mock_data()
        data = {
            "name": "test",
            "category_id": category.id
        }
        res = await client.post(self.base_url, json=data)
        print(res.json())
        assert res.status_code == 201
        assert res.json().get("name") == "test"

    async def test_subcategory_list(self, client):
        await SubCategoryFactory.create_batch_mock_data(size=5)
        response = await client.get(self.base_url)
        assert response.status_code == 200
        assert len(response.json()) == 5

    async def test_get_subcategory(self, client):
        subcategory = await SubCategoryFactory.create_mock_data()
        response = await client.get(self.base_url+f"/{subcategory.id}")

        assert response.status_code == 200
        assert response.json().get("name") == subcategory.name

    async def test_delete_subcategory(self, client):
        subcategory = await SubCategoryFactory.create_mock_data()
        response = await client.delete(self.base_url+f"/{subcategory.id}")

        assert response.status_code == 204

