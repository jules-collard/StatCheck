import { Team } from "../team/team.model";
import { Award } from "./award.model";

export type Player = {
    id: number;
    isActive: boolean;
    currentTeamID: number | null;
    firstName: string;
    lastName: string;
    sweaterNumber: number | null;
    position: "G" | "D" | "L" | "C" | "R";
    headshot: string;
    heightInInches: number;
    heightInCentimeters: number;
    weightInPounds: number;
    weightInKilograms: number;
    birthDate: string; // ISO date string
    birthCountry: string;
    shootsCatches: string;
    draftYear: number | null;
    draftTeamAbbrev: string | null;
    draftRound: number | null;
    draftPickInRound: number | null;
    draftOverallPick: number | null;
    inHHOF: boolean | null;
    team: Team | null;
    awards: Award[];
};