import { SkaterSeasonRecords } from "./skater-totals-table/skater-season-records.model";

export type SkaterStats = {
    playerID: number;
    season: number;
    teamTriCodes: string[];
    totals: SkaterTotals;
    shooting: SkaterShooting;
    onIce: SkaterOnIce
}

export type SkaterTotals = {
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

export type SkaterShooting = {
    xg: number;
    xgGoals: number;
    fenwick: number;
}

export type SkaterOnIce = {
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