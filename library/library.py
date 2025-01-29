import sqlite3

def get_connection():
    return sqlite3.connect('library.db')

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS library (
            book_id INTEGER NOT NULL,
            price TEXT NOT NULL,
            author TEXT NOT NULL,
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    """)
    
    conn.commit()
    conn.close()

def add_book_with_details():
    conn = get_connection()
    cursor = conn.cursor()
    
    name = input("Enter book name: ")
    price = input("Enter book price: ")
    author = input("Enter book author: ")

    # Check if book already exists
    cursor.execute("SELECT id FROM books WHERE name = ?", (name,))
    existing_book = cursor.fetchone()
    
    if existing_book:
        print(f"Error: Book '{name}' already exists in the database!")
        conn.close()
        return

    # Insert new book
    cursor.execute("INSERT INTO books (name) VALUES (?)", (name,))
    book_id = cursor.lastrowid
    
    # Insert details
    cursor.execute("""
        INSERT INTO library (book_id, price, author)
        VALUES (?, ?, ?)
    """, (book_id, price, author))
    
    conn.commit()
    print(f"Book '{name}' added successfully with all details!")
    conn.close()

def update_book_details():
    conn = get_connection()
    cursor = conn.cursor()
    
    book_id = input("Enter book ID to update: ")
    
    # Verify book exists
    cursor.execute("""
        SELECT books.name, library.price, library.author 
        FROM books
        JOIN library ON books.id = library.book_id
        WHERE books.id = ?
    """, (book_id,))
    book = cursor.fetchone()
    
    if not book:
        print("Book not found!")
        conn.close()
        return
    
    print("Current details:")
    print(f"Name: {book[0]}, Price: {book[1]}, Author: {book[2]}")
    
    # Get updates
    new_name = input(f"Enter new name [{book[0]}]: ") or book[0]
    new_price = input(f"Enter new price [{book[1]}]: ") or book[1]
    new_author = input(f"Enter new author [{book[2]}]: ") or book[2]
    
    # Update records
    cursor.execute("UPDATE books SET name = ? WHERE id = ?", (new_name, book_id))
    cursor.execute("""
        UPDATE library 
        SET price = ?, author = ?
        WHERE book_id = ?
    """, (new_price, new_author, book_id))
    
    conn.commit()
    conn.close()
    print("Book details updated successfully!")

def remove_book():
    conn = get_connection()
    cursor = conn.cursor()
    
    book_id = input("Enter book ID to remove: ")
    
    # Check if book exists
    cursor.execute("SELECT id FROM books WHERE id = ?", (book_id,))
    if not cursor.fetchone():
        print("No book found with that ID!")
        conn.close()
        return
    
    # Delete records
    cursor.execute("DELETE FROM library WHERE book_id = ?", (book_id,))
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    
    conn.commit()
    print(f"Book ID {book_id} removed successfully!")
    conn.close()

def view_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT books.id, books.name, library.price, library.author
        FROM books
        JOIN library ON books.id = library.book_id
    """)
    
    books = cursor.fetchall()
    
    if not books:
        print("No books in the library!")
        conn.close()
        return
    
    print("\nAll Books:")
    print("-" * 60)
    for book in books:
        print(f"ID: {book[0]}")
        print(f"Title: {book[1]}")
        print(f"Price: {book[2]}")
        print(f"Author: {book[3]}")
        print("-" * 60)
    
    conn.close()

def main_menu():
    create_tables()
    
    while True:
        print("\nLibrary Management System")
        print("1. Add New Book with Details")
        print("2. Update Book Details")
        print("3. Remove Book")
        print("4. View All Books")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            add_book_with_details()
        elif choice == '2':
            update_book_details()
        elif choice == '3':
            remove_book()
        elif choice == '4':
            view_all_books()
        elif choice == '0':
            print("Exiting program...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()