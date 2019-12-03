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

def test_total():
    tax_calculator = TaxCalculator(tva=.1)
    bill = Bill(tax_calculator=tax_calculator)
    bill.add(100.0)
    expected_total = bill.amount * 1.1

    total = bill.total

    assert total == expected_total, f"Total was {total}, but it should be {expected_total}"