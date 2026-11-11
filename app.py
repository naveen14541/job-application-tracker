
import os
import mysql.connector
from datetime import datetime


def connect_db():
    """Connect Python to the MySQL database."""

    password = os.getenv("MYSQL_PASSWORD")

    if not password:
        raise ValueError(
            "MYSQL_PASSWORD is not set. Set it in your terminal first."
        )

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="job_tracker"
    )

    return connection


def add_job(connection):
    """Collect job details and insert a new application."""

    print("\n--- Add Job Application ---")

    cursor = connection.cursor()

    try:
        company_name = input("Company Name: ").strip()

        while not company_name:
            print("Company name cannot be empty!")
            company_name = input("Company Name: ").strip()

        job_role = input("Job Role: ").strip()

        while not job_role:
            print("Job role cannot be empty!")
            job_role = input("Job Role: ").strip()

        location = input("Location: ").strip()

        application_date = input(
            "Application Date (YYYY-MM-DD): "
        ).strip()

        while True:
            try:
                datetime.strptime(application_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date! Please use YYYY-MM-DD format.")
                application_date = input(
                    "Application Date (YYYY-MM-DD): "
                ).strip()

        allowed_statuses = [
            "Applied", "Test", "Interview", "Rejected", "Selected"
        ]

        status = input("Status: ").strip().capitalize()

        while status not in allowed_statuses:
            print(
                "Invalid status! Choose: "
                "Applied, Test, Interview, Rejected, Selected"
            )
            status = input("Status: ").strip().capitalize()

        interview_date = input(
            "Interview Date (YYYY-MM-DD, press Enter if none): "
        ).strip()

        while interview_date != "":
            try:
                datetime.strptime(interview_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date! Please use YYYY-MM-DD format.")
                interview_date = input(
                    "Interview Date (YYYY-MM-DD, press Enter if none): "
                ).strip()

        if interview_date == "":
            interview_date = None

        job_link = input("Job Link: ").strip()
        notes = input("Notes: ").strip()

        query = """
        INSERT INTO job_applications
        (
            company_name,
            job_role,
            location,
            application_date,
            status,
            interview_date,
            job_link,
            notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            company_name,
            job_role,
            location,
            application_date,
            status,
            interview_date,
            job_link,
            notes
        )

        cursor.execute(query, values)
        connection.commit()

        print("\nJob application added successfully!")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()


def view_jobs(connection):
    """Display all saved job applications."""

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM job_applications")
        jobs = cursor.fetchall()

        print("\n--- Saved Job Applications ---")
        print("Total jobs:", len(jobs))

        for job in jobs:
            print("ID:", job[0])
            print("Company:", job[1])
            print("Role:", job[2])
            print("Location:", job[3])
            print("Application Date:", job[4])
            print("Status:", job[5])
            print("Interview Date:", job[6])
            print("--------------------")

    finally:
        cursor.close()


def delete_job(connection):
    """Delete a job application."""

    print("\n--- Delete Job Application ---")

    job_id = input("Enter Job ID to delete: ").strip()

    while not job_id.isdigit() or int(job_id) <= 0:
        print("Invalid Job ID! Enter a positive number.")
        job_id = input("Enter Job ID to delete: ").strip()

    job_id = int(job_id)

    print("Selected Job ID:", job_id)

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM job_applications WHERE id = %s",
            (job_id,)
        )

        job = cursor.fetchone()

        if job is None:
            print("Job ID not found!")
            return

        print("Job ID found! Ready to delete.")

        confirm = input(
            "Are you sure you want to delete this job? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Deletion cancelled!")
            return

        cursor.execute(
            "DELETE FROM job_applications WHERE id = %s",
            (job_id,)
        )

        connection.commit()
        print("Job application deleted successfully!")

    except Exception as error:
        connection.rollback()
        print("Failed to delete job:", error)

    finally:
        cursor.close()


def edit_job(connection):
    """Update an existing job application."""

    print("\n--- Edit Job Application ---")

    job_id = input("Enter Job ID to edit: ").strip()

    while not job_id.isdigit() or int(job_id) <= 0:
        print("Invalid Job ID! Enter a positive number.")
        job_id = input("Enter Job ID to edit: ").strip()

    job_id = int(job_id)

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, company_name, job_role, status, location, interview_date
            FROM job_applications
            WHERE id = %s
            """,
            (job_id,)
        )

        job = cursor.fetchone()

        if job is None:
            print("Job ID not found!")
            return

        print("Job ID:", job[0])
        print("Company:", job[1])
        print("Role:", job[2])
        print("Current Status:", job[3])
        print("Current Location:", job[4])
        print("Current Interview Date:", job[5])

    finally:
        cursor.close()

    allowed_statuses = [
        "Applied", "Test", "Interview", "Rejected", "Selected"
    ]

    new_status = input(
        "Enter new status (Applied/Test/Interview/Rejected/Selected): "
    ).strip().capitalize()

    while new_status not in allowed_statuses:
        print("Invalid status! Please choose an allowed status.")

        new_status = input(
            "Enter new status (Applied/Test/Interview/Rejected/Selected): "
        ).strip().capitalize()

    new_location = input(
        "Enter new location (press Enter to keep current): "
    ).strip()

    if not new_location:
        new_location = job[4]

    new_interview_date = input(
        "Enter new interview date (YYYY-MM-DD, press Enter to keep current): "
    ).strip()

    if not new_interview_date:
        new_interview_date = job[5]

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE job_applications
            SET
                status = %s,
                location = %s,
                interview_date = %s
            WHERE id = %s
            """,
            (new_status, new_location, new_interview_date, job_id)
        )

        connection.commit()
        print("Job details updated successfully!")

    except Exception as error:
        connection.rollback()
        print("Failed to update job:", error)

    finally:
        cursor.close()

def search_job(connection):
    """Search job applications by company name."""

    print("\n--- Search Job Application ---")
    
    job_id = input("Enter Job ID (press Enter to search by name/role): ").strip()

    if job_id:
        if not job_id.isdigit() or int(job_id) <= 0:
            print("Invalid Job ID!")
            return

        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT * FROM job_applications WHERE id = %s",
                (int(job_id),)
            )

            jobs = cursor.fetchall()

            if not jobs:
                print("No job application found!")
            else:
                for job in jobs:
                    print("ID:", job[0])
                    print("Company:", job[1])
                    print("Role:", job[2])
                    print("Status:", job[5])

        finally:
            cursor.close()

        return

    company_name = input("Enter Company Name or Job Role to search: ").strip()

    cursor = connection.cursor()

    try:
        query = """
        SELECT * FROM job_applications
        WHERE company_name LIKE %s
        OR job_role LIKE %s
        """

        search_value = f"%{company_name}%"
        cursor.execute(query, (search_value, search_value))
        jobs = cursor.fetchall()

        if not jobs:
            print("No job applications found!")
        else:
            print("Search Results:")
            for job in jobs:
                print("ID:", job[0])
                print("Company:", job[1])
                print("Role:", job[2])
                print("Status:", job[5])
                print("--------------------")

    finally:
        cursor.close()
        
def dashboard(connection):
    """Display job application statistics."""

    print("\n--- Job Application Dashboard ---")

    cursor = connection.cursor()

    try:
        query = """
        SELECT
            COUNT(*) AS total_jobs,
            SUM(status = 'Applied') AS applied_count,
            SUM(status = 'Test') AS test_count,
            SUM(status = 'Interview') AS interview_count,
            SUM(status = 'Rejected') AS rejected_count,
            SUM(status = 'Selected') AS selected_count
        FROM job_applications
        """

        cursor.execute(query)
        result = cursor.fetchone()

    finally:
        cursor.close()

    total_jobs = result[0]
    selected_jobs = result[5] or 0

    if total_jobs > 0:
        success_rate = (selected_jobs / total_jobs) * 100
    else:
        success_rate = 0

    print("Total Jobs:", total_jobs)
    print("Applied:", result[1] or 0)
    print("Test:", result[2] or 0)
    print("Interview:", result[3] or 0)
    print("Rejected:", result[4] or 0)
    print("Selected:", selected_jobs)
    print("Success Rate:", round(success_rate, 2), "%")
            
def export_jobs_to_csv(connection):
    """Export all job applications to a CSV file."""

    print("\n--- Export Jobs to CSV ---")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM job_applications")
        jobs = cursor.fetchall()

    finally:
        cursor.close()
    import csv

    with open("jobs_export.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Company",
            "Role",
            "Location",
            "Application Date",
            "Status",
            "Interview Date",
            "Job Link",
            "Notes"
        ])

        writer.writerows(jobs)

    print("Jobs exported successfully!")
    

def filter_jobs_by_status(connection):
    """Filter job applications by status."""

    print("\n--- Filter Jobs by Status ---")

    status = input(
        "Enter Job Status (Applied/Test/Interview/Rejected/Selected): "
    ).strip().title()

    valid_statuses = [
        "Applied",
        "Test",
        "Interview",
        "Rejected",
        "Selected"
    ]

    if status not in valid_statuses:
        print("Invalid status! Please enter a valid status.")
        return

    cursor = connection.cursor()

    try:
        query = """
        SELECT *
        FROM job_applications
        WHERE status = %s
        """

        cursor.execute(query, (status,))
        jobs = cursor.fetchall()

    finally:
        cursor.close()

    if not jobs:
        print("No jobs found with this status.")
        return

    for job in jobs:
        print("\nJob ID:", job[0])
        print("Company:", job[1])
        print("Role:", job[2])
        print("Status:", job[5])
        print("----------------------")
    
def main():
    """Main menu of the Job Application Tracker."""

    connection = None

    try:
        connection = connect_db()
        print("Database connected successfully!")

        while True:
            print("\n===== JOB APPLICATION TRACKER =====")
            print("1. Add Job")
            print("2. View Jobs")
            print("3. Edit Job")
            print("4. Exit")
            print("5. Search Job")
            print("6. Delete Job")
            print("7. Dashboard")
            print("8. Export Jobs to CSV")
            print("9. Filter Jobs by Status")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                add_job(connection)

            elif choice == "2":
                view_jobs(connection)

            elif choice == "3":
                edit_job(connection)

            elif choice == "4":
                print("Exiting Job Application Tracker...")
                break
            
            elif choice == "5":
                search_job(connection)
                
            elif choice == "6":
                delete_job(connection)
            
            elif choice == "7":
                dashboard(connection)
                
            elif choice == "8":
                export_jobs_to_csv(connection)
                
            elif choice == "9":
                filter_jobs_by_status(connection)
                
            else:
                print("Invalid choice! Please enter 1, 2, 3, 4, 5, 6, 7, 8 or 9.")

    except Exception as error:
        print("An error occurred:", error)

    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
