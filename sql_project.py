import mysql.connector
from tabulate import tabulate

# Function to connect to MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database=""   # Replace with your database name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def display_products(cursor, connection):
    print('🙏 WELCOME TO OUR STORE 🙏')
    print('**************************')
    print('*MENU                    *')
    print("*PRESS 1 FOR GROCERIES   *")
    print("*PRESS 2 FOR GADGETS     *")
    print("*PRESS 3 FOR DECORE      *")
    print("*PRESS 4 TO EXIT         *")
    print('**************************')
    
    ch = input('Enter your choice: ')
    
    if ch == '1':
        category = 'groceries'
    elif ch == '2':
        category = 'gadgets'
    elif ch == '3':
        category = 'decore'
    elif ch == '4':
        print("🙏 THANK YOU FOR VISITING & COME AGAIN 🙏")
        return
    else:
        print("Invalid choice!")
        return

    print(category.upper() + " :")
    cursor.execute(f"SELECT * FROM {category}")
    products = cursor.fetchall()
    print(tabulate(products, headers=['itemno', 'item', 'quantity', 'price'], tablefmt='psql'))

    cart(cursor, connection, category)
    process_shopping_cart(cursor)

def process_shopping_cart(cursor):
    print('\n\n' + "-" * 50)
    print('                        BILL')
    cursor.execute("SELECT * FROM CART")
    products = cursor.fetchall()
    print(tabulate(products, headers=['ITEM_NO', 'ITEM_NAME', 'QTY', 'PRICE'], tablefmt='psql'))

    total = 0
    for row in products:
        qty = int(row[2])
        price = int(row[3])
        total += qty * price

    print('\nTOTAL PRICE IS ₹', total)
    print('\n🙏 THANK YOU FOR PURCHASING 🙏')
    print("🙏 THANK YOU FOR VISITING & COME AGAIN 🙏")
    print("-" * 50)

def cart(cursor, connection, table_name):
    # Reset the cart
    cursor.execute("DROP TABLE IF EXISTS CART")
    cursor.execute("CREATE TABLE CART (ITEM_NO INT NOT NULL, ITEM_NAME VARCHAR(50), QTY INT, PRICE INT)")
    connection.commit()

    c = 1
    while True:
        itemno = input("Enter the itemno to add to your cart (0 to finish): ")
        if itemno == '0':
            break

        try:
            itemno = int(itemno)
            quantity = int(input("Enter the quantity: "))

            query = f"SELECT * FROM {table_name} WHERE itemno = %s"
            cursor.execute(query, (itemno,))
            data = cursor.fetchone()

            if not data:
                print("Item not found.")
                continue

            insert_query = "INSERT INTO CART (ITEM_NO, ITEM_NAME, QTY, PRICE) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (c, data[1], quantity, data[3]))
            connection.commit()
            c += 1

        except ValueError:
            print("Invalid input. Please enter numbers only.")

def shopping():
    connection = connect_to_database()
    if connection is None:
        return
    cursor = connection.cursor()
    display_products(cursor, connection)
    connection.close()

if __name__ == "__main__":
    shopping()
