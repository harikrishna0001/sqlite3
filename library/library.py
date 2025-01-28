import  sqlite3

sqliteconnection = sqlite3.connect('library.db')
cursor = sqliteconnection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS library (
        book_id INTEGER NOT NULL,
        name TEXT NOT NULL,  
        price TEXT NOT NULL,
        author TEXT NOT NULL,
        FOREIGN KEY(book_id) REFERENCES books(id)
    )
""")

sqliteconnection.commit()
sqliteconnection.close()


def add_book():
   
    name = input("Enter the name of book: ")

    cursor.execute("""
    INSERT INTO books (name)
    VALUES (?)
    """, (name,))

    sqliteconnection.commit()
    sqliteconnection.close()
    print(f"book {name} added.")

def add_book_details():
   
    book_name = input("Enter the book's name: ")
    cursor.execute("SELECT id FROM book WHERE name = ?", (book_name,))
    books= cursor.fetchone()

    if books:
        book_id = books[0]

        price = input("Enter the book price : ")
        author = input("Enter the book author: ")
       
        cursor.execute("""
        INSERT INTO library (student_id, name, price, author)
        VALUES (?, ?, ?, ?, ?);
        """, (book_id, book_name, price, author,))

        sqliteconnection.commit()
        print(f"details for {book_name} added successfully.")
    else:
        print(f"book {book_name} not found.")

    sqliteconnection.close()


def update_book_details():
   

 
    book_id = input("Enter the ID of the book you want to update : ")

    
    new_name = input("Enter the new name of the book : ")


    cursor.execute("""
    UPDATE books
    SET name = ?
    WHERE id = ?
    """, (new_name, book_id))


    cursor.execute("""
    UPDATE library
    SET name = ?
    WHERE book_id = ?
    """, (new_name, book_id))

    sqliteconnection.commit()
    sqliteconnection.close()
    print(f"book ID {book_id} updated to {new_name}.")



def remove_book():
   


    book_id = input("Enter the ID of the book you want to remove: ")

    cursor.execute("""
    remove FROM library WHERE book_id = ?
    """, (book_id,))


    cursor.execute("""
    remove FROM book WHERE id = ?
    """, (book_id,))

    sqliteconnection.commit()
    sqliteconnection.close()
    print(f"book with ID {book_id} and  deleted.")


def show_table():
   

    cursor.execute("""
        SELECT books.name, library.price, library.author
        FROM students
        JOIN library ON book.id = library.book_id
    """)
    rows = cursor.fetchall()

    if rows:
        print("\nbooks and details:")
        for row in rows:
            print(f"Name: {row[0]}, price: {row[1]}, author: {row[2]},")
    else:
        print("No book found.")

    sqliteconnection.close()

while True:
        print("\nSelect an option:")
        print("1. Add book")
        print("2. Add book details")
        print("3. Update book")
        print("4. Remove book")
        print("5. Veiw all book")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            add_book_details()
        elif choice == '3':
            update_book_details()
        elif choice == '4':
            remove_book()
        elif choice == '5':
            show_table()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")





