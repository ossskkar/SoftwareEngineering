import pytest
from unittest import mock

@pytest.fixture
def tax_calculator():
    print("\nInstantiating tax_calculator fixture\n")
    tax_calculator = mock.MagicMock()

    return tax_calculator

def test_total(tax_calculator):
    assert True

def test_total_200(tax_calculator):
    assert True