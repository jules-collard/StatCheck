CREATE MATERIALIZED VIEW IF NOT EXISTS skater_stats AS
    WITH totals AS (
        SELECT
            games."season",
            games."gameType",
            skater_appearances."playerID",
            array_agg(DISTINCT (skater_appearances."teamID")) AS "teams",
            count(skater_appearances."gameID") AS "gamesPlayed",
            sum(skater_appearances."goals") AS "goals",
            sum(skater_appearances."assists") AS "assists",
            sum(skater_appearances."plusMinus") AS "plusMinus",
            sum(skater_appearances."pim") AS "penaltyMinutes",
            sum(skater_appearances."hits") AS "hits",
            sum(skater_appearances."sog") AS "sog",
            sum(skater_appearances."blocks") AS "blocks",
            sum(skater_appearances."toiSeconds")::NUMERIC / NULLIF(count(skater_appearances."gameID"), 0) AS "avgTOI"
        FROM skater_appearances
        LEFT JOIN games ON skater_appearances."gameID" = games."id"
        GROUP BY games."season", games."gameType", skater_appearances."playerID"
    ), shooting AS (
        SELECT
            games."season",
            games."gameType",
            COALESCE(events."shootingPlayerID", events."scoringPlayerID") AS "playerID",
            COALESCE(SUM("xg"), 0) AS "xg",
            SUM(CASE WHEN "typeCode" = 505 THEN 1 ELSE 0 END) AS "xgGoals",
            COUNT(events."eventID") AS "fenwick"
        FROM events
        LEFT JOIN games ON events."gameID" = games.id
        WHERE events."xg" IS NOT NULL
        GROUP BY games."season", games."gameType", "playerID"
    ), onice AS (
        SELECT
            games."season",
            games."gameType",
            split_shifts."playerID",
            sum("goalsFor")::NUMERIC / NULLIF(sum("sogFor"), 0)::NUMERIC AS "onIceShootingPct",
            sum("fenwickFor") AS "fenwickFor",
            sum("fenwickAgainst") AS "fenwickAgainst",
            sum("corsiFor") AS "corsiFor",
            sum("corsiAgainst") AS "corsiAgainst",
            sum("xgFor") AS "xgFor",
            sum("xgAgainst") AS "xgAgainst",
            sum("oZoneStarts") AS "oZoneStarts",
            sum("nZoneStarts") AS "nZoneStarts",
            sum("dZoneStarts") AS "dZoneStarts"
        FROM split_shifts
        LEFT JOIN games on split_shifts."gameID" = games.id
        WHERE "attackingSkaters" = "defendingSkaters"
        GROUP BY games."season", games."gameType", "playerID"
    ), max_games AS (
        SELECT
            teams."id" AS "teamID",
            games."season",
            games."gameType",
            COUNT(games."id") AS "games"
        FROM teams
        LEFT JOIN games ON teams."id" = games."homeTeamID" OR teams."id" = games."awayTeamID"
        GROUP BY games."season", games."gameType", teams."id"
    )
    SELECT
        totals."season",
        totals."gameType",
        totals."playerID",
        players."firstName",
        players."lastName",
        players."position",
        players."isActive",
        totals."teams",
        CASE WHEN 
            (totals."gamesPlayed"::NUMERIC >= (0.3125 * max_games."games"::NUMERIC) AND totals."gameType" = 2)
            OR (totals."gamesPlayed" >= 5 AND totals."gameType" = 3) THEN TRUE ELSE FALSE END AS "qualified",
        CASE WHEN
            (totals."sog"::NUMERIC >= (1.5 * max_games."games"::NUMERIC) AND totals."gameType" = 2)
            OR (totals."sog" >= 15 AND totals."gameType" = 3) THEN TRUE ELSE FALSE END AS "shotsQualified",
        totals."gamesPlayed",
        totals."goals",
        totals."assists",
        totals."plusMinus",
        totals."penaltyMinutes",
        totals."hits",
        totals."sog",
        totals."blocks",
        totals."avgTOI",
        COALESCE(shooting."xg", 0) AS "xg",
        COALESCE(shooting."xgGoals", 0) AS "xgGoals",
        COALESCE(shooting."fenwick", 0) AS "fenwick",
        onice."onIceShootingPct",
        onice."fenwickFor",
        onice."fenwickAgainst",
        onice."corsiFor",
        onice."corsiAgainst",
        onice."xgFor",
        onice."xgAgainst",
        onice."oZoneStarts",
        onice."nZoneStarts",
        onice."dZoneStarts"
    FROM totals
    LEFT JOIN shooting ON totals."season" = shooting."season" AND totals."gameType" = shooting."gameType" AND totals."playerID" = shooting."playerID"
    LEFT JOIN onice ON totals."season" = onice."season" AND totals."gameType" = onice."gameType" AND totals."playerID" = onice."playerID"
    LEFT JOIN max_games ON totals."teams"[array_upper(totals."teams", 1)] = max_games."teamID" AND totals."season" = max_games."season" AND totals."gameType" = max_games."gameType"
    LEFT JOIN players ON totals."playerID" = players."id"
    ORDER BY totals."season" ASC;