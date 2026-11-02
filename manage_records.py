import pandas as pd
import numpy as np
from data import (
    load_data,
    add_student_record,
    update_student_record,
    delete_student_record
)

def clear():
    for _ in range(3):
        print()

def get_valid_float(prompt, min_val=0.0, max_val=20.0, allow_blank=True):
    while True:
        val = input(prompt).strip()
        if allow_blank and val == "":
            return np.nan
        try:
            num = float(val)
            if min_val <= num <= max_val:
                return num
            else:
                print(f"Marks must be between {min_val} and {max_val}!")
        except ValueError:
            print("Invalid input! Please enter a valid number (e.g. 15 or 14.5).")

def recalculate_row(df, index):
    subject_cols = list(df.columns[2:7])
    marks_series = pd.to_numeric(df.loc[index, subject_cols], errors="coerce")
    total = marks_series.sum(skipna=True)
    avg = marks_series.mean(skipna=True)
    df.loc[index, "Total"] = round(total, 2)
    df.loc[index, "Average"] = round(avg, 2)

def add_student(df):
    print("\n" + "="*50)
    print("             ADD NEW STUDENT RECORD")
    print("="*50)

    name = input("Enter Student Name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return df

    while True:
        try:
            roll = int(input("Enter 4-digit Enrollment Number: ").strip())
            if roll in df["Enrollment_Number"].values:
                print(f"Enrollment number {roll} already exists for {df.loc[df.Enrollment_Number==roll, 'Name'].values[0]}! Try another.")
                continue
            break
        except ValueError:
            print("Enrollment number must be an integer!")

    subject_cols = list(df.columns[2:7])
    print("\nEnter Marks for each subject (Out of 20, press Enter if absent):")
    student_data = {"Name": name, "Enrollment_Number": roll}

    for sub in subject_cols:
        marks = get_valid_float(f"  • {sub:<20} : ", 0, 20, allow_blank=True)
        student_data[sub] = marks


    marks_list = [student_data[s] for s in subject_cols if pd.notna(student_data[s])]
    total = sum(marks_list) if marks_list else 0.0
    avg = (total / len(subject_cols)) if subject_cols else 0.0

    student_data["Total"] = round(total, 2)
    student_data["Average"] = round(avg, 2)

    add_student_record(student_data)
    df = load_data()

    print("\n[SUCCESS] Student record added successfully to PostgreSQL!")
    return df

def update_student(df):
    print("\n" + "="*50)
    print("             UPDATE STUDENT RECORD")
    print("="*50)

    sid = input("Enter Student Enrollment Number to update: ").strip()
    try:
        sid_int = int(sid)
    except ValueError:
        print("Invalid Enrollment number!")
        return df

    matched = df[df.Enrollment_Number == sid_int]
    if matched.empty:
        print(f"No student found with Enrollment Number {sid_int}!")
        return df

    idx = matched.index[0]
    student = df.loc[idx]
    subject_cols = list(df.columns[2:7])

    print(f"\nCurrent Record for: {student['Name']} (Roll: {student['Enrollment_Number']})")
    for sub in subject_cols:
        print(f"  • {sub:<20} : {student[sub]}")
    print(f"  • Total Marks          : {student['Total']}")
    print(f"  • Average Marks        : {student['Average']}")

    print("\nWhat would you like to update?")
    print("1. Update specific subject marks")
    print("2. Update all subjects marks")
    print("3. Update Student Name")
    print("4. Cancel")
    opt = input("Enter choice (1-4): ").strip()

    if opt == "1":
        print("\nAvailable subjects:")
        for i, s in enumerate(subject_cols, 1):
            print(f"  {i}. {s}")
        try:
            sub_choice = int(input("Select subject (1-5): "))
            if 1 <= sub_choice <= len(subject_cols):
                target_sub = subject_cols[sub_choice - 1]
                new_marks = get_valid_float(f"Enter new marks for {target_sub} (0-20, leave blank if absent): ")
                df.loc[idx, target_sub] = new_marks
                recalculate_row(df, idx)

                student_data = df.loc[idx].to_dict()
                update_student_record(sid_int, student_data)
                print(f"\n[SUCCESS] Marks updated! New Total: {df.loc[idx, 'Total']}, Average: {df.loc[idx, 'Average']}")
            else:
                print("Invalid subject choice!")
        except ValueError:
            print("Invalid input!")

    elif opt == "2":
        print("\nEnter new marks for all subjects:")
        for sub in subject_cols:
            df.loc[idx, sub] = get_valid_float(f"  • {sub:<20} : ")
        recalculate_row(df, idx)

        student_data = df.loc[idx].to_dict()  
        update_student_record(sid_int, student_data)
        print(f"\n[SUCCESS] All marks updated! New Total: {df.loc[idx, 'Total']}, Average: {df.loc[idx, 'Average']}")

    elif opt == "3":
        new_name = input("Enter new name: ").strip()
        if new_name:
            df.loc[idx, "Name"] = new_name
            student_data = df.loc[idx].to_dict()
            update_student_record(sid_int, student_data)
            print("[SUCCESS] Student name updated!")

    elif opt == "4":
        print("Update cancelled.")
    else:
        print("Invalid choice!")

    return df

def delete_student(df):
    print("\n" + "="*50)
    print("             DELETE STUDENT RECORD")
    print("="*50)

    sid = input("Enter Student Enrollment Number to delete: ").strip()
    

    matched = df[df.Enrollment_Number == sid]
    if matched.empty:
        print(f"No student found with Enrollment Number {sid}!")
        return df

    idx = matched.index[0]
    student = df.loc[idx]
    print(f"\nFound Student: {student['Name']} (Enrollment: {student['Enrollment_Number']})")
    print(f"Total Marks: {student['Total']}, Average: {student['Average']}")

    confirm = input("\nAre you SURE you want to permanently delete this record? (y/n): ").strip().lower()
    if confirm == 'y':
        deleted = delete_student_record(sid)

        if deleted:
            df = load_data()
            print("[SUCCESS] Student record deleted from PostgreSQL!")
        else:
            print("Student record could not be deleted.")
    else:
        print("Deletion cancelled.")

    return df

def view_all_records(df):
    print("\n" + "="*80)
    print(f"                 ALL STUDENT RECORDS ({len(df)} Students)")
    print("="*80)
    print(df.to_string(index=False))
    print("="*80)

def manage_records_menu():
    while True:
        clear()
        df = load_data()
        print("*"*60)
        print("             STUDENT RECORDS MANAGEMENT (CRUD)")
        print("*"*60)
        print("1. Add New Student Record")
        print("2. Update Student Record")
        print("3. Delete Student Record")
        print("4. View All Student Records")
        print("5. Return to Main Menu")
        print("*"*60)
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            df = add_student(df)
            input("\nPress Enter to continue...")
        elif choice == "2":
            df = update_student(df)
            input("\nPress Enter to continue...")
        elif choice == "3":
            df = delete_student(df)
            input("\nPress Enter to continue...")
        elif choice == "4":
            view_all_records(df)
            input("\nPress Enter to continue...")
        elif choice == "5":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice! Please select 1-5.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    manage_records_menu()

