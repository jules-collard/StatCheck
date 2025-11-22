CREATE MATERIALIZED VIEW IF NOT EXISTS goalie_stats AS
    WITH totals AS (
        SELECT
            games."season",
            games."gameType",
            goalie_appearances."playerID",
            array_agg(DISTINCT goalie_appearances."teamID") AS "teams",
            sum(goalie_appearances."played"::INT) AS "gamesPlayed",
            sum(goalie_appearances."starter"::INT) AS "gamesStarted",
            sum(CASE WHEN goalie_appearances."decision" = 'W' THEN 1 ELSE 0 END) AS "wins",
            sum(CASE WHEN goalie_appearances."decision" = 'L' THEN 1 ELSE 0 END) AS "losses",
            sum(goalie_appearances."shotsAgainst") - sum(goalie_appearances."saves") AS "goalsAgainst",
            (sum(goalie_appearances."shotsAgainst") - sum(goalie_appearances."saves"))::NUMERIC * 3600 / sum(goalie_appearances."toiSeconds")::NUMERIC AS "goalsAgainstAvg",
            sum(goalie_appearances."saves")::NUMERIC / NULLIF(sum(goalie_appearances."shotsAgainst"), 0)::NUMERIC AS "savePct",
            sum(goalie_appearances."evenStrengthSaves")::NUMERIC / NULLIF(sum(goalie_appearances."evenStrengthShotsAgainst"), 0)::NUMERIC AS "evenStrengthSavePct",
            sum(goalie_appearances."powerPlaySaves")::NUMERIC / NULLIF(sum(goalie_appearances."powerPlayShotsAgainst"), 0)::NUMERIC AS "powerPlaySavePct"
        FROM goalie_appearances
        LEFT JOIN games ON goalie_appearances."gameID" = games."id"
        GROUP BY games."season", games."gameType", goalie_appearances."playerID"
    ), advanced AS (
        SELECT
            games."season",
            games."gameType",
            events."goalieInNetID",
            COALESCE(SUM(events."xg"), 0) AS "xgAgainst",
            sum(CASE WHEN events."typeCode" = 505 THEN 1 ELSE 0 END) AS "xgGoalsAgainst",
            count(events."eventID") AS "fenwickAgainst"
        FROM events
        LEFT JOIN games ON events."gameID" = games."id"
        WHERE events."xg" IS NOT NULL
        GROUP BY games."season", games."gameType", events."goalieInNetID"
    ), max_games AS (
        SELECT
            teams."id" AS "teamID",
            games."season",
            COUNT(games."id") AS "games"
        FROM teams
        LEFT JOIN games ON teams."id" = games."homeTeamID" OR teams."id" = games."awayTeamID"
        GROUP BY games."season", teams."id"
    )
    SELECT
        totals."season",
        totals."gameType",
        totals."playerID",
        players."firstName",
        players."lastName",
        players."isActive",
        totals."teams",
        CASE WHEN totals."gamesPlayed"::NUMERIC >= (0.3125 * max_games."games"::NUMERIC) THEN TRUE ELSE FALSE END AS "qualified",
        totals."gamesPlayed",
        totals."gamesStarted",
        totals."wins",
        totals."losses",
        totals."goalsAgainst",
        totals."goalsAgainstAvg",
        totals."savePct",
        totals."evenStrengthSavePct",
        totals."powerPlaySavePct",
        advanced."xgAgainst",
        advanced."xgGoalsAgainst",
        advanced."fenwickAgainst"
    FROM totals 
    LEFT JOIN advanced ON totals."season" = advanced."season" AND totals."gameType" = advanced."gameType" AND totals."playerID" = advanced."goalieInNetID"
    LEFT JOIN max_games ON totals."teams"[array_upper(totals."teams", 1)] = max_games."teamID"
    LEFT JOIN players ON totals."playerID" = players."id"
    WHERE totals."gamesPlayed" > 0;

CREATE INDEX goalie_index ON goalie_stats ("playerID");
CREATE INDEX season_index ON goalie_stats ("season");
CREATE INDEX game_index ON goalie_stats ("gameType");