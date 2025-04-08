SELECT year, COUNT(*) AS race_count
FROM races
GROUP BY year
ORDER BY year;
