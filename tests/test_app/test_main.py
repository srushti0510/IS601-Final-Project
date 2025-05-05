from app.main import app
from fastapi.testclient import TestClient

def test_main_app_startup():
    client = TestClient(app)
    response = client.get("/")
    # Depending on your actual root endpoint setup
    assert response.status_code in [200, 404]  # Acceptable if root path isn’t defined
