import pytest
from httpx import AsyncClient
from fastapi import status
from io import BytesIO
from PIL import Image
from unittest.mock import AsyncMock, patch
from app.main import app
from app.dependencies import get_settings
from app.models.user_model import User

settings = get_settings()

def create_test_image(color="blue", size=(100, 100)) -> BytesIO:
    img = Image.new("RGB", size, color=color)
    img_bytes = BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    return img_bytes

@patch("app.routers.user_routes.UserService.update_user_profile_picture", new_callable=AsyncMock)
@patch("app.routers.user_routes.upload_profile_picture", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_upload_valid_jpeg(mock_upload, mock_update_user, client_with_token, user):
    mock_upload.return_value = "http://mocked-minio/test-user.jpg"
    user.profile_picture_url = "http://mocked-minio/test-user.jpg"
    mock_update_user.return_value = user
    token, user_id = client_with_token
    image_data = create_test_image()
    files = {"file": ("test.jpg", image_data, "image/jpeg")}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/users/{user_id}/upload-profile-picture",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["profile_picture_url"] == "http://mocked-minio/test-user.jpg"

@patch("app.routers.user_routes.UserService.update_user_profile_picture", new_callable=AsyncMock)
@patch("app.routers.user_routes.upload_profile_picture", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_upload_valid_png(mock_upload, mock_update_user, client_with_token, user):
    mock_upload.return_value = "http://mocked-minio/test-user.jpg"
    user.profile_picture_url = "http://mocked-minio/test-user.jpg"
    mock_update_user.return_value = user
    token, user_id = client_with_token

    img = Image.new("RGBA", (100, 100), color=(255, 0, 0, 128))
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    files = {"file": ("test.png", img_bytes, "image/png")}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/users/{user_id}/upload-profile-picture",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["profile_picture_url"] == "http://mocked-minio/test-user.jpg"

@pytest.mark.asyncio
async def test_upload_invalid_file_type(client_with_token, user):
    token, user_id = client_with_token
    fake_file = BytesIO(b"not-an-image")
    fake_file.seek(0)
    files = {"file": ("notanimage.txt", fake_file, "text/plain")}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/users/{user_id}/upload-profile-picture",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid file type" in response.text

@pytest.mark.asyncio
async def test_unauthorized_upload_attempt(async_client):
    files = {"file": ("test.jpg", BytesIO(b"fakejpegdata"), "image/jpeg")}

    response = await async_client.post(
        "/users/some-id/upload-profile-picture",
        files=files
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Not authenticated" in response.json().get("detail", "")

@patch("app.routers.user_routes.UserService.update_user_profile_picture")
@patch("app.routers.user_routes.upload_profile_picture")
@pytest.mark.asyncio
async def test_upload_valid_jpeg_with_async_client(mock_upload, mock_update, async_client, user, user_token):
    mock_url = "http://mocked-minio/test-user.jpg"
    mock_upload.return_value = mock_url
    user.profile_picture_url = mock_url
    mock_update.return_value = user

    image_data = create_test_image()
    files = {"file": ("test.jpg", image_data, "image/jpeg")}

    response = await async_client.post(
        f"/users/{user.id}/upload-profile-picture",
        files=files,
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["profile_picture_url"] == mock_url
    mock_upload.assert_called_once()
    mock_update.assert_called_once()
