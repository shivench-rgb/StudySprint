
import sqlite3
import pandas as pd

DB_NAME = "studysprint.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            due_date TEXT NOT NULL,
            priority TEXT NOT NULL,
            estimated_minutes INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_task(title, subject, due_date,
             priority, estimated_minutes):
    connection = get_connection()

    connection.execute("""
        INSERT INTO tasks
        (title, subject, due_date, priority, estimated_minutes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title, subject, str(due_date),
        priority, estimated_minutes
    ))

    connection.commit()
    connection.close()


def get_tasks():
    connection = get_connection()

    data = pd.read_sql_query(
        "SELECT * FROM tasks ORDER BY due_date ASC",
        connection
    )

    connection.close()
    return data


def update_task(task_id, title, subject, due_date,
                priority, estimated_minutes, completed):
    connection = get_connection()

    connection.execute("""
        UPDATE tasks
        SET title = ?, subject = ?, due_date = ?,
            priority = ?, estimated_minutes = ?, completed = ?
        WHERE id = ?
    """, (
        title, subject, str(due_date),
        priority, estimated_minutes,
        int(completed), task_id
    ))

    connection.commit()
    connection.close()


def delete_task(task_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()