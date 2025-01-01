import sqlite3
from datetime import datetime

# Database initialization
def initialize_database():
    conn = sqlite3.connect("car_plates.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Plates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate TEXT NOT NULL UNIQUE,
        price REAL NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('available', 'sold'))
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(plate_id) REFERENCES Plates(id),
        FOREIGN KEY(user_id) REFERENCES Users(id)
    )
    """)

    conn.commit()
    conn.close()

# Add a new plate
def add_plate(plate, price):
    conn = sqlite3.connect("car_plates.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Plates (plate, price, status) VALUES (?, ?, 'available')", (plate, price))
    conn.commit()
    conn.close()

# View available plates
def view_available_plates():
    conn = sqlite3.connect("car_plates.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, plate, price FROM Plates WHERE status = 'available'")
    plates = cursor.fetchall()
    conn.close()
    return plates

# Sell a plate
def sell_plate(plate_id, user_name, user_address):
    conn = sqlite3.connect("car_plates.db")
    cursor = conn.cursor()

    # Add user
    cursor.execute("INSERT INTO Users (name, address) VALUES (?, ?)", (user_name, user_address))
    user_id = cursor.lastrowid

    # Update plate status
    cursor.execute("UPDATE Plates SET status = 'sold' WHERE id = ?", (plate_id,))

    # Add sale record
    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO Sales (plate_id, user_id, date) VALUES (?, ?, ?)", (plate_id, user_id, sale_date))

    conn.commit()
    conn.close()

# View sales history
def view_sales_history():
    conn = sqlite3.connect("car_plates.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT Plates.plate, Users.name, Users.address, Sales.date
    FROM Sales
    JOIN Plates ON Sales.plate_id = Plates.id
    JOIN Users ON Sales.user_id = Users.id
    """)
    sales = cursor.fetchall()
    conn.close()
    return sales

# Main menu
def main_menu():
    initialize_database()
    while True:
        print("\n--- Avtomobil Raqamlari Sotish Dasturi ---")
        print("1. Yangi raqam qo'shish")
        print("2. Mavjud raqamlarni ko'rish")
        print("3. Raqamni sotish")
        print("4. Sotuvlar tarixini ko'rish")
        print("5. Chiqish")

        choice = input("Tanlang (1-5): ")

        if choice == "1":
            plate = input("Raqamni kiriting (masalan, 'AA 1234 BB'): ")
            price = float(input("Narxini kiriting: "))
            add_plate(plate, price)
            print("Raqam muvaffaqiyatli qo'shildi!")

        elif choice == "2":
            plates = view_available_plates()
            if plates:
                print("\nMavjud raqamlar:")
                for plate in plates:
                    print(f"ID: {plate[0]}, Raqam: {plate[1]}, Narx: {plate[2]}")
            else:
                print("Hozirda sotuvda raqamlar yo'q.")

        elif choice == "3":
            plates = view_available_plates()
            if plates:
                print("\nMavjud raqamlar:")
                for plate in plates:
                    print(f"ID: {plate[0]}, Raqam: {plate[1]}, Narx: {plate[2]}")

                plate_id = int(input("Sotiladigan raqam ID sini kiriting: "))
                user_name = input("Xaridorning ismini kiriting: ")
                user_address = input("Xaridorning manzilini kiriting: ")
                sell_plate(plate_id, user_name, user_address)
                print("Raqam muvaffaqiyatli sotildi!")
            else:
                print("Hozirda sotuvda raqamlar yo'q.")

        elif choice == "4":
            sales = view_sales_history()
            if sales:
                print("\nSotuvlar tarixi:")
                for sale in sales:
                    print(f"Raqam: {sale[0]}, Xaridor: {sale[1]}, Manzil: {sale[2]}, Sana: {sale[3]}")
            else:
                print("Hozircha sotuvlar yo'q.")

        elif choice == "5":
            print("Dastur tugatildi.")
            break

        else:
            print("Noto'g'ri tanlov, qayta urinib ko'ring.")

if __name__ == "__main__":
    main_menu()
