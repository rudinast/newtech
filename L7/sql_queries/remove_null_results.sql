DELETE FROM results
WHERE 
    raceId IS NULL OR
    driverId IS NULL OR
    constructorId IS NULL OR
    number IS NULL OR
    grid IS NULL OR
    position IS NULL OR
    positionText IS NULL OR
    positionOrder IS NULL OR
    points IS NULL OR
    laps IS NULL OR
    time IS NULL OR
    milliseconds IS NULL OR
    fastestLap IS NULL OR
    rank IS NULL OR
    fastestLapTime IS NULL OR
    fastestLapSpeed IS NULL OR
    statusId IS NULL;