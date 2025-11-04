export type GameState = {
    finished: boolean;
    timeRemaining: string;
    period: number;
    periodType: 'REG' | 'OT' | 'SO';
    lastPeriodType: 'REG' | 'OT' | 'SO';
}