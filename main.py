import sqlite3

# Create the database and tables if they don't exist
sqliteconnection = sqlite3.connect('students.db')
cursor = sqliteconnection.cursor()

# Create the students table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
""")

# Create the marklist table with an additional 'name' column to store the student's name
cursor.execute("""
    CREATE TABLE IF NOT EXISTS marklist (
        student_id INTEGER NOT NULL,
        name TEXT NOT NULL,  
        maths TEXT NOT NULL,
        english TEXT NOT NULL,
        chemistry TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id)
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


def add_mark():
    sqliteconnection = sqlite3.connect('students.db')
    cursor = sqliteconnection.cursor()

    # Get the student's name and fetch their ID
    student_name = input("Enter the student's name: ")
    cursor.execute("SELECT id FROM students WHERE name = ?", (student_name,))
    student = cursor.fetchone()

    if student:
        student_id = student[0]

        # Get marks for each subject
        maths = input("Enter the Maths mark: ")
        english = input("Enter the English mark: ")
        chemistry = input("Enter the Chemistry mark: ")

        # Insert into the marklist table (now including the student's name)
        cursor.execute("""
        INSERT INTO marklist (student_id, name, maths, english, chemistry)
        VALUES (?, ?, ?, ?, ?);
        """, (student_id, student_name, maths, english, chemistry))

        sqliteconnection.commit()
        print(f"Marks for {student_name} added successfully.")
    else:
        print(f"Student {student_name} not found.")

    sqliteconnection.close()


def delete_students():
    sqliteconnection = sqlite3.connect('students.db')
    cursor = sqliteconnection.cursor()

    student_id = input("Enter the ID of the student you want to delete: ")

    # First, delete the marks associated with the student
    cursor.execute("""
    DELETE FROM marklist WHERE student_id = ?
    """, (student_id,))

    # Now delete the student
    cursor.execute("""
    DELETE FROM students WHERE id = ?
    """, (student_id,))

    sqliteconnection.commit()
    sqliteconnection.close()
    print(f"Student with ID {student_id} and their marks deleted.")


def show_table():
    sqliteconnection = sqlite3.connect('students.db')
    cursor = sqliteconnection.cursor()

    cursor.execute("""
        SELECT students.name, marklist.maths, marklist.english, marklist.chemistry
        FROM students
        JOIN marklist ON students.id = marklist.student_id
    """)
    rows = cursor.fetchall()

    if rows:
        print("\nStudents and their marks:")
        for row in rows:
            print(f"Name: {row[0]}, Maths: {row[1]}, English: {row[2]}, Chemistry: {row[3]}")
    else:
        print("No students or marks found.")

    sqliteconnection.close()


def main():
    while True:
        print("\nSelect an option:")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Show Students and Marks")
        print("4. Add Marks")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_students()
        elif choice == '2':
            delete_students()
        elif choice == '3':
            show_table()
        elif choice == '4':
            add_mark()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
