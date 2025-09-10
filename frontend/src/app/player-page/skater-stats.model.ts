import { SkaterSeasonRecords } from "./season-totals-table/skater-season-records.model";

export type SkaterStats = {
    playerID: number;
    season: number;
    teamTriCode: string;
    totals: SkaterTotals;
    shooting: SkaterShooting;
}

type SkaterTotals = {
    gamesPlayed: number;
    goals: number;
    assists: number;
    plusMinus: number;
    hits: number;
    sog: number;
    blocks: number;
    penaltyMinutes: number;
    avgTOI: number;
    records?: SkaterSeasonRecords;
}

type SkaterShooting = {
    xg: number;
    xgGoals: number;
    fenwick: number;
}

type SkaterOnIce = {
    onIceShootingPct: number;
    fenwickFor: number;
    fenwickAgainst: number;
    corsiFor: number;
    corsiAgainst: number;
    xgFor: number;
    xgAgainst: number;
    oZoneStarts: number;
    nZoneStarts: number;
    dZoneStarts: number;
}