import sqlite3
import random
DB = "tpch.sqlite"


def connect():
    return sqlite3.connect(DB)


def get_all_pets():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM pet")
    pets = cur.fetchall()

    conn.close()
    return pets

def get_all_available_pets():
    conn = connect()
    cur = conn.cursor()

    cur.execute('''
                SELECT * FROM pet
                WHERE availability = "Available"
                ''')
    pets = cur.fetchall()

    conn.close()
    return pets

def get_pet_by_id(pet_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pet WHERE pet_id = ?", (pet_id,))
    pet = cur.fetchone()
    conn.close()
    return pet

def new_application(adopter_name, pet_id, reasoning, has_pets):
    conn = connect()
    cur = conn.cursor()

    # create new APP ID
    cur.execute("SELECT app_id FROM adoption_application ORDER BY app_id DESC LIMIT 1")
    row = cur.fetchone()

    if row is None:
        next_num = 1
    else:
        last_id = row[0]
        last_num = int(last_id.replace("APP", ""))
        next_num = last_num + 1

    app_id = f"APP{next_num:03d}"

    # create random staff_id
    staff_num = random.randint(1, 109)
    staff_id = f"STF{staff_num:03d}"

    # insert into DB
    cur.execute("""
        INSERT INTO adoption_application 
        (app_id, adopter_name, staff_id, pet_id, status, reasoning, has_existing_pets, staff_notes, decision_date)
        VALUES (?, ?, ?, ?, 'Under Review', ?, ?, 'N/A', 'N/A')
    """, (app_id, adopter_name, staff_id, pet_id, reasoning, has_pets))

    conn.commit()
    conn.close()
    return app_id


def get_app_by_id(app_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM adoption_application WHERE app_id = ?", (app_id,))
    app = cur.fetchone()
    conn.close()
    return app

def get_staff_by_id(staff_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM staff WHERE staff_id = ?", (staff_id,))
    staff = cur.fetchone()
    conn.close()
    return staff


