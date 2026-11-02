import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
from data import load_data

REPORTS_DIR = "reports"

def clear():
    for _ in range(3):
        print()

def get_grade_and_status(total_marks):
    if total_marks >= 80:
        return "A+ (Outstanding)", "FIRST CLASS WITH DISTINCTION"
    elif total_marks >= 70:
        return "A  (Excellent)", "FIRST CLASS"
    elif total_marks >= 60:
        return "B+ (Very Good)", "FIRST CLASS"
    elif total_marks >= 50:
        return "B  (Good)", "SECOND CLASS"
    elif total_marks >= 40:
        return "C  (Average)", "PASS CLASS"
    else:
        return "F  (Fail)", "NEEDS REMEDIAL ATTENTION"

def generate_pdf_report(student, df):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    pdf_filename = f"{REPORTS_DIR}/ReportCard_{student['Enrollment_Number']}_{student['Name']}.pdf"

    df_temp = df.copy()
    df_temp["Rank"] = df_temp["Total"].rank(ascending=False, method="min")
    rank = int(df_temp.loc[df["Enrollment_Number"] == student["Enrollment_Number"], "Rank"].values[0])

    subject_cols = list(df.columns[2:7])
    total = float(student["Total"])
    avg = float(student["Average"])
    grade_str, division_str = get_grade_and_status(total)

    table_rows = []
    failed_subjects = []
    subject_names_clean = []
    student_scores = []

    for sub in subject_cols:
        val = student[sub]
        clean_name = sub.replace("_", " ")
        subject_names_clean.append(clean_name)
        if pd.isna(val) or val == "":
            mark_str = "ABSENT"
            sub_status = "ABSENT"
            failed_subjects.append(f"{clean_name} (Absent)")
            student_scores.append(0.0)
        else:
            m = float(val)
            student_scores.append(m)
            mark_str = f"{m:.1f}"
            if m >= 8.0:
                sub_status = "PASS"
            else:
                sub_status = "FAIL"
                failed_subjects.append(f"{clean_name} ({m:.1f}/20)")

        table_rows.append([clean_name, "20", "08", mark_str, sub_status])

    if failed_subjects:
        final_result = "RE-APPEAR / ATKT"
        result_color = "#dc2626"
        remarks = f"Needs improvement in: {', '.join(failed_subjects)}. Remedial classes recommended."
    elif total >= 80:
        final_result = "PASSED (DISTINCTION)"
        result_color = "#16a34a"
        remarks = "Outstanding academic performance across all subjects! Keep it up!"
    elif total >= 65:
        final_result = "PASSED (FIRST CLASS)"
        result_color = "#16a34a"
        remarks = "Good overall performance. Continue working consistently."
    else:
        final_result = "PASSED"
        result_color = "#2563eb"
        remarks = "Satisfactory performance. Put more practice in weaker topics."

    current_date = datetime.now().strftime("%d-%b-%Y")

    with plt.rc_context({
        'text.color': '#0f172a',
        'axes.labelcolor': '#0f172a',
        'xtick.color': '#0f172a',
        'ytick.color': '#0f172a',
        'figure.facecolor': '#ffffff',
        'axes.facecolor': '#ffffff',
        'legend.facecolor': '#ffffff',
        'legend.edgecolor': '#cbd5e1',
        'legend.labelcolor': '#0f172a'
    }):
        fig = plt.figure(figsize=(8.27, 11.69), facecolor='white')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='white')
        ax.axis("off")

        ax.add_patch(patches.Rectangle((0.03, 0.03), 0.94, 0.94, fill=False, edgecolor='#1e3a8a', linewidth=2.5))
        ax.add_patch(patches.Rectangle((0.036, 0.036), 0.928, 0.928, fill=False, edgecolor='#1e3a8a', linewidth=0.8))

        ax.add_patch(patches.Rectangle((0.036, 0.88), 0.928, 0.084, facecolor='#1e3a8a', edgecolor='none'))
        ax.text(0.5, 0.938, "MARKS ANALYZER | REPORT CARD GENERATOR", ha='center', va='center', fontsize=13, fontweight='bold', color='white')
        ax.text(0.5, 0.912, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", ha='center', va='center', fontsize=10, color='#cbd5e1')
        ax.text(0.5, 0.890, "MID SEMESTER TEST (MST) - STATEMENT OF MARKS", ha='center', va='center', fontsize=10, fontweight='bold', color='#fbbf24')

        ax.add_patch(patches.Rectangle((0.06, 0.77), 0.88, 0.095, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1))
        
        ax.text(0.08, 0.840, "Student Name", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.22, 0.840, f":  {student['Name'].upper()}", fontsize=9.5, color='#0f172a', fontweight='bold')
        
        ax.text(0.08, 0.812, "Enrollment No", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.22, 0.812, f":  {student['Enrollment_Number']}", fontsize=9.5, color='#0f172a', fontweight='bold')
        
        ax.text(0.08, 0.784, "Class Rank", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.22, 0.784, f":  {rank} out of {len(df)}", fontsize=9.5, color='#0f172a', fontweight='bold')

        ax.text(0.48, 0.840, "Academic Session", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.62, 0.840, "    :  2025-2026", fontsize=9.5, color='#0f172a')

        ax.text(0.48, 0.812, "Semester / Branch", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.62, 0.812, "    :  3rd Sem (CSE)", fontsize=9.5, color='#0f172a')

        ax.text(0.48, 0.784, "Result Status", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.62, 0.784, f":  {final_result}", fontsize=9.5, color=result_color, fontweight='bold')

        col_labels = ["Subject Name", "Max Marks", "Min Pass", "Marks Obtained", "Status"]
        col_widths = [0.38, 0.15, 0.15, 0.18, 0.14]

        table = ax.table(
            cellText=table_rows,
            colLabels=col_labels,
            colWidths=col_widths,
            loc='center',
            bbox=[0.06, 0.49, 0.88, 0.25]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)

        for (row_idx, col_idx), cell in table.get_celld().items():
            cell.set_edgecolor('#cbd5e1')
            if row_idx == 0:
                cell.set_facecolor('#1e3a8a')
                cell.set_text_props(color='#ffffff', fontweight='bold')
                cell.set_height(0.035)
            else:
                if row_idx % 2 == 0:
                    cell.set_facecolor('#f8fafc')
                else:
                    cell.set_facecolor('#ffffff')

                if col_idx == 4:
                    status_text = table_rows[row_idx - 1][4]
                    if status_text == "PASS":
                        cell.set_text_props(color='#16a34a', fontweight='bold')
                    else:
                        cell.set_text_props(color='#dc2626', fontweight='bold')
                elif col_idx in [1, 2, 3]:
                    cell.set_text_props(ha='center', color='#0f172a', fontweight='bold' if col_idx == 3 else 'normal')
                else:
                    cell.set_text_props(color='#0f172a', fontweight='bold')

        ax.add_patch(patches.Rectangle((0.06, 0.38), 0.88, 0.09, facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=1))

        ax.text(0.08, 0.440, "GRAND TOTAL", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.21, 0.440, f":  {total:.1f} / 100.0", fontsize=9.5, color='#0f172a', fontweight='bold')

        ax.text(0.08, 0.405, "PERCENTAGE", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.21, 0.405, f":  {total:.1f}%", fontsize=9.5, color='#0f172a', fontweight='bold')

        ax.text(0.46, 0.440, "FINAL GRADE", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.58, 0.440, f":  {grade_str}", fontsize=9.5, color='#1e3a8a', fontweight='bold')

        ax.text(0.46, 0.405, "DIVISION", fontsize=9, color='#64748b', fontweight='bold')
        ax.text(0.58, 0.405, f":  {division_str}", fontsize=8.5, color='#0f172a', fontweight='bold')

        ax_bar = fig.add_axes([0.10, 0.18, 0.80, 0.16], facecolor='#ffffff')
        bar_x = np.arange(len(subject_names_clean))
        bar_colors = ['#dc2626' if m < 8.0 else '#2563eb' for m in student_scores]
        bars = ax_bar.bar(bar_x, student_scores, color=bar_colors, width=0.45, edgecolor='#1e3a8a', zorder=3)
        ax_bar.axhline(8.0, color='#ef4444', linestyle='--', linewidth=1.5, label='Min Pass Marks (8)', zorder=4)
        ax_bar.set_xticks(bar_x)
        ax_bar.set_xticklabels(subject_names_clean, fontsize=8, rotation=10, color='#0f172a', fontweight='bold')
        ax_bar.set_yticks(np.arange(0, 21, 4))
        ax_bar.tick_params(colors='#0f172a', labelsize=8)
        for spine in ax_bar.spines.values():
            spine.set_color('#94a3b8')
        ax_bar.set_ylabel("Marks (out of 20)", fontsize=8, color='#0f172a', fontweight='bold')
        ax_bar.set_title("Subject Performance vs Passing Mark (8)", fontsize=8.5, fontweight='bold', pad=4, color='#1e3a8a')
        ax_bar.legend(loc='upper right', fontsize=7.5, facecolor='#ffffff', edgecolor='#cbd5e1', labelcolor='#0f172a')
        ax_bar.grid(axis='y', linestyle=':', color='#cbd5e1', alpha=0.8, zorder=0)

        for bar in bars:
            h = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width() / 2, h + 0.35, f"{h:.1f}", ha='center', fontsize=8, fontweight='bold', color='#0f172a')

        ax.add_patch(patches.Rectangle((0.06, 0.10), 0.88, 0.055, facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1))
        ax.text(0.08, 0.133, "REMARKS:", fontsize=8.5, color='#1e3a8a', fontweight='bold')
        ax.text(0.08, 0.112, remarks, fontsize=8.5, color='#334155', style='italic')

        ax.text(0.08, 0.055, f"Date of Issue: {current_date}", fontsize=8.5, color='#64748b')

        import io
        buf = io.BytesIO()
        fig.savefig(buf, format='pdf', dpi=200, bbox_inches='tight')
        plt.close(fig)
        pdf_bytes = buf.getvalue()

    # Safely save to disk: if file is already open in Adobe/browser, save with timestamp so PermissionError never occurs!
    try:
        with open(pdf_filename, "wb") as f:
            f.write(pdf_bytes)
    except PermissionError:
        ts = datetime.now().strftime("%H%M%S")
        pdf_filename = f"{REPORTS_DIR}/ReportCard_{student['Enrollment_Number']}_{student['Name']}_{ts}.pdf"
        with open(pdf_filename, "wb") as f:
            f.write(pdf_bytes)

    return pdf_filename

