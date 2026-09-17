from __future__ import annotations

from app.domain import Employee
from app.services import (
    aggregate_metrics,
    assign_default_tasks,
    build_welcome_email,
)


class OnboardingSystem:
    """Coordinates onboarding automation steps."""

    def assign_tasks(self, employee: Employee):
        """Assign default onboarding tasks."""
        assign_default_tasks(employee)
        return employee.tasks

    def retrieve_documents(self, employee: Employee):
        """Return the list of required employee documents."""
        return list(employee.documents.keys())

    def send_welcome_email(self, employee: Employee) -> str:
        """Generate and mark the welcome email as sent."""
        email = build_welcome_email(employee)
        employee.welcome_email_sent = True
        return email

    def monitor_completion(self, employee: Employee) -> str:
        """Return an onboarding completion summary."""
        metrics = aggregate_metrics([employee])

        return (
            f"Overall completion is "
            f"{metrics['completion_rate'] * 100:.0f}% and "
            f"documents received average is "
            f"{metrics['documents_received'] * 100:.0f}%."
        )

    def collect_and_track(self, employee: Employee):
        """Run the complete onboarding workflow."""

        self.assign_tasks(employee)
        self.retrieve_documents(employee)

        email = self.send_welcome_email(employee)
        summary = self.monitor_completion(employee)

        return {
            "email": email,
            "summary": summary,
            "tasks": employee.tasks,
        }