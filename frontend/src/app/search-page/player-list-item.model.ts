export type PlayerListItem = {
    id: number;
    fullName: string;
    isActive: boolean;
    position: 'G' | 'D' | 'L' | 'R' | 'C';
    teamTriCode: string | null;
    headshot: string;
};