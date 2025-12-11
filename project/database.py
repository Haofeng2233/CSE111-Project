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

def get_apps_by_staff(staff_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
                SELECT app_id, status
                FROM adoption_application
                WHERE staff_id = ?""", (staff_id,))
    apps = cur.fetchall()
    conn.close()
    return apps

def get_mr_by_staff(staff_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
                SELECT record_id, checkup_date
                FROM medical_record
                WHERE staff_id = ?""", (staff_id,))
    records = cur.fetchall()
    conn.close()
    return records

def get_org_name(org_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT org_name FROM organization WHERE org_id = ?", (org_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# ADMIN FUNCTIONS
def get_all_staff():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM staff")
    staffs = cur.fetchall()

    conn.close()
    return staffs

def add_staff(staff_name, org_ID, staff_role, staff_phone, staff_email):
    conn = connect()
    cur = conn.cursor()
    
    # create new staff id
    cur.execute("SELECT staff_id FROM staff ORDER BY staff_id DESC LIMIT 1")
    row = cur.fetchone()

    if row is None:
        next_num = 1
    else:
        last_id = row[0]
        last_num = int(last_id.replace("STF", ""))
        next_num = last_num + 1

    new_staff = f"STF{next_num:03d}"

    # insert into DB
    cur.execute("""
                INSERT INTO staff
                (staff_id, org_id, staff_name, staff_role, staff_phone, staff_email)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (new_staff, org_ID, staff_name, staff_role, staff_phone, staff_email))
    
    conn.commit()
    conn.close()
    return new_staff


# ADMIN ORGS
def get_all_orgs():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM organization")
    orgs = cur.fetchall()

    conn.close()
    return orgs

def add_org(org_name, phone, email, address):
    conn = connect()
    cur = conn.cursor()
    
    # create new org id
    cur.execute("SELECT org_id FROM organization ORDER BY org_id DESC LIMIT 1")
    row = cur.fetchone()

    if row is None:
        next_num = 1
    else:
        last_id = row[0]
        last_num = int(last_id.replace("ORG", ""))
        next_num = last_num + 1

    new_org = f"ORG{next_num:03d}"

    # insert into DB
    cur.execute("""
                INSERT INTO organization
                (org_id, org_name, org_phone, org_email, org_address)
                VALUES (?, ?, ?, ?, ?)
                """, (new_org, org_name, phone, email, address))
    
    conn.commit()
    conn.close()
    return new_org

# admin statistics 1 - query 11 in functions.sql
def get_application_stats():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            o.org_name,
            s.staff_name,
            COUNT(aa.app_id) AS total_applications,
            SUM(
                CASE 
                    WHEN aa.status IN ('Approved', 'Denied') THEN 1
                    ELSE 0
                END
            ) AS processed_applications
        FROM organization o
        JOIN staff s
            ON o.org_id = s.org_id
        JOIN adoption_application aa
            ON s.staff_id = aa.staff_id
        WHERE s.staff_role = 'adoption coordinator'
        GROUP BY o.org_name, s.staff_name
    """)

    results = cur.fetchall()
    conn.close()
    return results

# admin stats 2 
def get_pet_stats():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            o.org_name,
            COUNT(p.pet_id) AS total_pets,
            SUM(CASE WHEN p.species = 'Dog' THEN 1 ELSE 0 END) AS total_dogs,
            SUM(CASE WHEN p.species = 'Cat' THEN 1 ELSE 0 END) AS total_cats,
            SUM(CASE WHEN p.species = 'Dog' AND m.vaccination_status = 'Vaccinated' THEN 1 ELSE 0 END) AS vaccinated_dogs,
            SUM(CASE WHEN p.species = 'Cat' AND m.vaccination_status = 'Vaccinated' THEN 1 ELSE 0 END) AS vaccinated_cats
        FROM organization o
        JOIN pet p ON o.org_id = p.org_id
        LEFT JOIN medical_record m ON p.pet_id = m.pet_id
        GROUP BY o.org_name
    """)

    results = cur.fetchall()
    conn.close()
    return results

