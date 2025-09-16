SELECT
    games.season,
    group_concat(DISTINCT skater_appearances."teamID") AS "teams",
    coalesce(SUM(xg), 0) AS xg,
    sum(CASE WHEN "typeCode" == 505 THEN 1 ELSE 0 END) AS xgGoals,
    count(events.id) AS fenwick
FROM events
LEFT JOIN games ON events."gameID" == games.id
LEFT JOIN skater_appearances ON events."gameID" == skater_appearances."gameID" AND skater_appearances."playerID" == :playerID
WHERE
    (events."shootingPlayerID" == :playerID OR events."scoringPlayerID" == :playerID)
    AND events.xg NOT NULL
    AND games."gameType" == :gameType
GROUP BY games.season
ORDER BY games.season;