SELECT
    games.season,
    skater_appearances."teamID",
    coalesce(SUM(xg), 0) AS xg,
    sum(CASE WHEN "typeCode" == 505 THEN 1 ELSE 0 END) AS actualGoals,
    count(events.id) AS actualShotAttempts
FROM events
LEFT JOIN games ON events."gameID" == games.id
LEFT JOIN skater_appearances ON events."gameID" == skater_appearances."gameID" AND skater_appearances."playerID" == :playerID
WHERE
    (events."shootingPlayerID" == :playerID OR events."scoringPlayerID" == :playerID)
    AND events.xg NOT NULL
    AND games."gameType" == :gameType
GROUP BY games.season, skater_appearances."teamID"