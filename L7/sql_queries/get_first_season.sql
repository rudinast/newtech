SELECT * 
FROM seasons
WHERE year = (SELECT MIN(year) FROM seasons);
