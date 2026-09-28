"""
context_engine.py

Responsibilities:
- Analyze enterprise work data
- Build a work context summary
- Count items that matter to Byte

This module should not:
- Modify pet health
- Update pet state
- Call AI
- Display UI
"""

from datetime import datetime


class ContextEngine:
    def build_context(self, data: dict) -> dict:
        """
        Convert raw data into work context.

        Parameters:
            data (dict): DataFrames loaded by DataLoader

        Returns:
            dict: Current workplace context
        """

        messages_df = data["messages"]
        emails_df = data["emails"]
        tasks_df = data["tasks"]
        meetings_df = data["meetings"]
        manager_requests_df = data["manager_requests"]
        timesheets_df = data["timesheets"]

        unread_messages = len(
            messages_df[
                messages_df["status"].str.lower() == "unread"
            ]
        )

        unanswered_emails = len(
            emails_df[
                (emails_df["status"].str.lower() == "unread")
                &
                (emails_df["requires_response"].str.lower() == "yes")
            ]
        )

        open_tasks = len(
            tasks_df[
                tasks_df["status"].str.lower() == "open"
            ]
        )

        overdue_tasks = self._count_overdue_tasks(tasks_df)

        open_manager_requests = len(
            manager_requests_df[
                manager_requests_df["status"].str.lower() == "open"
            ]
        )

        meetings_today = len(meetings_df)

        timesheet_submitted = self._timesheet_submitted(
            timesheets_df
        )

        return {
            "unread_messages": unread_messages,
            "unanswered_emails": unanswered_emails,
            "open_tasks": open_tasks,
            "overdue_tasks": overdue_tasks,
            "pending_manager_requests": open_manager_requests,
            "meetings_today": meetings_today,
            "timesheet_submitted": timesheet_submitted,
            "generated_at": datetime.now().isoformat()
        }

    def _count_overdue_tasks(self, tasks_df) -> int:
        """
        Count tasks whose due date has passed.
        """

        today = datetime.now().date()

        overdue_count = 0

        for _, row in tasks_df.iterrows():

            try:
                due_date = datetime.strptime(
                    str(row["due_date"]),
                    "%Y-%m-%d"
                ).date()

                if (
                    due_date < today
                    and str(row["status"]).lower() == "open"
                ):
                    overdue_count += 1

            except Exception:
                continue

        return overdue_count

    def _timesheet_submitted(self, timesheet_df) -> bool:
        """
        Determine whether a timesheet is submitted.
        """

        if len(timesheet_df) == 0:
            return False

        latest_status = str(
            timesheet_df.iloc[0]["status"]
        ).lower()

        return latest_status == "submitted"