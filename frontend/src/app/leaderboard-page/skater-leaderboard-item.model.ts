import { SkaterTotals } from "../player-page/skater-stats.model";
import { Position } from "../shared/util-types";

export type SkaterLeaderboardItem = {
    playerID: number;
    firstName: string;
    lastName: string;
    position: Position;
    teamTriCodes: string[];
    totals: SkaterTotals
}