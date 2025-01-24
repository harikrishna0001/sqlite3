import sqlite3

# Create a connection to the database
sqliteconnection = sqlite3.connect('students.db')
cursor = sqliteconnection.cursor()

# Create the students table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
""")

sqliteconnection.commit()
sqliteconnection.close()


def add_students():
    sqliteconnection = sqlite3.connect('students.db')
    cursor = sqliteconnection.cursor()
    
    name = input("Enter the name of student: ")

    cursor.execute("""
    INSERT INTO students (name)
    VALUES (?)
    """, (name,))

    sqliteconnection.commit()
    sqliteconnection.close()
    print(f"Student {name} added.")


def delete_students():
    sqliteconnection = sqlite3.connect('students.db')
    cursor = sqliteconnection.cursor()
    
    student_id = input("Enter the ID of the student you want to delete: ")

    cursor.execute("""
    DELETE FROM students WHERE id = ?
    """, (student_id,))

    sqliteconnection.commit()
    sqliteconnection.close()
    print(f"Student with ID {student_id} deleted.")


def show_table():
    # Show the students in the table
    sqliteconnection = sqlite3.connect('students.db')
    cursor = sqliteconnection.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    if rows:
        print("\nStudents in the table:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}")
    else:
        print("No students found.")
    
    sqliteconnection.close()


def main():
    while True:
        print("\nSelect an option:")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Show Students")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_students()
        elif choice == '2':
            delete_students()
        elif choice == '3':
            show_table()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
