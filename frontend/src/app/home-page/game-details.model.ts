type GameState = 'FUT' | 'OFF' | 'PRE' | 'LIVE';
type PeriodType = 'REG' | 'OT' | 'SO';

type Team = {
  id: number;
  abbrev: string;
  record?: string;
  score?: number;
  sog?: number;
}

type Clock = {
  timeRemaining: string;
  inIntermission: boolean;
}

type PeriodDescriptor = {
  number: number;
  periodType: PeriodType;
}

type GameOutcome = {
  lastPeriodType: PeriodType;
}

export type GameDetails = {
  id: number;
  startTimeEastern: string;
  gameState: GameState;
  awayTeam: Team;
  homeTeam: Team;
  clock?: Clock;
  periodDescriptor?: PeriodDescriptor;
  gameOutcome?: GameOutcome;
}