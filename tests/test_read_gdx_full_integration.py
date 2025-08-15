import pytest

def test_read_gdx_full_skip_if_no_gams():
    pytest.skip("Integration test runs only when GAMS is installed.")
