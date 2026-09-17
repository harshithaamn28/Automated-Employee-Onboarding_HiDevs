from datetime import date

from app.domain import Employee, TaskStatus
from app.services import (
    aggregate_metrics,
    answer_employee_query,
    assign_default_tasks,
    mark_document_received,
)
from app.system import OnboardingSystem


def make_employee() -> Employee:
    employee = Employee(
        id="emp-1",
        name="Amina Okafor",
        role="Product Designer",
        department="Design",
        start_date=date.today(),
        email="amina@example.com",
    )
    assign_default_tasks(employee, today=date.today())
    return employee


def test_default_tasks_and_documents_are_created():
    employee = make_employee()
    assert len(employee.tasks) == 5
    assert employee.tasks[0].title == "Review employee handbook"
    assert employee.documents["Government ID"] is False


def test_query_reports_current_onboarding_state():
    employee = make_employee()
    employee.tasks[0].status = TaskStatus.COMPLETE
    mark_document_received(employee, "Government ID")
    response = answer_employee_query(employee, "What documents do I still need?")
    assert "Tax form" in response
    assert "Government ID" not in response


def test_metrics_calculate_completion_rate():
    employee = make_employee()
    employee.tasks[0].status = TaskStatus.COMPLETE
    metrics = aggregate_metrics([employee])
    assert metrics["completion_rate"] == 0.2
    assert metrics["documents_received"] == 0.0


def test_onboarding_system_tracks_tasks_documents_and_email():
    system = OnboardingSystem()
    employee = Employee(
        id="emp-2",
        name="Luis Park",
        role="Data Analyst",
        department="Analytics",
        start_date=date.today(),
        email="luis@example.com",
    )

    tasks = system.assign_tasks(employee)
    assert len(tasks) == 5
    assert system.retrieve_documents(employee) == ["Government ID", "Tax form", "Bank details", "Signed offer"]

    employee.tasks[0].status = TaskStatus.COMPLETE
    mark_document_received(employee, "Government ID")
    email = system.send_welcome_email(employee)

    assert "Welcome" in email
    assert employee.welcome_email_sent is True
    assert "completion" in system.monitor_completion(employee).lower()
