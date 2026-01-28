# db.py
# Handles all database-related operations using SQLite

import sqlite3

DB_NAME = "journal.db"


# ============================
# Database connection
# ============================
def get_connection():
    """
    Create and return a database connection.
    check_same_thread=False is required for Streamlit.
    """
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ============================
# Table creation
# ============================
def create_tables():
    """
    Create required tables if they do not exist.
    Safe to run multiple times.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Chat history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT,
            date TEXT
        )
    """)

    # Journals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            journal_date TEXT,
            title TEXT,
            content TEXT,
            sentiment TEXT
        )
    """)

    conn.commit()
    conn.close()


# ============================
# Chat functions
# ============================
def save_chat(role, message, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO journal_entries (role, message, date) VALUES (?, ?, ?)",
        (role, message, date)
    )

    conn.commit()
    conn.close()


def load_chat():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, message, date FROM journal_entries ORDER BY id"
    )
    rows = cursor.fetchall()

    conn.close()
    return rows


def clear_chat():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM journal_entries")

    conn.commit()
    conn.close()


# ============================
# Journal functions
# ============================
def save_journal(journal_date, title, content, sentiment):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO journals (journal_date, title, content, sentiment)
        VALUES (?, ?, ?, ?)
        """,
        (journal_date, title, content, sentiment)
    )

    conn.commit()
    conn.close()


def load_journals():
    """
    Load all journals (newest first).
    Returns: (id, journal_date, title, content, sentiment)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, journal_date, title, content, sentiment
        FROM journals
        ORDER BY id DESC
        """
    )
    rows = cursor.fetchall()

    conn.close()
    return rows


def update_journal_title(journal_id, new_title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE journals SET title = ? WHERE id = ?",
        (new_title, journal_id)
    )

    conn.commit()
    conn.close()


def delete_journal(journal_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM journals WHERE id = ?",
        (journal_id,)
    )

    conn.commit()
    conn.close()
