SELECT 
    results.resultId,
    results.raceId,
    races.name AS race_name,
    drivers.forename || ' ' || drivers.surname AS driver_name,
    constructors.name AS constructor_name,
    results.position,
    results.points,
    races.year
FROM results
JOIN drivers ON results.driverId = drivers.driverId
JOIN constructors ON results.constructorId = constructors.constructorId
JOIN races ON results.raceId = races.raceId
WHERE races.year = 2010
ORDER BY races.name, results.position;
