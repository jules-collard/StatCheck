WITH SeasonGames AS (
    SELECT "playerID", "season", "teamID", "gameID", "gameType" FROM "player_games"
    LEFT JOIN "games" ON "games"."id"="player_games"."gameID"
    WHERE player_games."playerID" == :playerID AND games."gameType" == :gameType
    ORDER BY "gameID" ASC
)
SELECT
    "SeasonGames"."playerID",
    "SeasonGames".season,
    "SeasonGames"."teamID",
    sum("goalie_appearances"."played") AS "gamesPlayed",
    sum("goalie_appearances"."starter") AS "gamesStarted",
    sum(CASE WHEN "goalie_appearances"."decision" == 'W' THEN 1 ELSE 0 END) AS "wins",
    sum(CASE WHEN "goalie_appearances"."decision" == "L" THEN 1 ELSE 0 END) AS "losses",
    (sum("goalie_appearances"."shotsAgainst") - sum("goalie_appearances"."saves")) * 3600.0 / sum("goalie_appearances"."toiSeconds") AS "goalsAgainstAvg",
    sum("goalie_appearances"."saves") * 1.0 / sum("goalie_appearances"."shotsAgainst") AS "savePct",
    sum("goalie_appearances"."evenStrengthSaves") * 1.0 / sum("goalie_appearances"."evenStrengthShotsAgainst") AS "evenStrengthSavePct",
    sum("goalie_appearances"."powerPlaySaves") * 1.0 / sum("goalie_appearances"."powerPlayShotsAgainst") AS "powerPlaySavePct"
FROM "goalie_appearances"
LEFT JOIN "SeasonGames" ON goalie_appearances."gameID" == "SeasonGames"."gameID" AND goalie_appearances."playerID" == "SeasonGames"."playerID"
WHERE "goalie_appearances"."playerID" == :playerID AND "SeasonGames"."gameType" == :gameType
GROUP BY "SeasonGames"."season", "SeasonGames"."teamID";