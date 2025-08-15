import { Team } from "../../team/team.model";

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
}