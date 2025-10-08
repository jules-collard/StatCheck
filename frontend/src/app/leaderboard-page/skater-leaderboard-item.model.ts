import { SkaterTotals } from "../player-page/skater-stats.model";

export type SkaterLeaderboardItem = {
    playerID: number;
    firstName: string;
    lastName: string;
    teamTriCodes: string[];
    totals: SkaterTotals
}