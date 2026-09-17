from __future__ import annotations

from datetime import date, datetime

import streamlit as st

from app.domain import Employee, TaskStatus
from app.services import (
    aggregate_metrics,
    answer_employee_query,
    assign_default_tasks,
    build_welcome_email,
    mark_document_received,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PeopleHub | Employee Portal",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# EMPLOYEE / SESSION STATE
# ============================================================

if "employee" not in st.session_state:
    employee = Employee(
        id="EMP-1001",
        name="Jordan Lee",
        role="Software Engineer",
        department="Engineering",
        start_date=date.today(),
        email="jordan.lee@example.com",
    )

    assign_default_tasks(employee, today=date.today())

    # Realistic employee onboarding documents
    employee.documents = {
        "Offer Letter": True,
        "Government ID": True,
        "Tax Form": False,
        "Bank Details": False,
        "Address Proof": False,
        "Signed Employee Policies": False,
    }

    st.session_state.employee = employee


if "document_files" not in st.session_state:
    st.session_state.document_files = {
        "Offer Letter": "Jordan_Lee_Signed_Offer_Letter.pdf",
        "Government ID": "Jordan_Lee_Government_ID.pdf",
    }


if "document_dates" not in st.session_state:
    st.session_state.document_dates = {
        "Offer Letter": "16 Sep 2026",
        "Government ID": "16 Sep 2026",
    }


if "welcome_email_sent" not in st.session_state:
    st.session_state.welcome_email_sent = False


employee = st.session_state.employee


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
<style>

/* ----------------------------------------------------------
   MAIN PAGE
---------------------------------------------------------- */

.stApp {
    background-color: #f6f8fc;
    color: #172033;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* Force readable text */

.stApp p,
.stApp label,
.stApp span {
    color: #334155;
}

.stApp h1,
.stApp h2,
.stApp h3 {
    color: #0f172a;
}


/* ----------------------------------------------------------
   SIDEBAR
---------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background: #111827;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] .stButton button {
    background: transparent;
    border: 1px solid #273449;
    color: #f8fafc;
    text-align: left;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #1e293b;
    border-color: #3b82f6;
}


/* ----------------------------------------------------------
   BRAND
---------------------------------------------------------- */

.brand-logo {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    color: white !important;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 17px;
    font-weight: 900;
}

.brand-name {
    color: white !important;
    font-size: 22px;
    font-weight: 800;
    margin-top: 2px;
}

.brand-caption {
    color: #94a3b8 !important;
    font-size: 11px;
}


/* ----------------------------------------------------------
   EMPLOYEE AVATAR
---------------------------------------------------------- */

.employee-avatar {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, #dbeafe, #bfdbfe);
    color: #1d4ed8 !important;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 28px;
    font-weight: 900;
}


/* ----------------------------------------------------------
   METRIC CARDS
---------------------------------------------------------- */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
}

[data-testid="stMetricLabel"] p {
    color: #64748b !important;
}

[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 800;
}


/* ----------------------------------------------------------
   BORDER CONTAINERS
---------------------------------------------------------- */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff;
    border-color: #e2e8f0 !important;
    border-radius: 14px;
}


/* ----------------------------------------------------------
   BUTTONS
---------------------------------------------------------- */

.stButton button {
    border-radius: 9px;
    font-weight: 600;
}


/* ----------------------------------------------------------
   PROGRESS
---------------------------------------------------------- */

.stProgress > div > div > div > div {
    border-radius: 20px;
}


/* ----------------------------------------------------------
   FILE UPLOADER
---------------------------------------------------------- */

[data-testid="stFileUploader"] {
    background: #f8fafc;
    border-radius: 10px;
}


/* ----------------------------------------------------------
   CUSTOM TEXT
---------------------------------------------------------- */

.section-description {
    color: #64748b !important;
    font-size: 14px;
    margin-bottom: 15px;
}

