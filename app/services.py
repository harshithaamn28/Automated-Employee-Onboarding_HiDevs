from __future__ import annotations

from collections.abc import Iterable
from datetime import date, timedelta

from .domain import Employee, OnboardingTask, TaskStatus


# ---------------------------------------------------------
# Default onboarding tasks
# ---------------------------------------------------------

TASK_TEMPLATES = [
    ("Review employee handbook", "HR", "People"),
    ("Complete security training", "IT", "Compliance"),
    ("Meet your manager", "Manager", "People"),
    ("Set up development environment", "IT", "Tools"),
    ("Submit payroll information", "HR", "Payroll"),
]


# ---------------------------------------------------------
# Required employee documents
# ---------------------------------------------------------

DOCUMENT_TYPES = [
    "Government ID",
    "Tax form",
    "Bank details",
    "Signed offer",
]


# ---------------------------------------------------------
# Assign default onboarding tasks
# ---------------------------------------------------------

def assign_default_tasks(
    employee: Employee,
    today: date | None = None,
) -> list[OnboardingTask]:
    """Assign the standard onboarding tasks and documents."""

    start_date = today or date.today()

    employee.tasks = [
        OnboardingTask(
            id=f"{employee.id}-task-{index}",
            title=title,
            owner=owner,
            due_date=start_date + timedelta(days=index + 1),
            category=category,
        )
        for index, (title, owner, category)
        in enumerate(TASK_TEMPLATES, start=1)
    ]

    employee.documents = {
        document: False
        for document in DOCUMENT_TYPES
    }

    return employee.tasks


# ---------------------------------------------------------
# Update task status
# ---------------------------------------------------------

def update_task_status(
    employee: Employee,
    task_id: str,
    status: TaskStatus,
) -> bool:
    """Update the status of a specific onboarding task."""

    for task in employee.tasks:
        if task.id == task_id:
            task.status = status
            return True

    return False


# ---------------------------------------------------------
# Document collection
# ---------------------------------------------------------

def mark_document_received(
    employee: Employee,
    document_type: str,
    received: bool = True,
) -> None:
    """Mark an employee document as received or missing."""

    if document_type not in employee.documents:
        raise ValueError(
            f"Unknown document type: {document_type}"
        )

    employee.documents[document_type] = received


# ---------------------------------------------------------
# Welcome email generation
# ---------------------------------------------------------

def build_welcome_email(employee: Employee) -> str:
    """Generate a personalized employee welcome email."""

    first_name = employee.name.split()[0]

    return (
        f"Subject: Welcome to the team, {employee.name}!\n\n"
        f"Hi {first_name},\n\n"
        f"We are excited to welcome you to {employee.department} "
        f"as our new {employee.role}.\n\n"
        f"Your first day is "
        f"{employee.start_date:%B %-d, %Y}.\n\n"
        "Your onboarding checklist is ready in the employee portal.\n\n"
        "Please complete the required tasks and submit the "
        "necessary documents before your start date.\n\n"
        "See you soon,\n"
        "People Operations"
    )


# ---------------------------------------------------------
# Employee Query Assistant
# ---------------------------------------------------------

def answer_employee_query(
    employee: Employee,
    question: str,
) -> str:
    """Answer basic employee onboarding questions."""

    normalized = question.strip().lower()

    pending_tasks = [
        task.title
        for task in employee.tasks
        if task.status != TaskStatus.COMPLETE
    ]

    missing_documents = [
        name
        for name, received in employee.documents.items()
        if not received
    ]

    # Task-related questions
    if any(
        word in normalized
        for word in (
            "task",
            "tasks",
            "checklist",
            "todo",
            "to-do",
            "pending",
        )
    ):
        if not pending_tasks:
            return "You have completed every onboarding task."

        return (
            "Your remaining tasks are: "
            + "; ".join(pending_tasks)
            + "."
        )

    # Document-related questions
    if any(
        word in normalized
        for word in (
            "document",
            "documents",
            "paperwork",
            "upload",
            "id",
            "tax",
            "bank",
            "offer",
        )
    ):
        if not missing_documents:
            return "All required documents have been received."

        return (
            "The following documents are still needed: "
            + ", ".join(missing_documents)
            + "."
        )

    # Start-date questions
    if any(
        phrase in normalized
        for phrase in (
            "start",
            "start date",
            "first day",
            "begin",
            "joining",
        )
    ):
        return (
            f"Your start date is "
            f"{employee.start_date:%B %-d, %Y}."
        )

    # Completion questions
    if any(
        phrase in normalized
        for phrase in (
            "progress",
            "completion",
            "complete",
            "status",
        )
    ):
        return (
            f"Your onboarding completion rate is "
            f"{employee.completion_rate * 100:.0f}%. "
            f"Your current status is "
            f"{employee.onboarding_status}."
        )

    return (
        "I can help with your onboarding tasks, "
        "required documents, start date, or progress."
    )


# ---------------------------------------------------------
# Team Metrics
# ---------------------------------------------------------

def aggregate_metrics(
    employees: Iterable[Employee],
) -> dict[str, float]:
    """Calculate onboarding metrics for a group of employees."""

    employee_list = list(employees)

    if not employee_list:
        return {
            "completion_rate": 0.0,
            "average_onboarding_days": 0.0,
            "documents_received": 0.0,
        }

    completion_rate = (
        sum(
            employee.completion_rate
            for employee in employee_list
        )
        / len(employee_list)
    )

    document_rates = []

    for employee in employee_list:
        if employee.documents:
            received = sum(
                employee.documents.values()
            )

            total = len(employee.documents)

            document_rates.append(
                received / total
            )
        else:
            document_rates.append(0.0)

    documents_received = (
        sum(document_rates)
        / len(document_rates)
    )

    onboarding_days = (
        sum(
            max(
                (date.today() - employee.start_date).days,
                0,
            )
            for employee in employee_list
        )
        / len(employee_list)
    )

    return {
        "completion_rate": completion_rate,
        "average_onboarding_days": float(onboarding_days),
        "documents_received": documents_received,
    }