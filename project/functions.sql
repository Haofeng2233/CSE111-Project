--1
-- Update application status (Approve)
-- Change from APP012 to APP011
UPDATE adoption_application
SET status = 'Approved', 
    decision_date = '2025-11-15'
WHERE app_id = 'APP011';


--2
-- Update application status (Deny) of application "APP007"
UPDATE adoption_application
SET status = 'Denied', 
    decision_date = '2025-11-15'
WHERE app_id = 'APP007';


--3
-- Updating vaccination record of pet "P003"
UPDATE medical_record
SET vaccination_status = 'Vaccinated'
WHERE pet_id = 'P003';


--4
-- Update corresponding pet availability where application "APP010" is approved
UPDATE pet
SET availability = 'Adopted'
WHERE pet_id IN (
    SELECT pet_id 
    FROM adoption_application
    WHERE app_id = 'APP010'
      AND status = 'Approved'
);
-- UPDATE VERSION
-- update all pet availability when the latest application is approved
UPDATE pet
SET availability = 'Adopted'
WHERE pet_id IN (
    SELECT pet_id
    FROM adoption_application
    WHERE (pet_id, decision_date) IN (
        SELECT pet_id, MAX(decision_date)
        FROM adoption_application
        GROUP BY pet_id
    )
    AND status = 'Approved'
);


--5
-- Update corresponding pet availability when "APP018" application is denied
-- and its pet has no approved application
-- UPDATE pet
-- SET availability = 'Available'
-- WHERE pet_id = (
--     SELECT pet_id
--     FROM adoption_application
--     WHERE app_id = 'APP018'
--     AND status = 'Denied'
-- );
UPDATE pet
SET availability = 'Available'
WHERE pet_id = (
    SELECT pet_id
    FROM adoption_application
    WHERE app_id = 'APP018'
      AND status = 'Denied'
)
AND pet_id NOT IN (
    SELECT pet_id
    FROM adoption_application
    WHERE status = 'Approved'
);
-- UPDATE VERSION
-- Update all pet availabilities when the pet's applications only have denied status
UPDATE pet
SET availability = 'Available'
WHERE pet_id IN (
    SELECT pet_id
    FROM adoption_application
    WHERE status = 'Denied'
)
AND pet_id NOT IN (
    SELECT pet_id
    FROM adoption_application
    WHERE status = 'Approved'
);


--6
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


--7
-- Insert medical record of the new pet into database
INSERT INTO medical_record (
    record_id,
    pet_id,
    staff_id,
    checkup_date,
    treatment,
    vaccination_status,
    next_appointment
) VALUES (
    'REC251',
    'P251',
    'STF002',
    '2025-04-06',
    'Health Check',
    'Vaccinated',
    '2025-07-08'
);


--8
-- Deleting a pet from database
DELETE FROM pet
WHERE pet_id = 'P251';


--9
-- Delete the medical record of pet 'P251' from database
DELETE FROM medical_record
WHERE pet_id = 'P251';


--10
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


--11
-- How many applications did each org get?
-- Only staff with adoption coordinator role 
SELECT
    org_name,
    staff_name,
    count(app_id) as total_applications
FROM organization o 
JOIN staff
    ON o.org_id = staff.org_id
JOIN adoption_application aa 
    ON staff.staff_id = aa.staff_id
GROUP BY o.org_name, staff.staff_name;


--12
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
    

--13
-- name of adopters that have existing pets
SELECT adopter_name
FROM adoption_application
WHERE has_existing_pets = 'Yes';


--14
-- number of pets over 10 yrs old of each organization
SELECT o.org_id, org_name, COUNT(pet_id)
FROM organization o
JOIN pet p ON o.org_id = p.org_id
WHERE p.age > 10
GROUP BY o.org_id;


--15
-- ID of unvaccinated pets of each organization
SELECT o.org_id, p.pet_id
FROM organization o
JOIN pet p ON o.org_id = p.org_id
JOIN medical_record mr ON p.pet_id = mr.pet_id
WHERE mr.vaccination_status = 'Not Vaccinated'
ORDER BY o.org_id, p.pet_id;


--16
-- Information of staff with "admin" role
SELECT 
    staff_id,
    org_id,
    staff_name, 
    staff_phone,
    staff_email
FROM staff
WHERE staff_role = 'admin'
ORDER BY org_id;


--17
-- number of available cats and dogs of each organization
SELECT
    o.org_id,
    SUM(CASE WHEN p.species = 'Cat' AND p.availability = 'Available' THEN 1 ELSE 0 END),
    SUM(CASE WHEN p.species = 'Dog' AND p.availability = 'Available' THEN 1 ELSE 0 END)
FROM organization o
JOIN pet p ON o.org_id = p.org_id
GROUP BY o.org_id
ORDER BY o.org_id;


--18
-- pets with multiple adoption application
SELECT pet_id, COUNT(*)
FROM adoption_application
GROUP BY pet_id
HAVING COUNT(*) > 1;


--19
-- adopters who applied for more than 1 pet
SELECT adopter_name, COUNT(*)
FROM adoption_application
GROUP BY adopter_name
HAVING COUNT(*) > 1;