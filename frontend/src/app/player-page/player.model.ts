import { Team } from "../team/team.model";

export type Player = {
    id: number;
    isActive: boolean;
    currentTeamID: number | null;
    firstName: string;
    lastName: string;
    sweaterNumber: number | null;
    position: string;
    headshot: string | null;
    heroImage: string | null;
    heightInInches: number | null;
    heightInCentimeters: number | null;
    weightInPounds: number | null;
    weightInKilograms: number | null;
    birthDate: string; // ISO date string
    birthCity: string | null;
    birthCountry: string | null;
    shootsCatches: string;
    draftYear: number | null;
    draftTeamAbbrev: string | null;
    draftRound: number | null;
    draftPickInRound: number | null;
    draftOverallPick: number | null;
    team: Team | null;
};