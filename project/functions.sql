-- Update application status (Approve)
UPDATE adoption_application
SET status = 'Approved', 
    decision_date = '2025-11-15'
WHERE app_id = 'APP012';

-- Update application status (Deny)
UPDATE adoption_application
SET status = 'Denied', 
    decision_date = '2025-11-15'
WHERE app_id = 'APP007';

-- Updating vaccination record 
UPDATE medical_record
SET vaccination_status = 'Vaccinated'
WHERE pet_id = 'P003';

-- Update pet availability when application is approved
UPDATE pet
SET availability = 'Adopted'
WHERE pet_id IN (
    SELECT pet_id 
    FROM adoption_application
    WHERE app_id = 'APP010'
      AND status = 'Approved'
);

-- Update pet availibility when application is denied
UPDATE pet
SET availability = 'Available'
WHERE pet_id = (
    SELECT pet_id
    FROM adoption_application
    WHERE app_id = 'APP018'
    AND status = 'Denied'
);



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

-- Selecting Application with a pet, and which staff is processing
SELECT 
    app_id,
    status,
    pet_name,
    species,
    staff_name
FROM adoption_application aa
JOIN pet p 
    ON aa.pet_id = p.pet_id
JOIN staff s 
    ON aa.staff_id = s.staff_id;

-- How many applications did each org get?
SELECT
    org_name,
    staff_name,
    count(app_id) as total_applications
FROM organization o 
JOIN staff
    ON o.orgn_id = staff.org_id
JOIN adoption_application aa 
    ON staff.staff_id = aa.staff_id
GROUP BY o.org_name, staff.staff_name;

-- Which pets are still avilible? 
SELECT
    staff_name,
    pet_name,
    species,
    breed,
    availability,
    vaccination_status
FROM staff
JOIN medical_record
    ON staff.staff_id = medical_record.staff_id
JOIN pet
    ON medical_record.pet_id = pet.pet_id
WHERE pet.availability = 'Available';
    