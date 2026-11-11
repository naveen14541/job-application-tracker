while True:
    print("\n===== JOB APPLICATION TRACKER =====")
    print("1. Add Job")
    print("2. View Jobs")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("Opening Add Job...")
    elif choice == "2":
        print("Opening View Jobs...")
    elif choice == "3":
        print("Exiting Job Application Tracker...")
        break
    else:
        print("Invalid choice! Please enter 1, 2, or 3.")