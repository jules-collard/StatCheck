SELECT
    games.season,
    group_concat(DISTINCT goalie_appearances."teamID") AS "teams",
    coalesce(SUM(xg), 0) AS xgAgainst,
    sum(CASE WHEN "typeCode" == 505 THEN 1 ELSE 0 END) AS xgGoalsAgainst,
    count(events.id) AS fenwickAgainst
FROM events
LEFT JOIN games ON events."gameID" == games.id
LEFT JOIN goalie_appearances ON events."gameID" == goalie_appearances."gameID" AND goalie_appearances."playerID" == :playerID
WHERE
    (events."goalieInNetID" == :playerID)
    AND events.xg NOT NULL
    AND games."gameType" == :gameType
GROUP BY games.season
ORDER BY games.season;