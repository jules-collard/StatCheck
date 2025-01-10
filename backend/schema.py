import sqlite3
import os

def create_db_with_schema(db_path, *sql_statements):
    try:
        with sqlite3.connect(db_path) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

            for statement in sql_statements:
                conn.execute(statement)

            conn.commit()

    except sqlite3.OperationalError as e:
        print("Failed:", e)


def main():
    db_path = os.path.join(__file__, "..", "statcheck.db")

    create_teams_table_sql = '''
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER,
        fullName TEXT NOT NULL,
        teamCommonName TEXT NOT NULL,
        teamPlaceName TEXT NOT NULL,
        metaDateTime TEXT NOT NULL,
        PRIMARY KEY("id")
    );
    '''

    create_players_table_sql = '''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER,
        isActive INTEGER,
        currentTeamID INTEGER,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        sweaterNumber INTEGER NOT NULL,
        position TEXT NOT NULL,
        headshot TEXT,
        heroImage TEXT,
        heightInInches INTEGER,
        heightInCentimeters INTEGER,
        weightInPounds INTEGER,
        weightInKilograms INTEGER,
        birthDate TEXT,
        birthCity TEXT,
        birthCountry TEXT,
        shootsCatches TEXT NOT NULL,
        draftYear INTEGER,
        draftTeamAbbrev TEXT,
        draftRound INTEGER,
        draftPickInRound INTEGER,
        draftOverallPick INTEGER,
        inHHOF INTEGER,
        metaDateTime TEXT NOT NULL,
        PRIMARY KEY("id"),
        FOREIGN KEY("id") REFERENCES "teams"("id"),
        CHECK (isActive IN (0,1)),
        CHECK (shootsCatches IN ("L", "R")),
        CHECK (inHHOF IN (0,1))
    );
    '''

    create_game_types_table_sql = '''
    CREATE TABLE IF NOT EXISTS game_types (
        typeCode INTEGER,
        typeDescKey TEXT NOT NULL,
        PRIMARY KEY("typeCode")
    );
    '''

    create_games_table_sql = '''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER,
        season INTEGER NOT NULL,
        gameType INTEGER NOT NULL,
        neutralSite INTEGER,
        startTimeUTC TEXT,
        venueUTCOffset INTEGER,
        gameState TEXT NOT NULL,
        gameScheduleState TEXT,
        defaultVenue TEXT,
        awayTeamID INTEGER,
        awayTeamScore INTEGER NOT NULL,
        homeTeamID INTEGER,
        homeTeamScore INTEGER NOT NULL,
        maxRegulationPeriod INTEGER NOT NULL,
        lastPeriodType TEXT NOT NULL,
        winningGoalieID INTEGER,
        winningGoalscorerID,
        metaDateTime TEXT NOT NULL,
        PRIMARY KEY("id"),
        FOREIGN KEY("gameType") REFERENCES "game_types"("typeCode"),
        FOREIGN KEY("awayTeamID") REFERENCES "teams"("id"),
        FOREIGN KEY("homeTeamID") REFERENCES "teams"("id"),
        FOREIGN KEY("winningGoalieID") REFERENCES "players"("id"),
        FOREIGN KEY("winningGoalscorerID") REFERENCES "players"("id"),
        CHECK (gameState = "OFF"),
        CHECK (gameScheduleState = "OK")
    );
    '''

    create_event_types_table_sql = '''
    CREATE TABLE IF NOT EXISTS event_types (
        typeCode INTEGER,
        typeDescKey TEXT NOT NULL,
        PRIMARY KEY("typeCode")
    );
    '''

    create_events_table_sql = '''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER,
        timeInPeriod TEXT,
        timeRemaining TEXT,
        awayGoalie INTEGER NOT NULL,
        awaySkaters INTEGER NOT NULL,
        homeGoalie INTEGER NOT NULL,
        homeSkaters INTEGER NOT NULL,
        homeTeamDefendingSide TEXT,
        typeCode INTEGER,
        sortOrder INTEGER,
        period INTEGER,
        periodType TEXT,
        eventOwnerTeamID INTEGER,
        losingPlayerID INTEGER,
        winningPlayerID INTEGER,
        xCoord REAL,
        yCoord REAL,
        zoneCode TEXT,
        hittingPlayerID INTEGER,
        hitteePlayerID INTEGER,
        blockingPlayerID INTEGER,
        shootingPlayerID INTEGER,
        reason TEXT,
        shotType TEXT,
        goalieInNetID INTEGER,
        eventOwnerPlayerID,
        penaltyDuration INTEGER,
        committedByPlayerID INTEGER,
        drawnByPlayerID INTEGER,
        scoringPlayerID INTEGER,
        assist1PlayerID INTEGER,
        assist2PlayerID INTEGER,
        gameID INTEGER,
        metaDateTime TEXT NOT NULL,
        PRIMARY KEY("id"),
        FOREIGN KEY("typeCode") REFERENCES "game_types"("typeCode"),
        FOREIGN KEY("eventOwnerTeamID") REFERENCES "teams"("id"),
        FOREIGN KEY("losingPlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("winningPlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("hittingPlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("hitteePlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("blockingPlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("shootingPlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("goalieInNetID") REFERENCES "players"("id"),
        FOREIGN KEY("eventOwnerPlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("committedByPlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("drawnByPlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("scoringPlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("assist1PlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("assist2PlayerID") REFERENCES "players"("id"),
        FOREIGN KEY("gameID") REFERENCES "games"("id")
    );
    '''
    commands = [create_teams_table_sql,
                create_players_table_sql,
                create_game_types_table_sql,
                create_games_table_sql,
                create_event_types_table_sql,
                create_events_table_sql]
    create_db_with_schema(db_path, *commands)


if __name__ == "__main__":
    main()
