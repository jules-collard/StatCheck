import { Team } from "../../team/team.model";
import { GoalieSeasonRecords } from "../season-totals-table/goalie-season-records.model";
import { SkaterSeasonRecords } from "../season-totals-table/skater-season-records.model";

export type GoalieTotals = {
    playerID: number;
    season: number;
    gamesPlayed: number;
    gamesStarted: number;
    wins: number;
    losses: number;
    goalsAgainstAvg: number;
    savePct: number;
    evenStrengthSavePct: number;
    powerPlaySavePct: number;
    team: Team;
    records?: GoalieSeasonRecords;
}