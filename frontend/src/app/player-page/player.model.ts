import { Team } from "../team/team.model";

export type Player = {
    id: number;
    isActive: boolean;
    currentTeamID: number | null;
    firstName: string;
    lastName: string;
    sweaterNumber: number | null;
    position: "G" | "D" | "L" | "C" | "R";
    headshot: string;
    heroImage: string | null;
    heightInInches: number;
    heightInCentimeters: number;
    weightInPounds: number;
    weightInKilograms: number;
    birthDate: string; // ISO date string
    birthCity: string | null;
    birthCountry: string;
    shootsCatches: string;
    draftYear: number | null;
    draftTeamAbbrev: string | null;
    draftRound: number | null;
    draftPickInRound: number | null;
    draftOverallPick: number | null;
    team: Team | null;
};