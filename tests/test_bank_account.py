import unittest, os

from src.bank_account import BankAccount


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

    def test_withdraw(self):
        new_balance = self.account.withdraw(200)
        self.assertEqual(new_balance, 800, "El balance no es igual")

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)

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

    def test_transaction_log(self):
        self.account.deposit(500)
        self.assertTrue(os.path.exists("transaction_log.txt"))

    def test_count_transactions(self):
        assert self._count_lines(self.account.log_file) == 1
        self.account.deposit(500)
        self.assertEqual(self._count_lines(self.account.log_file), 2)
