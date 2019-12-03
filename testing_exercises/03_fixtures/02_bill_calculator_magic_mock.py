class TaxCalculator:
    def __init__(self, tva: float = .21):
        self.tva = tva

    def add_taxes(self, amount: float) -> float:
        return amount * (1 + self.tva)

class Bill:
    def __init__(self, tax_calculator: "TaxCalculator"):
        self.tax_calculator = tax_calculator
        self.amount: float = 0.

    def add(self, amount: float):
        self.amount += amount

    @property
    def total(self) -> float:
        """Calculates the total amount, including taxes"""
        return self.tax_calculator.add_taxes(self.amount)

import pytest
from unittest import mock

def test_total():
    tax_calculator = mock.MagicMock()
    bill = Bill(tax_calculator=tax_calculator)
    amount_to_add = 100.0
    amount_after_taxes = 110.0
    bill.add(amount_to_add)
    tax_calculator.add_taxes.return_value = amount_after_taxes

    total = bill.total

    assert total == amount_after_taxes, f"Total was {total}, but it should be {expected_total}"
    tax_calculator.add_taxes.assert_called_once_with(amount_to_add)