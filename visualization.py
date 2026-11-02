import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data import load_data 

df=pd.DataFrame()
df=load_data()

def clear():
    for x in range(3):
        print()

def MST_graph():
    while True:
        clear()
        print("1.Total marks of every students.")
        print("2.Marks obtained by students in each subject.")
        print("3.Marks obtained by specific student.")
        print("4.Average marks obtained by every students.")
        print("5.Subject wise class average.")
        print("6.Marks of all students in a specific subject.")
        print("7.Student vs Class Average Benchmark Comparison.")
        print("8.Class Grade Distribution (Pie Chart).")
        print("9.Exit.")
        ch=int(input("Enter your choice="))
        if ch==1:
            x=df['Name']
            y=df["Total"]
            bars=plt.bar(x,y, color='royalblue', edgecolor='black')
            plt.yticks(np.arange(0,101,10))
            plt.xlabel("Students-->")
            plt.ylabel("Marks-->")
            plt.title("Total marks scored by students.")
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f"{height:.1f}", ha='center', fontsize=9)
            plt.show()
            wait=input("Press Enter to continue...")
        
        elif ch==2:
            sub=list(df.columns[2:7])
            ax=df.plot(x="Name",y=sub,kind="bar",figsize=(11,6))
            plt.yticks(np.arange(0,21,2))
            plt.title("Marks obtained by students in each subject.")
            plt.ylabel("Marks-->")
            plt.xlabel("Students-->")
            plt.xticks(rotation=0)
            plt.legend(title='Subjects')
            for c in ax.containers:
                ax.bar_label(c, padding=2, fontsize=7)
            plt.show()
            wait=input("Press Enter to continue...")

        elif ch==3:
            while True:
                print("\nEnter 1 to continue using name.")
                print("Enter 2 to continue using Enrollment number.")
                print("Enter 3 to exit.")
                ch1=int(input("Enter your choice="))
                if ch1==1:
                    sname = input("Enter the name of student: ").strip()
                    student = df[df.Name.str.strip().str.lower() == sname.lower()]
                    if not student.empty:
                        subjects = list(df.columns[2:7])
                        marks = pd.to_numeric(student.iloc[0][subjects], errors='coerce').fillna(0).values
                
                        bars=plt.bar(subjects, marks, color='skyblue', edgecolor='black')
                        plt.title(f"Marks of {student.iloc[0]['Name']} in each subject")
                        plt.xlabel("Subjects -->")
                        plt.ylabel("Marks -->")
                        plt.yticks(np.arange(0, 21, 2))
                        plt.xticks(rotation=20)
                        for bar in bars:
                            height = bar.get_height()
                            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f"{height:.1f}", ha='center', fontsize=9)
                        plt.show()
                    else:
                        print(f"Student '{sname}' not found!")
                        print(f"Available students: {list(df['Name'])}")
                    wait=input("Press Enter to continue...")

                elif ch1==2:
                    sid = int(input("Enter the Enrollment number of the student: "))
                    student = df[df.Enrollment_Number==sid]
                    if not student.empty:
                        subjects = list(df.columns[2:7])
                        marks = pd.to_numeric(student.iloc[0][subjects], errors='coerce').fillna(0).values
                
                        bars=plt.bar(subjects, marks, color='skyblue', edgecolor='black')
                        plt.title(f"Marks of {student.iloc[0]['Name']} in each subject")
                        plt.xlabel("Subjects -->")
                        plt.ylabel("Marks -->")
                        plt.yticks(np.arange(0, 21, 2))
                        plt.xticks(rotation=20)
                        for bar in bars:
                            height = bar.get_height()
                            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f"{height:.1f}", ha='center', fontsize=9)
                        plt.show()
                    else:
                        print(f"Enrollment number '{sid}' not found!")
                        print(f"Available Enrollment numbers: {list(df['Enrollment_Number'])}")
                    wait=input("Press Enter to continue...")
                
                elif ch1==3:
                    break

                else :
                    print("Invalid choice!")

        elif ch==4:
            x=df['Name']
            y=df['Average']
            bars=plt.bar(x,y, color='coral', edgecolor='black')
            plt.yticks(np.arange(0,21,2))
            plt.ylabel("Marks-->")
            plt.xlabel("Students-->")
            plt.title("Average Performance of all students")
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f"{height:.2f}", ha='center', fontsize=9)
            plt.show()
            wait=input("Press Enter to continue...")

        elif ch==5:
            subjects = list(df.columns[2:7])
            avg_marks = [df[sub].mean() for sub in subjects]
            
            bars = plt.bar(subjects, avg_marks, color='teal', edgecolor='black')
            plt.yticks(np.arange(0, 21, 2))
            plt.title("Subject-wise Class Average Performance")
            plt.xlabel("Subjects -->")
            plt.ylabel("Marks -->")
            plt.xticks(rotation=20)
            
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f"{height:.2f}", ha='center', fontsize=9)
            
            plt.show()
            wait=input("Press Enter to continue...")

        elif ch==6:
            subject_cols = list(df.columns[2:7])
            sub_input = input("Enter the name of the subject: ").strip()

            # Case-insensitive subject match
            matched_sub = None
            for s in subject_cols:
                if s.lower() == sub_input.lower():
                    matched_sub = s
                    break

            if matched_sub:
                sub = matched_sub
                x = df['Name']
                y = pd.to_numeric(df[sub], errors='coerce').fillna(0)

                bars = plt.bar(x, y, color='mediumpurple', edgecolor='black')
                plt.yticks(np.arange(0, 21, 2))
                plt.xlabel("Students -->")
                plt.ylabel("Marks -->")
                plt.title(f"Marks scored by all students in {sub}")
                plt.xticks(rotation=20)

                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    if pd.isna(df.loc[i, sub]) or df.loc[i, sub] == "":
                        label = "Absent"
                    else:
                        label = f"{height:.1f}"
                    plt.text(bar.get_x() + bar.get_width() / 2, height + 0.3, label, ha='center', fontsize=9)

                plt.show()
            else:
                print(f"'{sub_input}' not found! Available subjects: {subject_cols}")
            wait = input("Press Enter to continue...")

        elif ch==7:
            while True:
                print("\nEnter 1 to continue using name.")
                print("Enter 2 to continue using Enrollment number.")
                print("Enter 3 to exit.")
                ch1=int(input("Enter your choice="))
                student_row = None
                if ch1==1:
                    sname = input("Enter the name of student: ").strip()
                    matched = df[df.Name.str.strip().str.lower() == sname.lower()]
                    if not matched.empty:
                        student_row = matched.iloc[0]
                    else:
                        print(f"Student '{sname}' not found!")
                        print(f"Available students: {list(df['Name'])}")
                elif ch1==2:
                    sid = int(input("Enter the Enrollment number of student: "))
                    matched = df[df.Enrollment_Number == sid]
                    if not matched.empty:
                        student_row = matched.iloc[0]
                    else:
                        print(f"Enrollment number '{sid}' not found!")
                        print(f"Available Enrollment numbers: {list(df['Enrollment_Number'])}")
                elif ch1==3:
                    break
                else:
                    print("Invalid choice!")

                if student_row is not None:
                    subjects = list(df.columns[2:7])
                    std_marks = [pd.to_numeric(student_row[sub], errors='coerce') for sub in subjects]
                    std_marks_plot = [0 if pd.isna(m) else m for m in std_marks]
                    class_avgs = [round(df[sub].mean(), 2) for sub in subjects]

                    x_indices = np.arange(len(subjects))
                    width = 0.35

                    plt.figure(figsize=(10, 6))
                    bars1 = plt.bar(x_indices - width/2, std_marks_plot, width=width, label=f"{student_row['Name']}'s Marks", color='royalblue', edgecolor='black')
                    bars2 = plt.bar(x_indices + width/2, class_avgs, width=width, label="Class Average", color='orange', edgecolor='black')

                    plt.xticks(x_indices, subjects, rotation=15)
                    plt.yticks(np.arange(0, 21, 2))
                    plt.ylabel("Marks -->")
                    plt.xlabel("Subjects -->")
                    plt.title(f"{student_row['Name']} vs Class Average Benchmark", fontsize=13, fontweight='bold')
                    plt.legend()

                    for idx, bar in enumerate(bars1):
                        height = bar.get_height()
                        label = "Absent" if pd.isna(std_marks[idx]) else f"{height:.1f}"
                        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.3, label, ha='center', fontsize=8, fontweight='bold')

                    for bar in bars2:
                        height = bar.get_height()
                        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f"{height:.1f}", ha='center', fontsize=8)

                    plt.tight_layout()
                    plt.show()

                wait = input("Press Enter to continue...")

        elif ch==8:
            grade_a = df[df["Total"] >= 80]
            grade_b = df[(df["Total"] >= 60) & (df["Total"] < 80)]
            grade_c = df[(df["Total"] >= 40) & (df["Total"] < 60)]
            needs_imp = df[df["Total"] < 40]

            grades_config = [
                ("Grade A (>= 80%)", grade_a, '#2ecc71'),
                ("Grade B (60-79%)", grade_b, '#3498db'),
                ("Grade C (40-59%)", grade_c, '#f39c12'),
                ("Needs Improvement (< 40%)", needs_imp, '#e74c3c'),
            ]

            print("\n" + "="*65)
            print("             CLASS GRADE DISTRIBUTION SUMMARY")
            print("="*65)
            for title, subset, _ in grades_config:
                count = len(subset)
                pct = (count / len(df)) * 100
                print(f"• {title:<28} : {count} students ({pct:.1f}%)")
                if count > 0:
                    names_with_roll = [f"{r['Name']} ({r['Enrollment_Number']})" for _, r in subset.iterrows()]
                    print(f"  Students: {', '.join(names_with_roll)}")
                else:
                    print("  Students: None")
            print("="*65)

            active_grades = [(t, s, c) for t, s, c in grades_config if len(s) > 0]
            sizes = [len(s) for _, s, _ in active_grades]
            colors = [c for _, _, c in active_grades]
            explode = [0.05] * len(sizes)
            slice_labels = [f"{t}\n({len(s)} students)" for t, s, _ in active_grades]

            legend_labels = []
            for t, s, _ in active_grades:
                names = ", ".join([f"{r['Name']} ({r['Enrollment_Number']})" for _, r in s.iterrows()])
                legend_labels.append(f"{t}: {len(s)} student(s)\n  • {names}")

            fig, ax = plt.subplots(figsize=(12, 6))
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=slice_labels,
                autopct='%1.1f%%',
                startangle=140,
                colors=colors,
                explode=explode,
                shadow=True,
                textprops={'fontsize': 10, 'fontweight': 'bold'}
            )

            for at in autotexts:
                at.set_fontsize(10)
                at.set_color('white')
                at.set_fontweight('bold')

            ax.legend(
                wedges,
                legend_labels,
                title="Students List by Grade",
                title_fontsize=11,
                loc="center left",
                bbox_to_anchor=(1.05, 0.5),
                fontsize=9
            )
            plt.title("Class Overall Grade Distribution (MST Result)", fontsize=14, fontweight='bold', pad=15)
            plt.tight_layout()
            plt.show()
            wait = input("Press Enter to continue...")

        elif ch==9:
            print("Exiting Graph Menu...")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    MST_graph()


