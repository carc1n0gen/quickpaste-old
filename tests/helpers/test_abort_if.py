import pytest
from app.helpers import abort_if


def test_should_not_abort_when_condition_is_falsy():
    try:
        abort_if(False, 404)
    except Exception:
        pytest.fail('Should not have errored.')


def test_should_abort_when_condition_is_truthy():
    try:
        abort_if(True, 404)
        pytest.fail('Should have errored.')
    except Exception:
        pass
