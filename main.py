import sys
from manage_records import manage_records_menu
from analysis import MST_analysis
from visualization import MST_graph
from generate_report import generate_report_menu

def clear():
    for _ in range(3):
        print()

def login():
    print("\n" + "="*72)
    print("MST MARKS ANALYZER".center(72))
    print("="*72)
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    if username == "MST" and password == "Master peace":
        print("Login successful!")
        main_dashboard()
    elif username != "MST" and password == "Master peace":
        print("Invalid username!")
        sys.exit(0)
    elif username == "MST" and password != "Master peace":
        print("Invalid password!")
        sys.exit(0)
    else:
        print("Invalid credentials!")
        sys.exit(0)

def main_dashboard():
    while True:
        clear()
        print("╔" + "═"*72 + "╗")
        print("║" + "MID SEMESTER TEST (MST) MARKS MANAGEMENT & ANALYTICS SYSTEM".center(72) + "║")
        print("║" + "Session 2025-2026".center(72) + "║")
        print("╠" + "═"*72 + "╣")
        print("║  1. 📝 Manage Student Records (Add / Update / Delete / View)           ║")
        print("║  2. 📊 Tabular Marks Analysis & Performance Reports                    ║")
        print("║  3. 📈 Graphical Visualizations & Analytics Charts                     ║")
        print("║  4. 📄 Report Card Generator                                           ║")
        print("║  5. ❌ Exit System                                                     ║")
        print("╚" + "═"*72 + "╝")

        ch = input("Enter your choice (1-5): ").strip()

        if ch == "1":
            manage_records_menu()
        elif ch == "2":
            MST_analysis()
        elif ch == "3":
            MST_graph()
        elif ch == "4":
            generate_report_menu()
        elif ch == "5":
            print("\nThank you for using MST Management & Analytics System. Goodbye!")
            sys.exit(0)
        else:
            print("\n[!] Invalid choice! Please select an option between 1 and 5.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    login()

