export type Game = {
    id: number;
    season: number;
    gameType: number;
    neutralSite: boolean;
    startTimeUTC: string; // ISO datetime string
    venueUTCOffset: number;
    gameState: string;
    gameScheduleState: string;
    defaultVenue: string;
    awayTeamID: number;
    awayTeamScore: number;
    homeTeamID: number;
    homeTeamScore: number;
    maxRegulationPeriods: number;
    lastPeriodType: string;
};