.document-file {
    color: #475569 !important;
    font-size: 13px;
}

.document-date {
    color: #94a3b8 !important;
    font-size: 12px;
}

.action-title {
    color: #92400e !important;
    font-size: 18px;
    font-weight: 800;
}

.footer {
    text-align: center;
    color: #94a3b8 !important;
    font-size: 12px;
    padding-top: 15px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    logo_col, brand_col = st.columns([1, 3])

    with logo_col:
        st.markdown(
            '<div class="brand-logo">PH</div>',
            unsafe_allow_html=True,
        )

    with brand_col:
        st.markdown(
            '<div class="brand-name">PeopleHub</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="brand-caption">Employee Experience Platform</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    st.caption("EMPLOYEE PORTAL")

    st.button("Dashboard", use_container_width=True)
    st.button("My Onboarding", use_container_width=True)
    st.button("My Documents", use_container_width=True)
    st.button("My Tasks", use_container_width=True)
    st.button("Company Information", use_container_width=True)

    st.divider()

    st.caption("SUPPORT")

    st.button("Help Center", use_container_width=True)
    st.button("Contact HR", use_container_width=True)

    st.divider()

    st.caption("SIGNED IN AS")
    st.write(f"**{employee.name}**")
    st.caption(employee.email)

    st.write("")
    st.caption("PeopleHub v1.0")


# ============================================================
# CURRENT VALUES
# ============================================================

completed_tasks = sum(
    task.status == TaskStatus.COMPLETE
    for task in employee.tasks
)

total_tasks = len(employee.tasks)

received_documents = sum(employee.documents.values())

total_documents = len(employee.documents)

pending_document_names = [
    name
    for name, received in employee.documents.items()
    if not received
]

submitted_document_names = [
    name
    for name, received in employee.documents.items()
    if received
]

task_progress = (
    completed_tasks / total_tasks
    if total_tasks
    else 0
)

document_progress = (
    received_documents / total_documents
    if total_documents
    else 0
)

overall_progress = (
    (task_progress + document_progress) / 2
)


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.title(f"Welcome, {employee.name.split()[0]}")

    st.markdown(
        """
        <div class="section-description">
        Complete your onboarding activities and submit the required
        documents before your joining process is finalized.
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:

    st.write("")

    if st.button(
        "Contact HR",
        type="primary",
        use_container_width=True,
    ):
        st.info(
            "Your request has been recorded. "
            "People Operations will contact you."
        )


# ============================================================
# EMPLOYEE PROFILE
# ============================================================

with st.container(border=True):

    profile1, profile2, profile3, profile4 = st.columns(
        [0.8, 2.7, 1.6, 1.6]
    )

    with profile1:

        st.markdown(
            f'<div class="employee-avatar">'
            f'{employee.name[0].upper()}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with profile2:

        st.subheader(employee.name)

        st.write(
            f"**{employee.role}** · {employee.department}"
        )

        st.caption(
            f"Employee ID: {employee.id}"
        )

        st.caption(employee.email)

    with profile3:

        st.caption("START DATE")

        st.write(
            f"**{employee.start_date.strftime('%d %B %Y')}**"
        )

        st.caption("EMPLOYMENT TYPE")
        st.write("Full Time")

    with profile4:

        st.caption("ONBOARDING STATUS")

        if overall_progress >= 1:
            st.success("Completed")

        elif overall_progress > 0:
            st.info("In Progress")

        else:
            st.warning("Not Started")


# ============================================================
# OVERVIEW
# ============================================================

st.write("")
st.subheader("Onboarding Overview")

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(
        "Overall Progress",
        f"{overall_progress * 100:.0f}%",
    )

with metric2:

    st.metric(
        "Tasks Completed",
        f"{completed_tasks}/{total_tasks}",
    )

with metric3:

    st.metric(
        "Documents Submitted",
        f"{received_documents}/{total_documents}",
    )

with metric4:

    st.metric(
        "Documents Pending",
        len(pending_document_names),
    )

st.progress(overall_progress)

st.caption(
    f"{completed_tasks} of {total_tasks} tasks completed · "
    f"{received_documents} of {total_documents} documents submitted"
)


# ============================================================
# ACTION REQUIRED
# ============================================================

st.write("")

if pending_document_names:

    with st.container(border=True):

        st.markdown(
            '<div class="action-title">Action Required</div>',
            unsafe_allow_html=True,
        )

        st.write("")

        st.warning(
            f"You have {len(pending_document_names)} "
            f"document(s) still pending."
        )

        st.write(
            "Please submit the following documents "
            "to continue your onboarding:"
        )

        for document_name in pending_document_names:
            st.write(
                f"**{document_name}** — Not submitted"
            )

else:

    st.success(
        "All required employee documents have been submitted."
    )


# ============================================================
# DOCUMENT CENTER
# ============================================================

st.write("")
st.header("Document Center")

st.markdown(
    """
    <div class="section-description">
    Review your submitted documents and upload any documents
    that are still required by People Operations.
    </div>
    """,
    unsafe_allow_html=True,
)

submitted_col, pending_col = st.columns(2)


# ============================================================
# SUBMITTED DOCUMENTS
# ============================================================

with submitted_col:

    st.subheader("Submitted Documents")

    st.caption(
        f"{len(submitted_document_names)} document(s) received"
    )

    if submitted_document_names:

        for document_name in submitted_document_names:

            with st.container(border=True):

                title_col, status_col = st.columns(
                    [3, 1]
                )

                with title_col:

                    st.write(
                        f"**{document_name}**"
                    )

                with status_col:

                    st.success("Received")

                filename = (
                    st.session_state.document_files.get(
                        document_name,
                        "Submitted document",
                    )
                )

                submitted_date = (
                    st.session_state.document_dates.get(
                        document_name,
                        "Previously submitted",
                    )
                )

                st.markdown(
                    f'<div class="document-file">'
                    f'File name: <b>{filename}</b>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="document-date">'
                    f'Submitted on: {submitted_date}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                st.caption(
                    "Status: Submitted and available for HR verification"
                )

    else:

        st.info(
            "You have not submitted any documents yet."
        )


# ============================================================
# PENDING DOCUMENTS
# ============================================================

with pending_col:

    st.subheader("Pending Documents")

    st.caption(
        f"{len(pending_document_names)} document(s) still required"
    )

    document_details = {
        "Tax Form": (
            "Required for tax declarations and "
            "employee compliance records."
        ),
        "Bank Details": (
            "Required for salary credit and "
            "monthly payroll processing."
        ),
        "Address Proof": (
            "Required to verify your current "
            "residential address."
        ),
        "Signed Employee Policies": (
            "Acknowledgement of company policies, "
            "confidentiality and workplace guidelines."
        ),
        "Offer Letter": (
            "Signed copy of your employment offer."
        ),
        "Government ID": (
            "Government-issued identity document."
        ),
    }

    if pending_document_names:

        for document_name in pending_document_names:

            with st.container(border=True):

                title_col, status_col = st.columns(
                    [3, 1]
                )

                with title_col:

                    st.write(
                        f"**{document_name}**"
                    )

                with status_col:

                    st.warning("Pending")

                st.caption(
                    document_details.get(
                        document_name,
                        "Required employee onboarding document.",
                    )
                )

                uploaded_file = st.file_uploader(
                    f"Upload {document_name}",
                    type=[
                        "pdf",
                        "png",
                        "jpg",
                        "jpeg",
                        "docx",
                    ],
                    key=f"upload_{document_name}",
                )

                if uploaded_file is not None:

                    mark_document_received(
                        employee,
                        document_name,
                        True,
                    )

                    st.session_state.document_files[
                        document_name
                    ] = uploaded_file.name

                    st.session_state.document_dates[
                        document_name
                    ] = datetime.now().strftime(
                        "%d %b %Y"
                    )

                    st.success(
                        f"{uploaded_file.name} uploaded successfully."
                    )

                    st.rerun()

    else:

        st.success(
            "No pending documents. Your document checklist is complete."
        )


# ============================================================
# ONBOARDING TASKS
# ============================================================

st.write("")
st.header("Onboarding Tasks")

st.markdown(
    """
    <div class="section-description">
    Complete the activities assigned by HR, IT and your manager.
    </div>
    """,
    unsafe_allow_html=True,
)

task_descriptions = {
    "Review employee handbook":
        "Read the employee handbook and acknowledge company policies.",

    "Complete security training":
        "Complete mandatory information security and compliance training.",

    "Meet your manager":
        "Attend your introductory meeting with your reporting manager.",

    "Set up development environment":
        "Configure your laptop, employee accounts and development tools.",

    "Submit payroll information":
        "Provide the information required to activate salary processing.",
}


for index, task in enumerate(employee.tasks, start=1):

    with st.container(border=True):

        number_col, task_col, status_col = st.columns(
            [0.5, 4, 1.2]
        )

        with number_col:

            st.markdown(
                f"### {index:02}"
            )

        with task_col:

            checked = st.checkbox(
                task.title,
                value=(
                    task.status
                    == TaskStatus.COMPLETE
                ),
                key=f"task_{task.id}",
            )

            if checked:
                task.status = TaskStatus.COMPLETE
            else:
                task.status = TaskStatus.TODO

            st.caption(
                task_descriptions.get(
                    task.title,
                    "Complete this onboarding activity.",
                )
            )

            st.caption(
                f"Assigned to: {task.owner} · "
                f"Category: {task.category} · "
                f"Due: {task.due_date.strftime('%d %b %Y')}"
            )

        with status_col:

            if checked:
                st.success("Completed")
            else:
                st.warning("Pending")


# ============================================================
# WORKFLOW
# ============================================================

st.write("")
st.header("Onboarding Journey")

st.markdown(
    """
    <div class="section-description">
    Follow your progress from offer acceptance through your first week.
    </div>
    """,
    unsafe_allow_html=True,
)


if received_documents == total_documents:
    document_stage = "Completed"
else:
    document_stage = "In Progress"


workflow = [
    {
        "step": "01",
        "title": "Offer & Joining",
        "description": "Offer accepted and employee profile created.",
        "status": "Completed",
    },
    {
        "step": "02",
        "title": "Document Submission",
        "description": "Submit identity, tax, banking and employment documents.",
        "status": document_stage,
    },
    {
        "step": "03",
        "title": "HR Verification",
        "description": "People Operations verifies employee information.",
        "status": "Pending",
    },
    {
        "step": "04",
        "title": "IT & Account Setup",
        "description": "Laptop, company email and system access are prepared.",
        "status": "Pending",
    },
    {
        "step": "05",
        "title": "Orientation",
        "description": "Attend company induction and meet your manager.",
        "status": "Pending",
    },
    {
        "step": "06",
        "title": "First Week",
        "description": "Meet your team, understand goals and complete check-in.",
        "status": "Pending",
    },
]


workflow_cols = st.columns(3)

for index, stage in enumerate(workflow):

    with workflow_cols[index % 3]:

        with st.container(border=True):

            st.caption(
                f"STEP {stage['step']}"
            )

            st.subheader(
                stage["title"]
            )

            st.write(
                stage["description"]
            )

            if stage["status"] == "Completed":
                st.success("Completed")

            elif stage["status"] == "In Progress":
                st.info("In Progress")

            else:
                st.caption("Status: Not started")


# ============================================================
# HR VERIFICATION
# ============================================================

st.write("")
st.header("HR Verification")

st.caption(
    "Current verification status of your employee information."
)

verification1, verification2, verification3 = st.columns(3)


with verification1:

    with st.container(border=True):

        st.subheader("Identity Verification")

        st.write(
            "Government-issued identification"
        )

        if employee.documents.get(
            "Government ID",
            False,
        ):
            st.success("Document received")
        else:
            st.warning("Government ID required")


with verification2:

    with st.container(border=True):

        st.subheader("Payroll Setup")

        st.write(
            "Bank and tax information"
        )

        payroll_ready = (
            employee.documents.get(
                "Bank Details",
                False,
            )
            and
            employee.documents.get(
                "Tax Form",
                False,
            )
        )

        if payroll_ready:
            st.success("Information received")
        else:
            st.warning("Documents pending")


with verification3:

    with st.container(border=True):

        st.subheader("Policy Acceptance")

        st.write(
            "Company policies and acknowledgement"
        )

        if employee.documents.get(
            "Signed Employee Policies",
            False,
        ):
            st.success("Policies acknowledged")
        else:
            st.warning("Acknowledgement pending")


# ============================================================
# AI ASSISTANT
# ============================================================

st.write("")

with st.container(border=True):

    st.header("PeopleHub Assistant")

    st.write(
        "Need help with your onboarding? Ask about your "
        "documents, tasks or joining information."
    )

    question = st.text_input(
        "Ask a question",
        placeholder=(
            "For example: Which documents are still pending?"
        ),
    )

    if question:

        answer = answer_employee_query(
            employee,
            question,
        )

        st.info(answer)


# ============================================================
# WELCOME COMMUNICATION
# ============================================================

st.write("")
st.header("Welcome Communication")

st.caption(
    "Your personalized welcome message from People Operations."
)

with st.expander(
    "View welcome email",
    expanded=False,
):

    st.code(
        build_welcome_email(employee),
        language="text",
    )

    if not st.session_state.welcome_email_sent:

        if st.button(
            "Mark Welcome Email as Sent",
            type="primary",
        ):

            st.session_state.welcome_email_sent = True
            employee.welcome_email_sent = True
            st.rerun()

    else:

        st.success(
            f"Welcome email sent to {employee.email}"
        )


# ============================================================
# ANALYTICS
# ============================================================

st.write("")
st.header("Onboarding Status")

metrics = aggregate_metrics([employee])

analytics1, analytics2, analytics3 = st.columns(3)

with analytics1:

    st.metric(
        "Task Completion",
        f"{task_progress * 100:.0f}%",
    )

    st.progress(task_progress)


with analytics2:

    st.metric(
        "Document Completion",
        f"{document_progress * 100:.0f}%",
    )

    st.progress(document_progress)


with analytics3:

    st.metric(
        "Overall Onboarding",
        f"{overall_progress * 100:.0f}%",
    )

    st.progress(overall_progress)


# ============================================================
# FINAL STATUS
# ============================================================

st.write("")

# Recalculate because user may have interacted with tasks.
final_completed_tasks = sum(
    task.status == TaskStatus.COMPLETE
    for task in employee.tasks
)

final_received_documents = sum(
    employee.documents.values()
)


if (
    final_completed_tasks == total_tasks
    and final_received_documents == total_documents
):

    st.success(
        "Onboarding complete. "
        "All required tasks and documents have been completed."
    )

else:

    final_pending_tasks = (
        total_tasks - final_completed_tasks
    )

    final_pending_documents = (
        total_documents - final_received_documents
    )

    st.info(
        f"Your onboarding is still in progress. "
        f"{final_pending_tasks} task(s) and "
        f"{final_pending_documents} document(s) remain."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        PeopleHub Employee Experience Platform
        &nbsp;•&nbsp;
        Employee Onboarding
        &nbsp;•&nbsp;
        People Operations
        &nbsp;•&nbsp;
        v1.0
    </div>
    """,
    unsafe_allow_html=True,
)