import { GoalieSeasonRecords } from "./goalie-totals-table/goalie-season-records.model";

export type GoalieStats = {
    playerID: number;
    season: number;
    teamTriCodes: string[];
    totals: GoalieTotals;
    advanced: GoalieAdvanced;
}

type GoalieTotals = {
    gamesPlayed: number;
    gamesStarted: number;
    wins: number;
    losses: number;
    goalsAgainst: number;
    goalsAgainstAvg: number;
    savePct?: number;
    evenStrengthSavePct?: number;
    powerPlaySavePct?: number;
    xgAgainst: number;
    xgGoalsAgainst: number;
    fenwickAgainst: number;
    records?: GoalieSeasonRecords;
}

type GoalieAdvanced = {
    xgAgainst: number;
    xgGoalsAgainst: number;
    fenwickAgainst: number;
}