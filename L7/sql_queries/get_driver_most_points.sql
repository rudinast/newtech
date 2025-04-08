SELECT 
    ds.driverId,
    d.forename || ' ' || d.surname AS driver_name,
    r.name AS race_name,
    r.year AS race_year,
    ds.points
FROM driver_standings ds
JOIN drivers d ON ds.driverId = d.driverId
JOIN races r ON ds.raceId = r.raceId
WHERE ds.points = (
    SELECT MAX(points) FROM driver_standings
)
ORDER BY r.year, r.name, driver_name;
