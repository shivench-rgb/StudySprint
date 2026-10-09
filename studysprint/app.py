```python
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from database import (
    create_table,
    add_task,
    get_tasks,
    update_task,
    delete_task
)

st.set_page_config(
    page_title="StudySprint",
    page_icon="📚",
    layout="wide"
)

create_table()

PRIORITIES = ["Low", "Medium", "High"]


def dashboard():
    st.title("StudySprint")
    st.caption("Plan your study. Track your progress.")

    data = get_tasks()

    if data.empty:
        st.info("No study tasks yet. Add your first task!")
        return

    total = len(data)
    completed = int(data["completed"].sum())
    pending = total - completed

    due_dates = pd.to_datetime(
        data["due_date"], errors="coerce"
    ).dt.date

    overdue = int(
        ((due_dates < date.today()) &
         (data["completed"] == 0)).sum()
    )

    first, second, third, fourth = st.columns(4)

    first.metric("Total Tasks", total)
    second.metric("Completed", completed)
    third.metric("Pending", pending)
    fourth.metric("Overdue", overdue)

    progress = completed / total

    st.subheader("Overall Progress")
    st.progress(progress)
    st.write(str(round(progress * 100, 1)) + "% completed")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Task Completion")

        chart_data = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Tasks": [completed, pending]
        })

        figure = px.pie(
            chart_data,
            names="Status",
            values="Tasks",
            hole=0.45
        )

        st.plotly_chart(
            figure,
            width="stretch"
        )

    with right:
        st.subheader("Tasks by Subject")

        subject_data = (
            data.groupby("subject")
            .size()
            .reset_index(name="Tasks")
            .sort_values("Tasks", ascending=False)
        )

        figure = px.bar(
            subject_data,
            x="subject",
            y="Tasks",
            labels={"subject": "Subject"}
        )

        st.plotly_chart(
            figure,
            width="stretch"
        )

    st.subheader("Upcoming Pending Tasks")

    upcoming = data[data["completed"] == 0].copy()

    upcoming["_due"] = pd.to_datetime(
        upcoming["due_date"], errors="coerce"
    )

    upcoming = upcoming.sort_values("_due").head(10)

    if upcoming.empty:
        st.success("All your study tasks are completed!")
    else:
        st.dataframe(
            upcoming[
                [
                    "title",
                    "subject",
                    "due_date",
                    "priority",
                    "estimated_minutes"
                ]
            ],
            hide_index=True,
            width="stretch"
        )


def add_task_page():
    st.title("Add Study Task")

    with st.form("add_task_form"):
        title = st.text_input("Task title")
        subject = st.text_input("Subject")

        due_date = st.date_input(
            "Due date",
            value=date.today()
        )

        priority = st.selectbox(
            "Priority",
            PRIORITIES,
            index=1
        )

        estimated_minutes = st.number_input(
            "Estimated study time (minutes)",
            min_value=15,
            max_value=600,
            value=60,
            step=15
        )

        submitted = st.form_submit_button(
            "Save Task",
            width="stretch"
        )

        if submitted:
            if not title.strip() or not subject.strip():
                st.error("Enter both task title and subject.")
            else:
                add_task(
                    title.strip(),
                    subject.strip(),
                    due_date,
                    priority,
                    estimated_minutes
                )

                st.success("Study task saved!")
                st.rerun()


def manage_tasks_page():
    st.title("Manage Study Tasks")

    data = get_tasks()

    if data.empty:
        st.info("Add a task before managing your tasks.")
        return

    search = st.text_input("Search task or subject")

    status_filter = st.selectbox(
        "Completion status",
        ["All", "Pending", "Completed"]
    )

    filtered = data.copy()

    if status_filter == "Pending":
        filtered = filtered[filtered["completed"] == 0]
    elif status_filter == "Completed":
        filtered = filtered[filtered["completed"] == 1]

    if search.strip():
        mask = (
            filtered["title"].str.contains(
                search,
                case=False,
                na=False,
                regex=False
            )
            |
            filtered["subject"].str.contains(
                search,
                case=False,
                na=False,
                regex=False
            )
        )

        filtered = filtered[mask]

    display_data = filtered.copy()

    display_data["Status"] = display_data["completed"].map(
        {0: "Pending", 1: "Completed"}
    )

    st.dataframe(
        display_data[
            [
                "id",
                "title",
                "subject",
                "due_date",
                "priority",
                "estimated_minutes",
                "Status"
            ]
        ],
        hide_index=True,
        width="stretch"
    )

    st.divider()
    st.subheader("Edit a Task")

    task_ids = data["id"].astype(int).tolist()

    selected_id = st.selectbox(
        "Select task ID",
        task_ids
    )

    selected = data[data["id"] == selected_id].iloc[0]

    with st.form("edit_task_form"):
        title = st.text_input(
            "Task title",
            value=str(selected["title"])
        )

        subject = st.text_input(
            "Subject",
            value=str(selected["subject"])
        )

        due_date = st.date_input(
            "Due date",
            value=pd.to_datetime(
                selected["due_date"]
            ).date()
        )

        priority = st.selectbox(
            "Priority",
            PRIORITIES,
            index=PRIORITIES.index(selected["priority"])
        )

        estimated_minutes = st.number_input(
            "Estimated study time (minutes)",
            min_value=15,
            max_value=600,
            value=int(selected["estimated_minutes"]),
            step=15
        )

        completed = st.checkbox(
            "Mark this task as completed",
            value=bool(selected["completed"])
        )

        submitted = st.form_submit_button("Update Task")

        if submitted:
            if not title.strip() or not subject.strip():
                st.error("Task title and subject are required.")
            else:
                update_task(
                    int(selected_id),
                    title.strip(),
                    subject.strip(),
                    due_date,
                    priority,
                    estimated_minutes,
                    completed
                )

                st.success("Task updated!")
                st.rerun()

    st.divider()
    st.subheader("Delete a Task")

    confirm_key = "confirm_delete_id"

    if st.button("Delete Selected Task", width="stretch"):
        st.session_state[confirm_key] = int(selected_id)

    if st.session_state.get(confirm_key) == int(selected_id):
        st.warning("Are you sure you want to delete this task?")

        yes, no = st.columns(2)

        with yes:
            if st.button("Confirm Delete", width="stretch"):
                delete_task(int(selected_id))
                del st.session_state[confirm_key]
                st.rerun()

        with no:
            if st.button("Cancel", width="stretch"):
                del st.session_state[confirm_key]
                st.rerun()


def main():
    st.sidebar.title("StudySprint")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Study Task",
            "Manage Tasks"
        ]
    )

    if page == "Dashboard":
        dashboard()
    elif page == "Add Study Task":
        add_task_page()
    elif page == "Manage Tasks":
        manage_tasks_page()

    st.sidebar.divider()
    st.sidebar.caption("Stay consistent. Keep learning.")


if __name__ == "__main__":
    main()
```
