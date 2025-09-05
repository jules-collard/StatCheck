SELECT
    games.season,
    coalesce(SUM(xg), 0) AS xgAgainst,
    sum(CASE WHEN "typeCode" == 505 THEN 1 ELSE 0 END) AS actualGoalsAgainst,
    count(events.id) AS actualShotsAgainst
FROM events
LEFT JOIN games ON events."gameID" == games.id
WHERE
    (events."goalieInNetID" == :playerID)
    AND events.xg NOT NULL
    AND events."typeCode" IN (505,506)
    AND games."gameType" == :gameType
GROUP BY games.season