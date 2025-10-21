CREATE TABLE organization (
    orgn_id CHAR(6) NOT NULL,
    org_name VARCHAR(100) NOT NULL,
    org_phone CHAR(15),
    org_email VARCHAR(100),
    org_address VARCHAR(150)
);


CREATE TABLE staff (
    staff_id CHAR(6) NOT NULL,
    org_id CHAR(6) NOT NULL,
    staff_name VARCHAR(100) NOT NULL,
    staff_role VARCHAR(50) NOT NULL,
    staff_phone CHAR(15),
    staff_email VARCHAR(100)
);


CREATE TABLE pet (
    pet_id CHAR(6) NOT NULL,
    pet_name VARCHAR(50) NOT NULL,
    species VARCHAR(20) NOT NULL,
    breed VARCHAR(50),
    age DECIMAL(2,0),
    gender CHAR(10),
    availability VARCHAR(20),
    org_id CHAR(6) NOT NULL
);


CREATE TABLE adopter (
    adopter_name VARCHAR(100) NOT NULL,
    adopter_phone CHAR(15),
    adopter_email VARCHAR(100),
    adopter_address VARCHAR(150)
);


CREATE TABLE medical_record (
    record_id CHAR(7) NOT NULL,
    pet_id CHAR(6) NOT NULL,
    staff_id CHAR(6) NOT NULL,
    checkup_date DATE NOT NULL,
    treatment VARCHAR(100),
    vaccination_status VARCHAR(20),
    next_appointment DATE
);


CREATE TABLE adoption_application (
    app_id CHAR(7) NOT NULL,
    adopter_name VARCHAR(100) NOT NULL,
    staff_id CHAR(6) NOT NULL,
    pet_id CHAR(6) NOT NULL,
    status VARCHAR(20) NOT NULL,
    reasoning VARCHAR(255),
    has_existing_pets CHAR(3),
    staff_notes VARCHAR(255),
    decision_date DATE
);