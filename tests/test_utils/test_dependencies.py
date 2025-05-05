from app.dependencies import get_settings

def test_get_settings_equivalence():
    s1 = get_settings()
    s2 = get_settings()
    assert s1 == s2  # Value-based comparison, not memory reference