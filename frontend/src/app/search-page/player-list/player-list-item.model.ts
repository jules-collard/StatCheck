export type PlayerListItem = {
    id: number;
    fullName: string;
    position: 'G' | 'D' | 'L' | 'R' | 'C';
    teamTriCode: string | null;
    headshot: string;
};