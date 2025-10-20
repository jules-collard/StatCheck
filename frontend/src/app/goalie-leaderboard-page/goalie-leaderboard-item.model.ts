import { GoalieAdvanced, GoalieTotals } from "../player-page/goalie-stats.model";

export type GoalieLeaderboardItem = {
    playerID: number;
    fullName: string;
    position: 'G';
    qualified: boolean;
    isActive: boolean;
    teamTriCodes: string[];
    totals: GoalieTotals;
    advanced: GoalieAdvanced | null;
}