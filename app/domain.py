from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import StrEnum


class TaskStatus(StrEnum):
    """Status of an employee onboarding task."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


@dataclass
class OnboardingTask:
    """Represents one onboarding task."""

    id: str
    title: str
    owner: str
    due_date: date
    status: TaskStatus = TaskStatus.TODO
    category: str = "General"


@dataclass
class Employee:
    """Represents an employee going through onboarding."""

    id: str
    name: str
    role: str
    department: str
    start_date: date
    email: str

    tasks: list[OnboardingTask] = field(default_factory=list)

    documents: dict[str, bool] = field(default_factory=dict)

    welcome_email_sent: bool = False

    created_at: datetime = field(
        default_factory=datetime.now
    )

    @property
    def completion_rate(self) -> float:
        """Return the percentage of completed onboarding tasks."""

        if not self.tasks:
            return 0.0

        completed_tasks = sum(
            task.status == TaskStatus.COMPLETE
            for task in self.tasks
        )

        return completed_tasks / len(self.tasks)

    @property
    def onboarding_status(self) -> str:
        """Return the current onboarding status."""

        if self.completion_rate == 1.0:
            return "Complete"

        if self.completion_rate > 0.0:
            return "In progress"

        return "Not started"