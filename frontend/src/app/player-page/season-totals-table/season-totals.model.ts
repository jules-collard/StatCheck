import { Team } from "../../team/team.model"
import { SkaterSeasonRecords } from "./skater-season-records.model";

export type SeasonTotals = {
    playerID: number;
    season: number;
    gamesPlayed: number;
    goals: number;
    assists: number;
    powerPlayGoals: number;
    plusMinus: number;
    hits: number;
    sog: number;
    blocks: number;
    penaltyMinutes: number;
    takeaways: number;
    giveaways: number;
    avgTOI: number;
    team: Team;
    records?: SkaterSeasonRecords;
}