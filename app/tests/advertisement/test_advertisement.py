import faker
import pytest
from starlette import status

from app.tests.advertisement.mock_advertisement import (
    AdvertisementFactory,
    CategoryFactory,
    SubCategoryFactory,
)
from app.tests.user.mock_user import UserFactory

pytest_plugins = ["pytest_asyncio"]
pytestmark = pytest.mark.asyncio


class TestCategory:
    base_url = "/api/v1/advertisements/category"

    async def test_create_category(self, client):
        data = {
            "name": "test",
        }
        res = await client.post(self.base_url, json=data)

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json().get("name") == "test"

    async def test_category_list(self, client):
        await CategoryFactory.create_batch_mock_data(size=5)
        response = await client.get(self.base_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 5

    async def test_get_category(self, client):
        category = await CategoryFactory.create_mock_data()
        response = await client.get(self.base_url + f"/{category.id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("name") == category.name

    async def test_delete_category(self, client):
        category = await CategoryFactory.create_mock_data()
        response = await client.delete(self.base_url + f"/{category.id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestSubCategory:
    base_url = "/api/v1/advertisements/subcategory"

    async def test_create_subcategory(self, client):
        category = await CategoryFactory.create_mock_data()
        data = {"name": "test", "category_id": category.id}
        res = await client.post(self.base_url, json=data)
        print(res.json())
        assert res.status_code == status.HTTP_201_CREATED
        assert res.json().get("name") == "test"

    async def test_subcategory_list(self, client):
        await SubCategoryFactory.create_batch_mock_data(size=5)
        response = await client.get(self.base_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 5

    async def test_get_subcategory(self, client):
        subcategory = await SubCategoryFactory.create_mock_data()
        response = await client.get(self.base_url + f"/{subcategory.id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("name") == subcategory.name

    async def test_delete_subcategory(self, client):
        subcategory = await SubCategoryFactory.create_mock_data()
        response = await client.delete(self.base_url + f"/{subcategory.id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestAdvertisement:
    base_url = "/api/v1/advertisements/"

    async def test_create_ad(self, client):
        user = await UserFactory.create_mock_data()
        subcategory = await SubCategoryFactory.create_mock_data()
        mock_ad_data = {
            "user_id": user.id,
            "sub_category_id": subcategory.id,
            "location": faker.Faker().address(),
            "price": faker.Faker().random_int(),
            "active": True,
            "negotiable": faker.Faker().boolean(),
            "description": faker.Faker().text(),
        }
        res = await client.post(self.base_url, json=mock_ad_data)
        assert res.status_code == status.HTTP_201_CREATED

    async def test_get_ads(self, client):
        await AdvertisementFactory.create_batch_mock_data(size=5)
        response = await client.get(self.base_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 5

    async def test_get_ad(self, client):
        ad = await AdvertisementFactory.create_mock_data()
        response = await client.get(self.base_url + f"{ad.id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("id") == ad.id
        assert response.json().get("description") == ad.description

    async def test_update_ad(self, client):
        ad = await AdvertisementFactory.create_mock_data()
        data = {"description": faker.Faker().text()}
        response = await client.patch(self.base_url + f"{ad.id}", json=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("description") == data.get("description")
        assert response.json().get("description") != ad.description
