import pytest
import os

from app.fred import to_usd, func

CI_ENV = os.getenv("CI") == "true"

@pytest.mark.skipif(CI_ENV == True, reason="to avoid issuing HTTP requests on the CI server")
def test_func():
    # with valid state_id
    results = func(state_id="CA")
    assert results[1] == "Positive"
    assert results[0] == "$749,900"

    # with invalid state_id, fails gracefully and returns nothing:
    invalid_results = func(state_id="CAS")
    assert invalid_results == None

def test_to_usd():
    assert to_usd("219999") == "$219,999"
