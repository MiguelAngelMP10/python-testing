import unittest, os
from datetime import datetime
from unittest.mock import patch
from src.bank_account import BankAccount
from src.exceptions import WithdrawalTimeRestrictionError, InsufficientFundsError


class BankAccountTests(unittest.TestCase):

    def setUp(self) -> None:
        self.account = BankAccount(balance=1000, log_file="transaction_log.txt")

    def tearDown(self) -> None:
        if os.path.exists(self.account.log_file):
            os.remove(self.account.log_file)

    def _count_lines(self, filename):
        with open(filename, "r") as f:
            return len(f.readlines())

    def test_deposit(self):
        new_balance = self.account.deposit(500)
        self.assertEqual(new_balance, 1500, "El balance no es igual")

    @patch("src.bank_account.datetime")
    def test_withdraw(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0)  # Fecha ficticia con hora 10 AM
        new_balance = self.account.withdraw(200)
        self.assertEqual(new_balance, 800, "El balance no es igual")

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)

    @patch("src.bank_account.datetime")
    def test_success_transfer(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0)  # Fecha ficticia con hora 10 AM
        target = BankAccount(balance=500)
        self.account.transfer(200, target)
        self.assertEqual(self.account.get_balance(), 800)
        self.assertEqual(target.get_balance(), 700)

    def test_insufficient_funds_transfer(self):
        target = BankAccount(balance=500)
        with self.assertRaises(ValueError) as context:
            self.account.transfer(2000, target)
        self.assertEqual(str(context.exception), "No hay fondos suficientes")

    def test_transaction_log(self):
        self.account.deposit(500)
        self.assertTrue(os.path.exists("transaction_log.txt"))

    def test_count_transactions(self):
        assert self._count_lines(self.account.log_file) == 1
        self.account.deposit(500)
        self.assertEqual(self._count_lines(self.account.log_file), 2)

    @patch("src.bank_account.datetime")
    def test_withdraw_disallow_before_bussines_hours(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 7, 0)  # Fecha ficticia con hora 7 AM
        with self.assertRaises(WithdrawalTimeRestrictionError):
            self.account.withdraw(1000)

    @patch("src.bank_account.datetime")
    def test_withdraw_disallow_after_bussines_hours(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 18, 0)  # Fecha ficticia con hora 6 PM
        with self.assertRaises(WithdrawalTimeRestrictionError):
            self.account.withdraw(1000)

    def test_deposit_multiples_amounts(self):
        test_cases = [
            {"amount": 100, "expected": 1100},
            {"amount": 3000, "expected": 4000},
            {"amount": 4500, "expected": 5500},
        ]
        for case in test_cases:
            with self.subTest(case=case["amount"]):
                self.account = BankAccount(balance=1000, log_file="transaction_log.txt")
                new_balance = self.account.deposit(case["amount"])
                self.assertEqual(new_balance, case["expected"])

    def test_deposit_invalid_amount(self):
        new_balance = self.account.deposit(-500)
        self.assertEqual(new_balance, 1000, "El balance no debe cambiar con un monto negativo")

        new_balance = self.account.deposit(0)
        self.assertEqual(new_balance, 1000, "El balance no debe cambiar con un monto de cero")

    @patch("src.bank_account.datetime")
    def test_insufficient_funds(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0)  # Fecha ficticia con hora 10 AM

        # Intentar retirar más de lo que hay en la cuenta (por ejemplo, 1500)
        with self.assertRaises(InsufficientFundsError) as context:
            self.account.withdraw(10000)

        # Verificar que el mensaje de la excepción sea el esperado
        self.assertEqual(
            str(context.exception),
            "Withdrawal of 10000 exceeds balance 1000"
        )
