"""Reusable database queries."""
import pandas as pd
from connection import get_connection


def get_students():
    conn = get_connection()

    query = """
        SELECT
            student_id,
            first_name,
            last_name,
            email,
            phone,
            enrollment_date,
            status
        FROM students
        ORDER BY student_id DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df


def add_student(first_name, last_name, email, phone,
                enrollment_date, status):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO students
        (first_name, last_name, email, phone,
         enrollment_date, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            first_name,
            last_name,
            email,
            phone,
            enrollment_date,
            status
        )
    )

    conn.commit()
    cursor.close()
    conn.close()


def update_student(student_id, first_name, last_name,
                   email, phone, enrollment_date, status):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE students
        SET
            first_name = %s,
            last_name = %s,
            email = %s,
            phone = %s,
            enrollment_date = %s,
            status = %s
        WHERE student_id = %s
    """

    cursor.execute(
        query,
        (
            first_name,
            last_name,
            email,
            phone,
            enrollment_date,
            status,
            student_id
        )
    )

    conn.commit()
    cursor.close()
    conn.close()


def delete_student(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        DELETE FROM students
        WHERE student_id = %s
    """

    cursor.execute(query, (student_id,))

    conn.commit()
    cursor.close()
    conn.close()