"""
data_loader.py

Responsibilities:
- Load enterprise mock data from CSV files
- Return pandas DataFrames
- Provide a single access point for data

This module should NOT contain business logic.
"""

from pathlib import Path
import pandas as pd


class DataLoader:
    def __init__(self, data_directory: str = "Data"):
        self.data_dir = Path(data_directory)

    def load_messages(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "messages.csv")

    def load_emails(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "emails.csv")

    def load_tasks(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "tasks.csv")

    def load_meetings(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "meetings.csv")

    def load_manager_requests(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "manager_requests.csv")

    def load_timesheets(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "timesheets.csv")

    def load_all(self) -> dict:
        """
        Load all enterprise datasets.

        Returns:
            dict containing all DataFrames
        """

        return {
            "messages": self.load_messages(),
            "emails": self.load_emails(),
            "tasks": self.load_tasks(),
            "meetings": self.load_meetings(),
            "manager_requests": self.load_manager_requests(),
            "timesheets": self.load_timesheets(),
        }