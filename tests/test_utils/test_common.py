import app.utils.common as common

def test_format_message():
    message = common.format_message("Success", "User created")
    assert message["status"] == "Success"
    assert message["message"] == "User created"
    assert message["code"] == 200

def test_format_message_with_code():
    message = common.format_message("Error", "Invalid input", code=400)
    assert message["status"] == "Error"
    assert message["message"] == "Invalid input"
    assert message["code"] == 400

