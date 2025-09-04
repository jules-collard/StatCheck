SELECT games.season, coalesce(SUM(xg), 0) AS xg FROM events
LEFT JOIN games ON events."gameID" == games.id
WHERE (:playerID == events."shootingPlayerID" OR :playerID == events."scoringPlayerID") AND games."gameType" == :gameType
GROUP BY games.season