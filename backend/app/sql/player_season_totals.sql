WITH SeasonGames AS (
    SELECT "playerID", "season", "teamID", "gameID" FROM "player_games"
    LEFT JOIN "games" ON "games"."id"="player_games"."gameID"
    WHERE player_games."playerID" == :playerID AND games."gameType" == :gameType
    ORDER BY "gameID" ASC
),
SeasonEvents AS (
    SELECT "events".*, "games"."season" FROM
    "events" LEFT JOIN "games"
    ON "events"."gameID"="games"."id"
    WHERE games."gameType" == :gameType
),
goalsTable AS (
    SELECT "scoringPlayerID", "gameID", "season", COUNT(id) AS goals FROM "SeasonEvents"
    WHERE "typeCode" == 505
        AND "periodType" != 'SO'
        AND "scoringPlayerID" == :playerID
    GROUP BY "scoringPlayerID", "season", "gameID"
),
primaryAssistsTable AS (
    SELECT "assist1PlayerID", "gameID", "season", COUNT("id") AS primaryAssists FROM "SeasonEvents"
    WHERE "assist1PlayerID" == :playerID AND "typeCode" == 505
    GROUP BY "assist1PlayerID", "season", "gameID"
),
secondaryAssistsTable AS (
    SELECT "assist2PlayerID", "gameID", "season", COUNT("id") AS secondaryAssists FROM "SeasonEvents"
    WHERE "assist2PlayerID" == :playerID AND "typeCode" == 505
    GROUP BY "assist2PlayerID", "season", "gameID"
),
hitsTable AS (
    SELECT "hittingPlayerID", "gameID", "season", COUNT("id") AS hits FROM "SeasonEvents"
    WHERE "hittingPlayerID" == :playerID AND "typeCode" == 503
    GROUP BY "hittingPlayerID", "season", "gameID"
),
shotsOnGoalTable AS (
    SELECT "shootingPlayerID", "gameID", "season", COUNT("id") AS sog FROM "SeasonEvents"
    WHERE "shootingPlayerID" == :playerID AND "typeCode" == 506
    GROUP BY "shootingPlayerID", "season", "gameID"
),
blocksTable AS (
    SELECT "blockingPlayerID", "gameID", "season", COUNT("id") AS blocks FROM "SeasonEvents"
    WHERE "blockingPlayerID" == :playerID AND "typeCode" == 508 AND
        ("reason" != 'teammate-blocked' OR "reason" IS NULL)
    GROUP BY "blockingPlayerID", "season", "gameID"
),
penaltyMinutesTable AS (
    SELECT "committedByPlayerID", "gameID", "season", sum("duration") AS penaltyMinutes FROM "SeasonEvents"
    WHERE "committedByPlayerID" == :playerID AND "typeCode" == 509
    GROUP BY "committedByPlayerID", "season", "gameID"
),
takeawaysTable AS (
    SELECT "playerID" AS "takeawayPlayerID", "gameID", "season", COUNT("id") AS takeaways FROM "SeasonEvents"
    WHERE "takeawayPlayerID" == :playerID AND "typeCode" == 525
    GROUP BY "takeawayPlayerID", "season", "gameID"
),
giveawaysTable AS (
    SELECT "playerID" AS "giveawayPlayerID", "gameID", "season", COUNT("id") AS giveaways FROM "SeasonEvents"
    WHERE  "giveawayPlayerID" == :playerID AND "typeCode" == 504
    GROUP BY "giveawayPlayerID", "season", "gameID"
)
SELECT
    "SeasonGames"."playerID" AS "playerID",
    "SeasonGames"."season" AS "season",
    "SeasonGames"."teamID" AS "teamID",
    count("SeasonGames"."gameID") AS "gamesPlayed",
    sum(coalesce("goalsTable"."goals", 0)) AS "goals",
    sum(coalesce("primaryAssistsTable"."primaryAssists", 0)) AS "primaryAssists",
    sum(coalesce("secondaryAssistsTable"."secondaryAssists", 0)) AS "secondaryAssists",
    sum(coalesce("hitsTable"."hits", 0)) AS "hits",
    sum(coalesce("shotsOnGoalTable"."sog", 0)) + coalesce("goalsTable"."goals", 0) AS "sog",
    sum(coalesce("blocksTable"."blocks", 0)) AS "blocks",
    sum(coalesce("penaltyMinutesTable"."penaltyMinutes", 0)) AS "penaltyMinutes",
    sum(coalesce("takeawaysTable"."takeaways", 0)) AS "takeaways",
    sum(coalesce("giveawaysTable"."giveaways", 0)) AS "giveaways"
FROM "SeasonGames"
LEFT JOIN "goalsTable"
ON "SeasonGames"."playerID"="goalsTable"."scoringPlayerID" AND "SeasonGames"."gameID"="goalsTable"."gameID"
LEFT JOIN "primaryAssistsTable"
ON "SeasonGames"."playerID"="primaryAssistsTable"."assist1PlayerID" AND "SeasonGames"."gameID"="primaryAssistsTable"."gameID"
LEFT JOIN "secondaryAssistsTable"
ON "SeasonGames"."playerID"="secondaryAssistsTable"."assist2PlayerID" AND "SeasonGames"."gameID"="secondaryAssistsTable"."gameID"
LEFT JOIN "hitsTable"
ON "SeasonGames"."playerID"="hitsTable"."hittingPlayerID" AND "SeasonGames"."gameID"="hitsTable"."gameID"
LEFT JOIN "shotsOnGoalTable"
ON "SeasonGames"."playerID"="shotsOnGoalTable"."shootingPlayerID" AND "SeasonGames"."gameID"="shotsOnGoalTable"."gameID"
LEFT JOIN "blocksTable"
ON "SeasonGames"."playerID"="blocksTable"."blockingPlayerID" AND "SeasonGames"."gameID"="blocksTable"."gameID"
LEFT JOIN "penaltyMinutesTable"
ON "SeasonGames"."playerID"="penaltyMinutesTable"."committedByPlayerID" AND "SeasonGames"."gameID"="penaltyMinutesTable"."gameID"
LEFT JOIN "takeawaysTable"
ON "SeasonGames"."playerID"="takeawaysTable"."takeawayPlayerID" AND "SeasonGames"."gameID"="takeawaysTable"."gameID"
LEFT JOIN "giveawaysTable"
ON "SeasonGames"."playerID"="giveawaysTable"."giveawayPlayerID" AND "SeasonGames"."gameID"="giveawaysTable"."gameID"
GROUP BY "SeasonGames"."playerID", "SeasonGames"."season", "SeasonGames"."teamID"
ORDER BY "SeasonGames"."season" ASC;