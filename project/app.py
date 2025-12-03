from flask import Flask, render_template, request, redirect
from database import get_all_pets, get_all_available_pets, get_pet_by_id, new_application, get_app_by_id, get_staff_by_id

app = Flask(__name__)

@app.route("/")
def menu():
    return render_template("main_menu.html")

@app.route("/adopter")
def adopter():
    return render_template("adopter.html")

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




@app.post("/search_app")
def search_app():
    app_id = request.form["app_id"].strip()
    return redirect(f"/app/{app_id}")



if __name__ == "__main__":
    app.run()