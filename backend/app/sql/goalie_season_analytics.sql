SELECT games.season, coalesce(SUM(xg), 0) AS xg FROM events
LEFT JOIN games ON events."gameID" == games.id
WHERE events."goalieInNetID" == :playerID AND events."typeCode" IN (505, 506) AND games."gameType" == :gameType
GROUP BY games.season