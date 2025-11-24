CREATE INDEX IF NOT EXISTS goalie_index ON goalie_stats ("playerID");
CREATE INDEX IF NOT EXISTS season_index ON goalie_stats ("season");
CREATE INDEX IF NOT EXISTS game_index ON goalie_stats ("gameType");