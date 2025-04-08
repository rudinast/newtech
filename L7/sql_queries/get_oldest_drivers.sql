SELECT * FROM drivers
WHERE 
    substr(dob, 7, 4) || '-' || substr(dob, 4, 2) || '-' || substr(dob, 1, 2) =
    (
        SELECT 
            MIN(substr(dob, 7, 4) || '-' || substr(dob, 4, 2) || '-' || substr(dob, 1, 2))
        FROM drivers
    );