def open_pdf_file(filepath):
    try:
        if sys.platform.startswith("win"):
            os.startfile(os.path.abspath(filepath))
        elif sys.platform.startswith("darwin"):
            os.system(f'open "{filepath}"')
        else:
            os.system(f'xdg-open "{filepath}"')
    except Exception as e:
        print(f"Could not automatically open PDF: {e}")

def generate_single_report(df):
    print("\n" + "="*50)
    print("      GENERATE OFFICIAL PDF REPORT CARD")
    print("="*50)
    print("1. Search by Student Name")
    print("2. Search by Enrollment Number")
    opt = input("Enter choice (1-2): ").strip()

    student_row = None
    if opt == "1":
        sname = input("Enter Student Name: ").strip()
        matched = df[df.Name.str.strip().str.lower() == sname.lower()]
        if not matched.empty:
            student_row = matched.iloc[0]
        else:
            print(f"Student '{sname}' not found!")
    elif opt == "2":
        try:
            sid = int(input("Enter Enrollment Number: ").strip())
            matched = df[df.Enrollment_Number == sid]
            if not matched.empty:
                student_row = matched.iloc[0]
            else:
                print(f"Enrollment Number '{sid}' not found!")
        except ValueError:
            print("Enrollment number must be an integer!")
    else:
        print("Invalid choice!")

    if student_row is not None:
        print(f"\nGenerating high-quality PDF Report Card for {student_row['Name']}...")
        pdf_path = generate_pdf_report(student_row, df)
        print("="*60)
        print(f"✅ [SUCCESS] PDF Report Card created successfully!")
        print(f"📁 File Location: {os.path.abspath(pdf_path)}")
        print("="*60)

        open_choice = input("Do you want to open the PDF report card now? (y/n): ").strip().lower()
        if open_choice == 'y':
            open_pdf_file(pdf_path)

