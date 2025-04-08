SELECT 
    d.forename || ' ' || d.surname || ' (' || d.number || ')' AS driver_name,
    p.lap,
    p.duration,
    r.name AS race_name,
    r.year AS race_year
FROM pitstops p
JOIN drivers d ON p.driverId = d.driverId
JOIN races r ON p.raceId = r.raceId
WHERE p.duration = (
    SELECT MIN(duration)
    FROM pitstops
    WHERE duration IS NOT NULL
)
ORDER BY r.year, r.name;
