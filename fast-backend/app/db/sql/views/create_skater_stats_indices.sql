CREATE INDEX IF NOT EXISTS skater_index ON skater_stats ("playerID");
CREATE INDEX IF NOT EXISTS skater_season_index ON skater_stats ("season");
CREATE INDEX IF NOT EXISTS skater_game_index ON skater_stats ("gameType");