import { Team } from "../../team/team.model";
import { GoalieSeasonRecords } from "../season-totals-table/goalie-season-records.model";

export type GoalieTotals = {
    playerID: number;
    season: number;
    gamesPlayed: number;
    gamesStarted: number;
    wins: number;
    losses: number;
    goalsAgainst: number;
    goalsAgainstAvg: number;
    savePct: number;
    evenStrengthSavePct: number;
    powerPlaySavePct: number;
    xgAgainst: number;
    xgGoalsAgainst: number;
    fenwickAgainst: number;
    team: Team;
    records?: GoalieSeasonRecords;
}