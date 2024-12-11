import unittest

from src.bank_account import BankAccount


class BankAccountTests(unittest.TestCase):

    def setUp(self) -> None:
        self.account = BankAccount(balance=1000)

    def test_deposit(self):
        new_balance = self.account.deposit(500)
        assert new_balance == 1500

    def test_withdraw(self):
        new_balance = self.account.withdraw(200)
        assert new_balance == 800

    def test_get_balance(self):
        assert self.account.get_balance() == 1000

    def test_success_transfer(self):
        target = BankAccount(balance=500)
        self.account.transfer(200, target)
        self.assertEqual(self.account.get_balance(), 800)
        self.assertEqual(target.get_balance(), 700)

    def test_insufficient_funds_transfer(self):
        target = BankAccount(balance=500)
        with self.assertRaises(ValueError) as context:
            self.account.transfer(2000, target)
        self.assertEqual(str(context.exception), "No hay fondos suficientes")
