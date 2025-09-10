SELECT
    games.season,
    "teamID",
    1.0 * sum("goalsFor") / sum("sogFor") AS onIceShootingPct,
    sum("fenwickFor") AS fenwickFor,
    sum("fenwickAgainst") AS fenwickAgainst,
    sum("corsiFor") AS corsiFor,
    sum("corsiAgainst") AS corsiAgainst,
    sum("xgFor") AS xgFor,
    sum("xgAgainst") AS xgAgainst,
    sum("oZoneStarts") AS oZoneStarts,
    sum("nZoneStarts") AS nZoneStarts,
    sum("dZoneStarts") AS dZoneStarts
FROM split_shifts
LEFT JOIN games on split_shifts."gameID" == games.id
WHERE
    games."gameType" == :gameType
    AND split_shifts."playerID" == :playerID
    AND "attackingSkaters" == "defendingSkaters"
GROUP BY games.season, split_shifts."teamID"
ORDER BY games.season, split_shifts."teamID";