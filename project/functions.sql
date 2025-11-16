-- Update application status (Approve)
UPDATE adoption_application
SET status = 'Approved', 
    decision_date = '2025-11-15'
WHERE app_id = 'APP002';

-- Update application status (Deny)
UPDATE adoption_application
SET status = 'Denied', 
    decision_date = '2025-11-15'
WHERE app_id = 'APP004';

-- Updating vaccination record 
UPDATE medical_record
SET vaccination_status = 'Vaccinated'
WHERE pet_id = 'P003';

-- Update pet availibility
UPDATE pet 
SET availability='Adopted' 
WHERE pet_id='PET001';

-- Example new pet into database
INSERT INTO pet (
    pet_id,
    pet_name,
    species,
    breed,
    age,
    gender,
    availability,
    org_id
) VALUES (
    'P251',
    'Seasame',
    'Dog',
    'Pug',
    4,
    'Male',
    'Available',
    'ORG001'
);

-- Deleting a pet from database
DELETE FROM pet
WHERE pet_id = 'P251';