def generate_all_reports(df):
    print(f"\nGenerating PDF report cards for all {len(df)} students...")
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    saved_files = []
    for _, student in df.iterrows():
        pdf_path = generate_pdf_report(student, df)
        saved_files.append(pdf_path)

    print("="*60)
    print(f"✅ [SUCCESS] Generated {len(saved_files)} PDF Report Cards in folder: '{REPORTS_DIR}/'")
    print("="*60)
    for path in saved_files:
        print(f"  • {path}")

    open_choice = input("\nDo you want to open the reports folder? (y/n): ").strip().lower()
    if open_choice == 'y':
        open_pdf_file(REPORTS_DIR)

def generate_report_menu():
    while True:
        clear()
        df = load_data()
        print("*"*60)
        print("       OFFICIAL PDF REPORT CARD & MARKSHEET GENERATOR")
        print("*"*60)
        print("1. Generate PDF Report Card for a Specific Student")
        print("2. Generate PDF Report Cards for ALL Students (Batch Export)")
        print("3. Return to Main Menu")
        print("*"*60)
        ch = input("Enter your choice (1-3): ").strip()

        if ch == "1":
            generate_single_report(df)
            input("\nPress Enter to continue...")
        elif ch == "2":
            generate_all_reports(df)
            input("\nPress Enter to continue...")
        elif ch == "3":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice!")
            input("Press Enter to continue...")

if __name__ == "__main__":
    generate_report_menu()
