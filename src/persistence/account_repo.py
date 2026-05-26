import os
import pandas as pd


class AccountRepository:
    _FILE_PATH = "data/accounts.csv"

    def __init__(self):
        """
        Initialize CSV database for accounts.
        """
        if not os.path.exists(self._FILE_PATH):
            os.makedirs(os.path.dirname(self._FILE_PATH), exist_ok=True)

            db = pd.DataFrame({
                "account_id": pd.Series(dtype="int64"),
                "balance": pd.Series(dtype="float64"),
            })

            db.to_csv(self._FILE_PATH, index=False)
            print("Account table created successfully!")

        self._db = pd.read_csv(self._FILE_PATH)

        if self._db.empty:
            self._db = pd.DataFrame({
                "account_id": pd.Series(dtype="int64"),
                "balance": pd.Series(dtype="float64"),
            })

        else:
            self._db = self._db.astype({"account_id": "int64", "balance": "float64"})

    def _save(self) -> None:
        """
        Persist data to CSV.
        """
        self._db.to_csv(self._FILE_PATH, index=False)

    def account_exists(self, account_id: int) -> bool:
        """
        Check whether an account exists.
        """
        return (self._db["account_id"] == account_id).any()

    def create_account(self, account_id: int) -> bool:
        """
        Create a new account.
        """
        if self.account_exists(account_id):
            return False

        new_account = pd.DataFrame([{"account_id": account_id, "balance": 0.0,}])
        self._db = pd.concat([self._db, new_account], ignore_index=True)
        self._save()

        return True

    def get_balance(self, account_id: int) -> float | None:
        """
        Return account balance.
        """
        balance = self._db.loc[self._db["account_id"] == account_id, "balance"].values
        if len(balance) == 0:
            return None
        return float(balance[0])

    def deposit(self, account_id: int, amount: float) -> bool:
        """
        Deposit money into account.
        """
        if not self.account_exists(account_id):
            return False

        self._db.loc[self._db["account_id"] == account_id, "balance"] += amount
        self._save()

        return True

    def withdrawal(self, account_id: int, amount: float) -> bool:
        """
        Withdraw money from account.
        """
        if not self.account_exists(account_id):
            return False

        self._db.loc[self._db["account_id"] == account_id, "balance"] -= amount
        self._save()

        return True

    def get_account_type(self, id: int) -> str | None:
        """
        Returns the type of an account.
        """
        account_type = self._db.loc[self._db["account_id"] == id, "account_type"].values
        if len(account_type) > 0:
            return str(account_type[0])
        return None

    def apply_interest_to_savings_accounts(self, interest_rate: float) -> int:
        """
        Applies an interest rate to every savings account and returns how many were updated.
        """
        savings_accounts = self._db["account_type"] == SAVINGS_ACCOUNT_TYPE
        updated_accounts = int(savings_accounts.sum())

        if updated_accounts == 0:
            return 0

        multiplier = 1 + (interest_rate / 100)
        self._db.loc[savings_accounts, "balance"] *= multiplier
        self._db.to_csv(self.FILE_PATH, index=False)

        return updated_accounts

    def get_points(self, id: int) -> int | None:
        """
        Returns the points of an account.
        """
        points = self._db.loc[self._db["account_id"] == id, "points"].values
        if len(points) > 0:
            return int(points[0])
        return None

    def add_points(self, id: int, points: int) -> bool:
        """
        Adds points to an account.
        """
        if not self.account_exists(id):
            return False

        self._db.loc[self._db["account_id"] == id, "points"] += points
        self._db.to_csv(self.FILE_PATH, index=False)
        return True
