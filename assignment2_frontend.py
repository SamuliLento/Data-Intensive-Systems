#This code is based on the video "Using copilot to create assignment 2"

import psycopg2

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

DATABASE_CONFIG = {
    "1": {
        "database": "dogs_db",
        "table": "dogs",
        "columns": ["name", "color"]
    },
    "2": {
        "database": "cats_db",
        "table": "cats",
        "columns": ["name", "color"]
    },
    "3": {
        "database": "pigs_db",
        "table": "pigs",
        "columns": ["name", "color"]
    }
}

def connect_to_database(db_name):
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=db_name
    )

def view_records(config):

    conn = connect_to_database(config["database"])
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM {config['table']}")

    rows = cur.fetchall()

    print("\nRecords")
    print("-" * 40)

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def insert_record(config):

    values = []

    for column in config["columns"]:
        value = input(f"Enter {column}: ")
        values.append(value)

    conn = connect_to_database(config["database"])
    cur = conn.cursor()

    placeholders = ", ".join(["%s"] * len(values))

    cur.execute(
        f"""
        INSERT INTO {config['table']}
        ({', '.join(config['columns'])})
        VALUES ({placeholders})
        """,
        values
    )

    conn.commit()

    print("Record inserted successfully")

    cur.close()
    conn.close()

def update_record(config):

    record_id = input("Enter ID to update: ")

    updates = {}

    for column in config["columns"]:
        value = input(
            f"New value for {column} (leave empty to skip): "
        )

        if value:
            updates[column] = value

    if not updates:
        print("Nothing to update.")
        return

    set_clause = ", ".join(
        [f"{key} = %s" for key in updates.keys()] 
    )

    values = list(updates.values())
    values.append(record_id)

    conn = connect_to_database(config["database"])
    cur = conn.cursor()

    cur.execute(
        f"""
        UPDATE {config['table']}
        SET {set_clause}
        WHERE id = %s
        """,
        values
    )

    conn.commit()

    print("Record updated")

    cur.close()
    conn.close()

def delete_record(config):

    record_id = input("Enter ID to delete: ")

    conn = connect_to_database(config["database"])
    cur = conn.cursor()

    cur.execute(
        f"DELETE FROM {config['table']} WHERE id = %s",
        (record_id,)
    )

    conn.commit()

    print("Record deleted.")

    cur.close()
    conn.close()

def database_menu(config):
    while True:
        print(f"""
Current database: {config['database']}

1. View records
2. Insert record
3. Update record
4. Delete record
5. Back
        """)

        choice = input("Select option: ")

        if choice == "1":
            view_records(config)
        elif choice == "2":
            insert_record(config)
        elif choice == "3":
            update_record(config)
        elif choice == "4":
            delete_record(config)
        elif choice == "5":
            break
        else:
            print("Invalid option")

def main():
    while True:
        print("""
==================================
Multi-Database PostgreSQL Frontend
==================================

1. Dogs Database
2. Cats Database
3. Pigs Database
4. Exit
        """)

        choice = input("Select database: ")

        if choice in DATABASE_CONFIG:
            database_menu(DATABASE_CONFIG[choice])
        elif choice =="4":
            print("Goodbye")
            break
        else:
            print("Invalid selection")

if __name__ == "__main__":
    main()