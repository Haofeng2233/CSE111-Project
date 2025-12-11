import sqlite3
from flask import Flask, render_template, request, redirect,jsonify
from database import add_pet, del_pet, get_all_pets, get_pet_stats, get_application_stats, add_org, get_all_orgs, add_staff, get_all_staff, get_all_available_pets, get_pet_by_id, new_application, get_app_by_id, get_staff_by_id, get_apps_by_staff, get_org_name, get_mr_by_staff

app = Flask(__name__)

@app.route("/")
def menu():
    return render_template("main_menu.html")

@app.route("/adopter")
def adopter():
    return render_template("adopter.html")

@app.route("/staff")
def staff():
    return render_template("staff.html")

@app.route("/vet")
def vet():
    return render_template("vet.html")

@app.route("/browse_pets")
def browse_pets():
    pets = get_all_available_pets()
    return render_template("browse_pets.html", pets=pets)

@app.get("/pet/<pet_id>")
def pet_view(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        return "Pet not found", 404
    return render_template("pet_view.html", pet=pet)

@app.get("/apply/<pet_id>")
def apply(pet_id):
    pet = get_pet_by_id(pet_id)  
    return render_template("application.html", pet=pet)

# Submitting a new adoption application
@app.post("/submit_application")
def submit_application():
    adopter_name = request.form["adopter_name"]
    reasoning = request.form["reasoning"]
    has_existing_pets = "Yes" if "has_existing_pets" in request.form else "No"
    pet_id = request.form["pet_id"]
    pet = get_pet_by_id(pet_id)
    pet_name = pet[1]  


    app_ID = new_application(adopter_name, pet_id, reasoning, has_existing_pets)

    return f"""
    <p style='font-size:40px;'>
        Application submitted for {pet_name}!<br>
        Your application ID is: <strong>{app_ID}</strong>
        <br><br>
        <a href='/' style='font-size:40px;'>Return to menu</a>
    </p>
    """

# Viewing the pet application
@app.get("/app/<app_id>")
def app_view(app_id):

    app = get_app_by_id(app_id)

    pet = None
    staff_name = None

    if app:
        # Get pet info
        pet_id = app[3]
        pet = get_pet_by_id(pet_id)

        # Get staff info
        staff_id = app[2]
        staff = get_staff_by_id(staff_id)
        if staff:
            staff_name = staff[2]   

    return render_template("view_application.html", app=app, pet=pet, staff_name=staff_name)

@app.get("/staff/<staff_id>")
def staff_view(staff_id):
    staff = get_staff_by_id(staff_id)

    org_name = None
    if staff:
        org_id = staff[1]
        org_name = get_org_name(org_id)

    apps = get_apps_by_staff(staff_id)
    return render_template("view_staff.html", staff=staff, org_name=org_name, apps=apps)


@app.get("/staff_app/<app_id>")
def staff_app_view(app_id):
    app = get_app_by_id(app_id)
    if not app:
        return "Application not found", 404
    
    pet = get_pet_by_id(app[3])
    staff = get_staff_by_id(app[2])
    return render_template("staff_app.html", app=app, pet=pet, staff=staff)

@app.get("/vet_mr/<record_id>")
def vet_mr_view(record_id):
    conn = sqlite3.connect("tpch.sqlite")
    cur = conn.cursor()

    cur.execute("""
                SELECT record_id, pet_id, staff_id, checkup_date, treatment, vaccination_status, next_appointment
                FROM medical_record
                WHERE record_id = ?""", (record_id,))
    record = cur.fetchone()
    conn.close()

    pet = get_pet_by_id(record[1])
    staff = get_staff_by_id(record[2])

    return render_template("vet_mr.html", record=record, pet=pet, staff=staff)

@app.get("/vet/<staff_id>")
def vet_view(staff_id):
    staff = get_staff_by_id(staff_id)

    role = staff[3]
    if role.lower() != "vet":
        return f"""
                <p style='font-size:40px; color:red;'>
                    Access denied -- staff {staff_id} is not a vet.
                </p>
                <a href='/vet' style='font-size:40px;'>← Back to portal</a>
                """
    
    org_name = get_org_name(staff[1])
    records = get_mr_by_staff(staff_id)
    return render_template("view_vet.html", staff=staff, org_name=org_name, records=records)

@app.post("/search_app")
def search_app():
    app_id = request.form["app_id"].strip()
    return redirect(f"/app/{app_id}")

@app.post("/search_staff")
def search_staff():
    staff_id = request.form["staff_id"].strip()
    return redirect(f"/staff/{staff_id}")

@app.post("/search_vet")
def search_vet():
    staff_id = request.form["staff_id"].strip()
    return redirect(f"/vet/{staff_id}")

@app.post("/update_app")
def update_app():
    app_id = request.form["app_id"]
    decision_date = request.form["decision_date"]
    result = request.form["result"]
    staff_note = request.form["staff_notes"]   

    new_status = "Approved" if result == "Approve" else "Denied"

    conn = sqlite3.connect("tpch.sqlite")
    cur = conn.cursor()

    cur.execute("""
        UPDATE adoption_application
        SET status = ?, decision_date = ?, staff_notes = ?
        WHERE app_id = ?
    """, (new_status, decision_date, staff_note, app_id))

    conn.commit()
    conn.close()

    return redirect(f"/staff_app/{app_id}")



@app.post("/update_mr")
def update_mr():
    record_id = request.form["record_id"]
    checkup_date = request.form["checkup_date"]
    treatment = request.form["treatment"]
    vaccination_status = request.form["vaccination_status"]
    next_appointment = request.form["next_appointment"]

    conn = sqlite3.connect("tpch.sqlite")
    cur = conn.cursor()

    cur.execute("""
                UPDATE medical_record
                SET checkup_date = ?, treatment = ?, vaccination_status = ?, next_appointment = ?
                WHERE record_id = ?""", (checkup_date, treatment,vaccination_status,next_appointment, record_id))
    
    conn.commit()
    conn.close()

    return redirect(f"/vet_mr/{record_id}")

# STAFF VIEW PETS
@app.get("/staff_pet_view/<staff_id>")
def staff_pet(staff_id):
    pets = get_all_pets()  
    staff = get_staff_by_id(staff_id) 
    return render_template("staff_pet.html", pets=pets, staff=staff)


#STAFF DELETE PET
@app.route("/delete_pet/<pet_id>", methods=["POST"])
def delete_pet(pet_id):
    staff_id = request.args.get("staff_id")
    del_pet(pet_id)
    return redirect(f"/staff_pet_view/{staff_id}")

#STAFF ADD PET
@app.get("/add_pet/<staff_id>")
def add_pet_form(staff_id):
    staff = get_staff_by_id(staff_id)
    return render_template("staff_add_pet.html", staff=staff)

@app.post("/add_pet")
def add_pet_submit():
    name = request.form["name"]
    species = request.form["species"]
    breed = request.form["breed"]
    age = request.form["age"]
    gender = request.form["gender"]
    org_id = request.form["org"]   # from form
    staff_id = request.form["staff_id"]

    add_pet(name, species, breed, age, gender, org_id)

    return redirect(f"/staff_pet_view/{staff_id}")



# ADMIN
@app.route("/admin")
def admin_page():
    return render_template("admin.html")

@app.route("/manage_staff")
def manage_staff():
    staffs = get_all_staff()
    return render_template("manage_staff.html", staffs=staffs)

@app.route("/new_staff", methods=["GET", "POST"])
def new_staff():
    if request.method == "POST":
        staff_name = request.form["staff_name"]
        org_id = request.form["org_id"]
        staff_role = request.form["staff_role"]
        staff_phone = request.form["staff_phone"]
        staff_email = request.form["staff_email"]

        add_staff(staff_name, org_id, staff_role, staff_phone, staff_email)

        return f"""
        <p style='font-size:40px;'>
            Staff member <strong>{staff_name}</strong> added!<br><br>
            <a href='/admin' style='font-size:40px;'>Back to Admin</a>
        </p>
        """

    # GET request → show form
    return render_template("new_staff.html")


# ADMIN ORGANIZATIONS
@app.route("/orgs")
def view_orgs():
    orgs = get_all_orgs()
    return render_template("organizations.html", orgs=orgs)

@app.route("/new_org", methods=["GET", "POST"])
def new_org():
    if request.method == "POST":
        org_name = request.form["org_name"]
        org_phone = request.form["org_phone"]
        org_email = request.form["org_email"]
        org_address = request.form["org_address"]

        add_org(org_name, org_phone, org_email, org_address)

        return f"""
        <p style='font-size:40px;'>
            Organization <strong>{org_name}</strong> added!<br><br>
            <a href='/admin' style='font-size:40px;'>Back to Admin</a>
        </p>
        """

    return render_template("organizations_new.html")

# ADMIN STATS
@app.route("/view_statistics")
def view_stats():
    app_stats = get_application_stats()
    pet_stats = get_pet_stats()
    return render_template("stats.html", stats=app_stats, pet_stats=pet_stats)



if __name__ == "__main__":
    app.run()