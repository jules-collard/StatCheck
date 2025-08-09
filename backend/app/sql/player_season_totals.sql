WITH SeasonGames AS (
    SELECT "playerID", "season", count("gameID") AS "gamesPlayed" FROM "player_games"
    LEFT JOIN "games" ON "games"."id"="player_games"."gameID"
    WHERE player_games."playerID" == :playerID AND games."gameType" == :gameType
    GROUP BY "playerID", "season"
),
SeasonEvents AS (
    SELECT "events".*, "games"."season" FROM
    "events" LEFT JOIN "games"
    ON "events"."gameID"="games"."id"
    WHERE games."gameType" == :gameType
),
goalsTable AS (
    SELECT "scoringPlayerID", "season", COUNT(id) AS goals FROM "SeasonEvents"
    WHERE "typeCode" == 505
        AND "periodType" != 'SO'
        AND "scoringPlayerID" == :playerID
    GROUP BY "scoringPlayerID", "season"
),
primaryAssistsTable AS (
    SELECT "assist1PlayerID", "season", COUNT("id") AS primaryAssists FROM "SeasonEvents"
    WHERE "assist1PlayerID" == :playerID AND "typeCode" == 505
    GROUP BY "assist1PlayerID", "season"
),
secondaryAssistsTable AS (
    SELECT "assist2PlayerID", "season", COUNT("id") AS secondaryAssists FROM "SeasonEvents"
    WHERE "assist2PlayerID" == :playerID AND "typeCode" == 505
    GROUP BY "assist2PlayerID", "season"
),
hitsTable AS (
    SELECT "hittingPlayerID", "season", COUNT("id") AS hits FROM "SeasonEvents"
    WHERE "hittingPlayerID" == :playerID AND "typeCode" == 503
    GROUP BY "hittingPlayerID", "season"
),
shotsOnGoalTable AS (
    SELECT "shootingPlayerID", "season", COUNT("id") AS sog FROM "SeasonEvents"
    WHERE "shootingPlayerID" == :playerID AND "typeCode" == 506
    GROUP BY "shootingPlayerID", "season"
),
blocksTable AS (
    SELECT "blockingPlayerID", "season", COUNT("id") AS blocks FROM "SeasonEvents"
    WHERE "blockingPlayerID" == :playerID AND "typeCode" == 508 AND
        ("reason" != 'teammate-blocked' OR "reason" IS NULL)
    GROUP BY "blockingPlayerID", "season"
),
penaltyMinutesTable AS (
    SELECT "committedByPlayerID", "season", sum("duration") AS penaltyMinutes FROM "SeasonEvents"
    WHERE "committedByPlayerID" == :playerID AND "typeCode" == 509
    GROUP BY "committedByPlayerID", "season"
),
takeawaysTable AS (
    SELECT "playerID" AS "takeawayPlayerID", "season", COUNT("id") AS takeaways FROM "SeasonEvents"
    WHERE "takeawayPlayerID" == :playerID AND "typeCode" == 525
    GROUP BY "takeawayPlayerID", "season"
),
giveawaysTable AS (
    SELECT "playerID" AS "giveawayPlayerID", "season", COUNT("id") AS giveaways FROM "SeasonEvents"
    WHERE  "giveawayPlayerID" == :playerID AND "typeCode" == 504
    GROUP BY "giveawayPlayerID", "season"
)
SELECT
    "SeasonGames"."playerID" AS "playerID",
    "SeasonGames"."season" AS "season",
    "SeasonGames"."gamesPlayed" AS "gamesPlayed",
    coalesce("goalsTable"."goals", 0) AS "goals",
    coalesce("primaryAssistsTable"."primaryAssists", 0) AS "primaryAssists",
    coalesce("secondaryAssistsTable"."secondaryAssists", 0) AS "secondaryAssists",
    coalesce("hitsTable"."hits", 0) AS "hits",
    coalesce("shotsOnGoalTable"."sog", 0) + "goals" AS "sog",
    coalesce("blocksTable"."blocks", 0) AS "blocks",
    coalesce("penaltyMinutesTable"."penaltyMinutes", 0) AS "penaltyMinutes",
    coalesce("takeawaysTable"."takeaways", 0) AS "takeaways",
    coalesce("giveawaysTable"."giveaways", 0) AS "giveaways"
FROM "SeasonGames"
LEFT JOIN "goalsTable"
ON "SeasonGames"."playerID"="goalsTable"."scoringPlayerID" AND "SeasonGames"."season"="goalsTable"."season"
LEFT JOIN "primaryAssistsTable"
ON "SeasonGames"."playerID"="primaryAssistsTable"."assist1PlayerID" AND "SeasonGames"."season"="primaryAssistsTable"."season"
LEFT JOIN "secondaryAssistsTable"
ON "SeasonGames"."playerID"="secondaryAssistsTable"."assist2PlayerID" AND "SeasonGames"."season"="secondaryAssistsTable"."season"
LEFT JOIN "hitsTable"
ON "SeasonGames"."playerID"="hitsTable"."hittingPlayerID" AND "SeasonGames"."season"="hitsTable"."season"
LEFT JOIN "shotsOnGoalTable"
ON "SeasonGames"."playerID"="shotsOnGoalTable"."shootingPlayerID" AND "SeasonGames"."season"="shotsOnGoalTable"."season"
LEFT JOIN "blocksTable"
ON "SeasonGames"."playerID"="blocksTable"."blockingPlayerID" AND "SeasonGames"."season"="blocksTable"."season"
LEFT JOIN "penaltyMinutesTable"
ON "SeasonGames"."playerID"="penaltyMinutesTable"."committedByPlayerID" AND "SeasonGames"."season"="penaltyMinutesTable"."season"
LEFT JOIN "takeawaysTable"
ON "SeasonGames"."playerID"="takeawaysTable"."takeawayPlayerID" AND "SeasonGames"."season"="takeawaysTable"."season"
LEFT JOIN "giveawaysTable"
ON "SeasonGames"."playerID"="giveawaysTable"."giveawayPlayerID" AND "SeasonGames"."season"="giveawaysTable"."season"
ORDER BY "SeasonGames"."season" ASC;