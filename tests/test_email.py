import pytest
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager

    
@pytest.mark.asyncio
async def test_send_markdown_email(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    await email_service.send_user_email(user_data, 'email_verification')
    # Manual verification in Mailtrap

def test_send_markdown_email_success(email_service):
    to_email = "recipient@example.com"
    subject = "Test Email"
    markdown_content = "# Hello\nThis is a **test** email."

    try:
        email_service.send_markdown_email(to_email, subject, markdown_content)
    except Exception as e:
        assert False, f"Email sending failed with exception: {e}"

def test_send_markdown_email_invalid_recipient(email_service):
    invalid_email = "invalid-email"  # Missing domain, '@', etc.
    subject = "Test Invalid Email"
    markdown_content = "# Hello\nThis should fail."

    try:
        email_service.send_markdown_email(invalid_email, subject, markdown_content)
        assert False, "Expected an error due to invalid email format"
    except Exception:
        pass  # Expected path

@pytest.mark.asyncio
async def test_send_markdown_email_invalid_recipient(email_service):
    invalid_email = "not-an-email"
    subject = "Test Email"
    markdown_content = "### Invalid recipient test"

    with pytest.raises(Exception, match="Invalid recipient"):
        await email_service.send_markdown_email(invalid_email, subject, markdown_content)
