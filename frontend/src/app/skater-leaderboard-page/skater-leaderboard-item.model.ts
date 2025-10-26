import { SkaterOnIce, SkaterShooting, SkaterTotals } from "../player-page/skater-stats.model";
import { Position } from "../shared/util-types";

export type SkaterLeaderboardItem = {
    playerID: number;
    fullName: string;
    isActive: boolean;
    qualified: boolean;
    shotsQualified: boolean;
    position: Position;
    teamTriCodes: string[];
    totals: SkaterTotals
    shooting: SkaterShooting
    onIce: SkaterOnIce
}