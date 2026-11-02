import pandas as pd
import numpy as np
from data import load_data

df=pd.DataFrame()
df=load_data()

def clear():
    for x in range(3):
        print()

def show_details():
    print(df)

def MST_analysis():
    df=load_data()
    while True:
        clear()
        print("MST MARKS ANALYSIS")
        print("*"*90)
        print("1.Show marks of every students.")
        print("2.Show marks of specific student.")
        print("3.Show marks of specific subject of all students.")
        print("4.Average marks of each student.")
        print("5.Highest marks in specific subject.")
        print("6.Lowest marks in specific subject.")
        print("7.Detailed performance analysis of a student.")
        print("8.Overall Class Performance Summary.")
        print("9.Subject-wise Class Performance Analysis.")
        print("10.Student Improvement Report.")
        print("11.Exit.")
        ch=int(input("Enter your choice="))
        if ch==1:
            show_details()
            wait=input("Press Enter to continue....")

        elif ch==2:
            while True:
                print("\nEnter 1 to continue using name.")
                print("Enter 2 to continue using enrollment number.")
                print("Enter 3 for exit.")
                ch1=int(input("Enter your choice="))
                if ch1==1:
                    sname=input("Enter the name of student=").strip()
                    match=df[df.Name.str.strip().str.lower()==sname.lower()]
                    if not match.empty:
                        df1=df.loc[df.Name.str.strip().str.lower()==sname.lower(),:]
                        print(df1)
                    else :
                        print(f"Student '{sname}' not found!")
                        print(f"Available students: {list(df['Name'])}")

                elif ch1==2:
                    sid=int(input("Enter the last 4 digit of your enrollment number="))
                    match=df[df.Enrollment_Number==sid]
                    if not match.empty:
                        df1=df.loc[df.Enrollment_Number==sid,:]
                        print(df1)
                    else:
                        print(f"Enrollement Number '{sid}' not found!")
                        print(f"Available Enrollment numbers: {list(df['Enrollment_Number'])}")

                elif ch1==3:
                    break
                
                else:
                    print("Invalid choice!")
                wait=input("Press Enter to continue....")
        
        elif ch==3:
            col=list(df.columns)
            sub=input("Enter the Name of the subject=")
            if sub in col:
                print(df[["Name", sub]])
            else:
                print(f"'{sub}' not found in columns! Available columns: {col[2:7]}")
            wait=input("Press Enter to continue....")
        
        elif ch==4:
            print(df[["Name","Average"]])
            wait=input("Press Enter to continue....")

        elif ch==5:
            col=list(df.columns)
            sub=input("Enter the name of the subject=")
            if sub in col:
                max_marks=df[sub].max()
                std=df.loc[df[sub]==max_marks,["Name",sub]]
                print(std)
            else:
                print(f"'{sub}' not found in columns! Available columns: {col[2:7]}")
            wait=input("Press Enter to continue...")

        elif ch==6:
            col=list(df.columns)
            sub=input("Enter the name of the subject=")
            if sub in col:
                min_marks=df[sub].min()
                std=df.loc[df[sub]==min_marks,["Name",sub]]
                print(std)
            else:
                print(f"'{sub}' not found in columns! Available columns: {col[2:7]}")
            wait=input("Press Enter to continue...")

        elif ch==7:
            while True:
                print("\nEnter 1 to continue using name.")
                print("Enter 2 to continue using Enrollement number.")
                print("Enter 3 for exit.")
                ch1=int(input("Enter your choice="))
                if ch1==1:
                    sname=input("Enter the name of student=").strip()
                    match=df[df.Name.str.strip().str.lower()==sname.lower()]
                    if not match.empty:
                        student=match.iloc[0]
                        col=list(df.columns)
                        subject_cols=col[2:7]
                        sub_marks=pd.to_numeric(student[subject_cols], errors="coerce")

                        high_sub=sub_marks.idxmax()
                        high_val=sub_marks.max()
                        low_sub=sub_marks.idxmin()
                        low_val=sub_marks.min()

                        df_temp=df.copy()
                        df_temp["Rank"]=df_temp["Total"].rank(ascending=False, method="min")
                        rank=int(df_temp.loc[match.index[0], "Rank"])

                        print()
                        print("="*60)
                        print(f"       STUDENT ANALYSIS REPORT: {student['Name'].upper()}")
                        print("="*60)
                        print(f"Enrollment Number : {student['Enrollment_Number']}")
                        print(f"Total Marks       : {student['Total']}")
                        print(f"Average Marks     : {student['Average']}")
                        print(f"Class Rank        : {rank} out of {len(df)}")
                        print(f"Highest Marks     : {high_val} (Subject: {high_sub})")
                        print(f"Lowest Marks      : {low_val} (Subject: {low_sub})")
                        print("-"*60)
                        print("Subject-wise Marks Breakdown:")
                        for s in subject_cols:
                            marks_val = student[s]
                            if pd.isna(marks_val):
                                marks_val = "Absent / Not Available"
                            print(f"  • {s:<20} : {marks_val}")
                        print("="*60)
                    else:
                        print(f"Student '{sname}' not found!")
                        print(f"Available students: {list(df['Name'])}")
                    wait=input("Press Enter to continue....")

                elif ch1==2:
                    sid=int(input("Enter the last 4 digit of enrollement number of student="))
                    match=df[df.Enrollment_Number==sid]
                    if not match.empty:
                        student=match.iloc[0]
                        col=list(df.columns)
                        subject_cols=col[2:7]
                        sub_marks=pd.to_numeric(student[subject_cols], errors="coerce")

                        high_sub=sub_marks.idxmax()
                        high_val=sub_marks.max()
                        low_sub=sub_marks.idxmin()
                        low_val=sub_marks.min()

                        df_temp=df.copy()
                        df_temp["Rank"]=df_temp["Total"].rank(ascending=False, method="min")
                        rank=int(df_temp.loc[match.index[0], "Rank"])

                        print()
                        print("="*60)
                        print(f"       STUDENT ANALYSIS REPORT: {student['Name'].upper()}")
                        print("="*60)
                        print(f"Enrollment Number : {student['Enrollment_Number']}")
                        print(f"Total Marks       : {student['Total']}")
                        print(f"Average Marks     : {student['Average']}")
                        print(f"Class Rank        : {rank} out of {len(df)}")
                        print(f"Highest Marks     : {high_val} (Subject: {high_sub})")
                        print(f"Lowest Marks      : {low_val} (Subject: {low_sub})")
                        print("-"*60)
                        print("Subject-wise Marks Breakdown:")
                        for s in subject_cols:
                            marks_val = student[s]
                            if pd.isna(marks_val):
                                marks_val = "Absent / Not Available"
                            print(f"  • {s:<20} : {marks_val}")
                        print("="*60)
                    else:
                        print(f"Enrollment Number '{sid}' not found!")
                        print(f"Available Enrollement numbers of students: {list(df['Enrollment_Number'])}")
                    wait=input("Press Enter to continue....")

                elif ch1==3:
                    break

                else:
                    print("Invalid choice!")
                wait=input("Press Enter to continue....")

        elif ch==8:
            col=list(df.columns)
            subject_cols=col[2:7]

            total_students=len(df)
            class_avg=df["Average"].mean()
            class_total_avg=df["Total"].mean()

            max_total=df["Total"].max()
            toppers=df.loc[df["Total"]==max_total, "Name"].tolist()
            topper_names=", ".join(toppers)

            min_total=df["Total"].min()
            low_performers=df.loc[df["Total"]==min_total, "Name"].tolist()
            low_names=", ".join(low_performers)

            above_students=df.loc[df["Average"]>=class_avg, "Name"].tolist()
            below_students=df.loc[df["Average"]<class_avg, "Name"].tolist()
            above_names=", ".join(above_students)
            below_names=", ".join(below_students)

            print()
            print("="*75)
            print("                     CLASS PERFORMANCE SUMMARY")
            print("="*75)
            print(f"Total Students in Class : {total_students}")
            print(f"Class Average (Marks)   : {class_avg:.2f} / 20")
            print(f"Class Average (Total)   : {class_total_avg:.2f} / 100")
            print(f"Class Topper(s)         : {topper_names} ({max_total} Marks)")
            print(f"Lowest Scorer(s)        : {low_names} ({min_total} Marks)")
            print(f"Students >= Class Avg   : {len(above_students)} students ({above_names})")
            print(f"Students < Class Avg    : {len(below_students)} students ({below_names})")
            print("-"*75)
            print("SUBJECT-WISE ANALYSIS:")
            print(f"{'Subject':<22} {'Average':<10} {'Highest (Student)':<25} {'Lowest (Student)':<20}")
            print("-" * 75)

            sub_averages={}
            for sub in subject_cols:
                sub_series=pd.to_numeric(df[sub], errors="coerce")
                sub_avg=sub_series.mean()
                sub_averages[sub]=sub_avg

                sub_max=sub_series.max()
                max_std=df.loc[df[sub]==sub_max, "Name"].tolist()
                max_info=f"{sub_max} ({', '.join(max_std)})"

                sub_min=sub_series.min()
                min_std=df.loc[df[sub]==sub_min, "Name"].tolist()
                min_info=f"{sub_min} ({', '.join(min_std)})"

                print(f"{sub:<22} {sub_avg:<10.2f} {max_info:<25} {min_info:<20}")

            print("-" * 75)
            best_sub=max(sub_averages, key=sub_averages.get)
            toughest_sub=min(sub_averages, key=sub_averages.get)
            print(f"★ Best Scoring Subject    : {best_sub} (Average: {sub_averages[best_sub]:.2f})")
            print(f"▲ Toughest Subject        : {toughest_sub} (Average: {sub_averages[toughest_sub]:.2f})")
            print("=" * 75)
            wait=input("Press Enter to continue....")

        elif ch==9:
            col=list(df.columns)
            subject_cols=col[2:7]
            sub_input=input("Enter the name of the subject=").strip()

            matched_sub=None
            for s in subject_cols:
                if s.lower()==sub_input.lower():
                    matched_sub=s
                    break

            if matched_sub:
                sub=matched_sub
                sub_series=pd.to_numeric(df[sub], errors="coerce")

                sub_avg=sub_series.mean()
                sub_max=sub_series.max()
                sub_min=sub_series.min()

                highest_students=df.loc[df[sub]==sub_max, "Name"].tolist()
                lowest_students=df.loc[df[sub]==sub_min, "Name"].tolist()

                above_students=df.loc[df[sub]>=sub_avg, "Name"].tolist()
                below_students=df.loc[df[sub]<sub_avg, "Name"].tolist()
                absent_students=df.loc[df[sub].isna(), "Name"].tolist()

                print()
                print("="*75)
                print(f"             SUBJECT PERFORMANCE ANALYSIS: {sub.upper()}")
                print("="*75)
                print(f"Class Average in {sub}    : {sub_avg:.2f} / 20")
                print(f"Highest Marks Scored      : {sub_max} ({', '.join(highest_students)})")
                print(f"Lowest Marks Scored       : {sub_min} ({', '.join(lowest_students)})")
                print(f"Students >= Subject Avg   : {len(above_students)} students ({', '.join(above_students)})")
                print(f"Students < Subject Avg    : {len(below_students)} students ({', '.join(below_students)})")
                if absent_students:
                    print(f"Absent Students           : {len(absent_students)} students ({', '.join(absent_students)})")
                print("-"*75)
                print(f"Student-wise Marks in {sub}:")
                for _, row in df.iterrows():
                    val=row[sub]
                    if pd.isna(val):
                        val_str="Absent / Not Available"
                    else:
                        val_str=f"{val}"
                    print(f"  • {row['Name']:<20} : {val_str}")
                print("="*75)
            else:
                print(f"'{sub_input}' not found! Available subjects: {subject_cols}")
            wait=input("Press Enter to continue....")

        elif ch==10:
            while True:
                print("\nEnter 1 to continue using name.")
                print("Enter 2 to continue using enrollment number.")
                print("Enter 3 to exit.")
                ch1=int(input("Enter your choice="))
                if ch1==1:
                    sname=input("Enter the name of student=").strip()
                    match=df[df.Name.str.strip().str.lower()==sname.lower()]
                    if not match.empty:
                        student=match.iloc[0]
                        col=list(df.columns)
                        subject_cols=col[2:7]

                        tot_val=student['Total']
                        tot_str=f"{int(tot_val)}" if pd.notna(tot_val) and float(tot_val).is_integer() else f"{tot_val}"
                        avg_val=student['Average']
                        avg_str=f"{int(avg_val)}" if pd.notna(avg_val) and float(avg_val).is_integer() else f"{avg_val}"

                        print()
                        print("==========" + " IMPROVEMENT REPORT " + "==========")
                        print()
                        print(f"Student Name : {student['Name']}")
                        print(f"Enrollment Number : {student['Enrollment_Number']}")
                        print(f"Total        : {tot_str}/100")
                        print(f"Average      : {avg_str}/20")
                        print()
                        print("Subject-wise Analysis:")
                        print()

                        priority_list=[]

                        for sub in subject_cols:
                            raw_val=student[sub]
                            if pd.isna(raw_val) or raw_val=="":
                                remark="Needs Improvement (Absent)"
                                score_display="Absent"
                                priority_list.append((sub, -1, "Absent", 14))
                            else:
                                m=float(raw_val)
                                m_str=f"{int(m)}" if m.is_integer() else f"{m}"
                                score_display=f"{m_str}/20"
                                if m >= 17:
                                    remark="Strong"
                                elif m >= 14:
                                    remark="Good"
                                elif m >= 10:
                                    remark="Average"
                                    priority_list.append((sub, m, m_str, 15))
                                else:
                                    remark="Needs Improvement"
                                    priority_list.append((sub, m, m_str, 14))

                            print(f"{sub:<20} : {score_display:<8} - {remark}")

                        priority_list.sort(key=lambda x: x[1])

                        print()
                        print("Priority Subjects:")
                        if priority_list:
                            for idx, (psub, _, _, _) in enumerate(priority_list, 1):
                                print(f"{idx}. {psub}")
                        else:
                            print("None! All subjects are performing well (Good/Strong).")

                        print()
                        print("Suggested Target:")
                        if priority_list:
                            for psub, _, p_mstr, p_target in priority_list:
                                print(f"{psub:<20} : {p_mstr} -> {p_target}")
                        else:
                            print("Maintain current performance and aim for 20/20 in all subjects!")

                        print("="*42)
                    else:
                        print(f"Student '{sname}' not found!")
                        print(f"Available students: {list(df['Name'])}")
                    wait=input("Press Enter to continue....")

                elif ch1==2:
                    sid=int(input("Enter the Enrollment number of the student="))
                    match=df[df.Enrollment_Number==sid]
                    if not match.empty:
                        student=match.iloc[0]
                        col=list(df.columns)
                        subject_cols=col[2:7]

                        tot_val=student['Total']
                        tot_str=f"{int(tot_val)}" if pd.notna(tot_val) and float(tot_val).is_integer() else f"{tot_val}"
                        avg_val=student['Average']
                        avg_str=f"{int(avg_val)}" if pd.notna(avg_val) and float(avg_val).is_integer() else f"{avg_val}"

                        print()
                        print("==========" + " IMPROVEMENT REPORT " + "==========")
                        print()
                        print(f"Student Name : {student['Name']}")
                        print(f"Enrollment Number : {student['Enrollment_Number']}")
                        print(f"Total        : {tot_str}/100")
                        print(f"Average      : {avg_str}/20")
                        print()
                        print("Subject-wise Analysis:")
                        print()

                        priority_list=[]

                        for sub in subject_cols:
                            raw_val=student[sub]
                            if pd.isna(raw_val) or raw_val=="":
                                remark="Needs Improvement (Absent)"
                                score_display="Absent"
                                priority_list.append((sub, -1, "Absent", 14))
                            else:
                                m=float(raw_val)
                                m_str=f"{int(m)}" if m.is_integer() else f"{m}"
                                score_display=f"{m_str}/20"
                                if m >= 17:
                                    remark="Strong"
                                elif m >= 14:
                                    remark="Good"
                                elif m >= 10:
                                    remark="Average"
                                    priority_list.append((sub, m, m_str, 15))
                                else:
                                    remark="Needs Improvement"
                                    priority_list.append((sub, m, m_str, 14))

                            print(f"{sub:<20} : {score_display:<8} - {remark}")

                        priority_list.sort(key=lambda x: x[1])

                        print()
                        print("Priority Subjects:")
                        if priority_list:
                            for idx, (psub, _, _, _) in enumerate(priority_list, 1):
                                print(f"{idx}. {psub}")
                        else:
                            print("None! All subjects are performing well (Good/Strong).")

                        print()
                        print("Suggested Target:")
                        if priority_list:
                            for psub, _, p_mstr, p_target in priority_list:
                                print(f"{psub:<20} : {p_mstr} -> {p_target}")
                        else:
                            print("Maintain current performance and aim for 20/20 in all subjects!")

                        print("="*42)
                    else:
                        print(f"Enrollment number '{sid}' not found!")
                        print(f"Available Enrollment Numbers: {list(df['Enrollment_Number'])}")
                    wait=input("Press Enter to continue....")

                elif ch1==3:
                    break

                else :
                    print("Invalid choice!")

        elif ch==11:
            print("Exiting MST Analysis Menu...")
            break

        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    MST_analysis()


