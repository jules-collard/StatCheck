type ConferenceAbbrev = 'E' | 'W';
type DivisionAbbrev = 'C' | 'P' | 'M' | 'A';

export type StandingsItem = {
  conferenceAbbrev: ConferenceAbbrev;
  divisionAbbrev: DivisionAbbrev;
  gamesPlayed: number;
  goalDifferential: number;
  goalAgainst: number;
  goalFor: number;
  losses: number;
  otLosses: number;
  wins: number;
  points: number;
  pointPctg: number;
  leagueSequence: number;
  teamAbbrev: string;
  teamLogo: string;
  l10Wins: number;
  l10Losses: number;
  l10OtLosses: number;
};