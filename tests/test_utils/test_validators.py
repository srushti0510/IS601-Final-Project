import pytest
import app.utils.validators as validators

def test_validate_email_success():
    assert validators.validate_email("test@gmail.com")  # Avoid example.com

def test_validate_email_failure():
    with pytest.raises(ValueError):
        validators.validate_email("not-an-email")

def test_validate_password_success():
    assert validators.validate_password("StrongP@ssword1")

def test_validate_password_failure():
    with pytest.raises(ValueError):
        validators.validate_password("weakpass")
