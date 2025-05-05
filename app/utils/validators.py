from builtins import bool, str
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email: str) -> bool:
    """
    Validate the email address using the email-validator library.
    
    Args:
        email (str): Email address to validate.
    
    Returns:
        bool: True if the email is valid, otherwise False.
    """
    try:
        # Validate and get info
        validate_email(email)
        return True
    except EmailNotValidError as e:
        # Email not valid, return False
        print(f"Invalid email: {e}")
        return False
    

import re

def validate_password(password: str) -> bool:
    if len(password) < 8:
        raise ValueError("Password too short")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Missing uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Missing lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Missing digit")
    if not re.search(r"[^\w\s]", password):
        raise ValueError("Missing special character")
    return True
