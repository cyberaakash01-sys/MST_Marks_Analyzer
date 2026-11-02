import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv("db.env")


def get_database_url():
    try:
        if "database" in st.secrets:
            return st.secrets["database"]["url"]
    except Exception:
        pass

    return os.getenv("DATABASE_URL")


@st.cache_resource
def get_engine():
    return create_engine(
        get_database_url(),
        pool_pre_ping=True
    )


def load_data():
    query = text("SELECT * FROM public.student_marks")

    with get_engine().connect() as connection:
        df = pd.read_sql(query, connection)

    return df

def add_student_record(student_data):
    query = text("""
        INSERT INTO public.student_marks
        ("Name", "Enrollment_Number", "EEEs",
         "Discrete_Structure", "Data_Structure",
         "DCS", "OOPM", "Total", "Average")
        VALUES (
            :Name, :Enrollment_Number, :EEEs,
            :Discrete_Structure, :Data_Structure,
            :DCS, :OOPM, :Total, :Average
        )
    """)

    with get_engine().begin() as connection:
        connection.execute(query, student_data)

def update_student_record(enrollment_number, student_data):
    query = text("""
        UPDATE public.student_marks
        SET
            "Name" = :Name,
            "EEEs" = :EEEs,
            "Discrete_Structure" = :Discrete_Structure,
            "Data_Structure" = :Data_Structure,
            "DCS" = :DCS,
            "OOPM" = :OOPM,
            "Total" = :Total,
            "Average" = :Average
        WHERE "Enrollment_Number" = :Enrollment_Number
    """)

    student_data["Enrollment_Number"] = enrollment_number

    with get_engine().begin() as connection:
        connection.execute(query, student_data)

def delete_student_record(enrollment_number):
    query = text("""
        DELETE FROM public.student_marks
        WHERE "Enrollment_Number" = :enrollment_number
    """)

    with get_engine().begin() as connection:
        result = connection.execute(
            query,
            {"enrollment_number": enrollment_number}
        )

    return result.rowcount > 0