WITH home_games AS (
    SELECT
        "homeTeamID",
        count(id) AS homeGames
    FROM games
    WHERE "gameType" == :gameType AND "season" == :season
    GROUP BY "homeTeamID"
),
away_games AS (
    SELECT
        "awayTeamID",
        count(id) AS awayGames
    FROM games
    WHERE "gameType" == :gameType AND "season" == :season
    GROUP BY "awayTeamID"
),
team_games AS (
    SELECT
        home_games."homeTeamID" AS "teamID",
        coalesce(homeGames, 0) + coalesce(awayGames, 0) AS totalGames
    FROM home_games
    FULL JOIN away_games ON home_games."homeTeamID" == away_games."awayTeamID"
),
advanced AS (
    SELECT
        "goalieInNetID",
        coalesce(sum(xg), 0) AS xgAgainst,
        sum(CASE WHEN "typeCode" == 505 THEN 1 ELSE 0 END) AS xgGoalsAgainst,
        count(*) AS fenwickAgainst
    FROM events
    LEFT JOIN games ON events."gameID" == games.id
    WHERE
        events.xg NOT NULL
        AND games."gameType" == :gameType
        AND games.season == :season
    GROUP BY "goalieInNetID"
),
leaderboard AS (
    SELECT
        goalie_appearances."playerID",
        players."firstName" || ' ' || players."lastName" AS "fullName",
        players."isActive",
        CASE WHEN sum("goalie_appearances"."played") >= 0.3125 * "team_games"."totalGames" THEN 1 ELSE 0 END AS "qualified",
        group_concat(DISTINCT "goalie_appearances"."teamID") AS "teams",
        sum("goalie_appearances"."played") AS "gamesPlayed",
        sum("goalie_appearances"."starter") AS "gamesStarted",
        sum(CASE WHEN "goalie_appearances"."decision" == 'W' THEN 1 ELSE 0 END) AS "wins",
        sum(CASE WHEN "goalie_appearances"."decision" == "L" THEN 1 ELSE 0 END) AS "losses",
        sum(goalie_appearances."shotsAgainst") - sum(goalie_appearances."saves") AS "goalsAgainst",
        (sum("goalie_appearances"."shotsAgainst") - sum("goalie_appearances"."saves")) * 3600.0 / sum("goalie_appearances"."toiSeconds") AS "goalsAgainstAvg",
        sum("goalie_appearances"."saves") * 1.0 / sum("goalie_appearances"."shotsAgainst") AS "savePct",
        sum("goalie_appearances"."evenStrengthSaves") * 1.0 / sum("goalie_appearances"."evenStrengthShotsAgainst") AS "evenStrengthSavePct",
        sum("goalie_appearances"."powerPlaySaves") * 1.0 / sum("goalie_appearances"."powerPlayShotsAgainst") AS "powerPlaySavePct",
        advanced.fenwickAgainst,
        advanced.xgAgainst,
        advanced.xgGoalsAgainst
    FROM "goalie_appearances"
    LEFT JOIN "games" ON goalie_appearances."gameID" == "games"."id"
    LEFT JOIN "players" ON goalie_appearances."playerID" == "players"."id"
    LEFT JOIN "team_games" ON players."currentTeamID" == team_games."teamID"
    LEFT JOIN "advanced" ON goalie_appearances."playerID" == advanced."goalieInNetID"
    WHERE "games".season == :season AND "games"."gameType" == :gameType
    GROUP BY goalie_appearances."playerID"
    ORDER BY gamesStarted DESC
)
SELECT * FROM leaderboard WHERE gamesPlayed > 0;